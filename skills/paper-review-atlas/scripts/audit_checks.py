"""Deterministic, evidence-preserving helpers for a paper review.

This module uses only the Python standard library.  It never imports a project,
runs a command, evaluates an expression, or treats manuscript text as code.

Public APIs
===========
``resolve_under_root(root, path, must_exist=True)`` resolves a path confined to
an explicit root. ``verify_quote(root, path, quote, line=None)`` checks exact
UTF-8 text, optionally requiring the match to START on a real 1-based line.

``reconcile_number(root, claim)`` accepts the following bounded declaration::

    {"source": {"path": "results.csv", "format": "csv",
                "where": {"model": "new"}},
     "operation": "mean", "field": "accuracy", "reported": "85.2",
     "source_unit": "fraction", "reported_unit": "percent",
     "rounding": {"places": 1, "mode": "half_even"}, "tolerance": "0"}

Sources are CSV records, a JSON array of objects, or a JSON object containing an
array at the exact ``records_key`` key. ``where`` is equality on scalar fields;
it is not an expression language. Operations are value, mean, sum, and count.
``value`` requires exactly one selected row. Empty groups and missing values
are unverified, including count of an empty group. Count uses number units and
omits field. Tolerance is a nonnegative absolute tolerance in REPORTED units;
it is applied after the declared Decimal rounding, never guessed from display.

A comparison adds ``comparison: {source, operation, field}`` and ``change``.
The primary source is current/new and comparison is baseline/reference.
``relative_percent`` means (current - baseline) / baseline * 100 and requires
reported_unit=percent. ``percentage_points`` subtracts their percent values
and requires reported_unit=percentage_point. Both use the same source_unit.
Units are explicit: number, fraction, percent, or percentage_point.

``paired_run_stats(left, right)`` accepts mappings from identical run IDs to
finite numbers, reporting right-minus-left differences and SAMPLE SD (n - 1).
One run permits a difference but not a sample SD or a claim of no effect. This
helper supplies no p-value or confidence interval and makes no independence,
randomization, distribution, or inferential-validity claim.

``validate_issue(issue, root=None)`` and ``validate_report(report, root=None)``
return validation records. An issue has id, status (confirmed/unverified/closed),
severity (critical/major/minor/editorial), fix, and acceptance_check. A confirmed
issue additionally needs location={path,line?} and evidence={quote,line?}.
With no root, evidence cannot be verified. A closed issue also needs
revision_evidence={path,quote,line?} and
check={status:'passed',method:'specific recorded check',
       observations:'specific observation', evidence:{path,quote,line?}}.
An optional check.evaluation={kind:'quote',path,quote,line?} or
{kind:'number',claim:<numeric declaration>} is actually recomputed and replaces
the manual-observations requirement. Manual closure has scope
recorded_evidence_only; recomputed closure has scope declarative_check_recomputed.
Neither verifies the scientific semantics of a reviewer judgment.
Self-asserted evidence.status is ignored.
``recheck_issue`` applies those same closure requirements.

A report has issues (which may be empty), optional reviewers (id/model/family),
independence_claim (none/multi_persona/cross_family), and optional coverage.
Coverage maps names to {status: passed/unverified/not_applicable,
evidence: [{path,quote,line?}]}; passed requires an actual verified record.
Text evidence for a visual audit is its inspection log, not image contents.
Each coverage entry may contain ``artifacts``, a list of source artifact paths,
whose presence is checked separately and never substitutes for an inspection
record. Visual coverage (figure/image/visual names or kind='visual') requires
at least one source artifact and records only log anchors/artifact presence.

Statuses distinguish a contradictory observation (mismatch/invalid) from
missing evidence (unverified). Malformed or unsafe declarations raise
AuditInputError; unavailable source data return unverified. Schema validation
does not authenticate reviewer identities or establish scientific truth.
"""

from __future__ import annotations

import csv
import io
import json
import math
import os
import re
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN, ROUND_HALF_UP, localcontext
from pathlib import Path
from typing import Any


MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_RECORDS = 10_000
MAX_QUOTE_CHARS = 20_000
MAX_QUOTE_MATCHES = 100
DECIMAL_PRECISION = 180
UNITS = frozenset({"number", "fraction", "percent", "percentage_point"})
SEVERITIES = frozenset({"critical", "major", "minor", "editorial"})


class AuditInputError(ValueError):
    """A malformed, unsafe, or unsupported audit declaration."""


class _Unavailable(ValueError):
    """Evidence exists incompletely or cannot be read; not a contradiction."""


def resolve_under_root(root: os.PathLike[str] | str, path: os.PathLike[str] | str,
                       must_exist: bool = True) -> Path:
    """Return a resolved, root-contained path; reject traversal and escapes.

    Absolute paths are accepted only inside root. Any explicit ``..`` path
    component is rejected, even if normalization would bring it back inside.
    Symlinks resolving outside root (including dangling ones) are rejected.
    The root must already exist and be a directory. No file is executed.
    """
    try:
        anchor = Path(root).resolve(strict=True)
        raw = os.fspath(path)
        if not isinstance(raw, str) or not raw or "\x00" in raw:
            raise AuditInputError("path must be a nonempty text path without NUL")
        candidate = Path(raw)
        if ".." in candidate.parts:
            raise AuditInputError("parent traversal ('..') is not allowed")
        if not anchor.is_dir():
            raise AuditInputError("root must be an existing directory")
        target = candidate if candidate.is_absolute() else anchor / candidate
        # Check containment before strict existence so an absent external path
        # cannot disguise an escape as merely missing evidence.
        resolved = target.resolve(strict=False)
        try:
            resolved.relative_to(anchor)
        except ValueError as exc:
            raise AuditInputError("path resolves outside the declared root") from exc
        if must_exist:
            resolved = resolved.resolve(strict=True)
        return resolved
    except AuditInputError:
        raise
    except (TypeError, ValueError, RuntimeError) as exc:
        raise AuditInputError(f"invalid path: {exc}") from exc


def _read_bytes(root: os.PathLike[str] | str, path: str) -> tuple[str, bytes]:
    target = resolve_under_root(root, path, must_exist=False)
    anchor = Path(root).resolve(strict=True)
    relative = target.relative_to(anchor).as_posix()
    try:
        if not target.is_file():
            raise _Unavailable(f"source is missing or is not a regular file: {relative}")
        with target.open("rb") as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
    except OSError as exc:
        raise _Unavailable(f"cannot read source {relative}: {exc.strerror or type(exc).__name__}") from exc
    if len(data) > MAX_FILE_BYTES:
        raise _Unavailable(f"source exceeds {MAX_FILE_BYTES} byte audit limit")
    return relative, data


def _read_text(root: os.PathLike[str] | str, path: str) -> tuple[str, str]:
    relative, data = _read_bytes(root, path)
    try:
        # Decode directly: no silent whitespace, Unicode, or newline changes.
        return relative, data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise _Unavailable(f"source is not valid UTF-8: {relative}") from exc


def _line_number(line: Any) -> int | None:
    if line is not None and (isinstance(line, bool) or not isinstance(line, int) or line < 1):
        raise AuditInputError("line must be a positive 1-based integer")
    return line


def verify_quote(root: os.PathLike[str] | str, path: str, quote: str,
                 line: int | None = None) -> dict[str, Any]:
    """Verify an exact quote and optional start-line anchor without guessing.

    Missing/unreadable/non-UTF-8 files are unverified. A readable file with the
    wrong quote or wrong supplied anchor is mismatch. Matches report their real
    start/end lines and 1-based start columns. At most 100 matches are returned.
    """
    _line_number(line)
    if not isinstance(quote, str) or not quote.strip():
        raise AuditInputError("quote must contain non-whitespace text")
    if len(quote) > MAX_QUOTE_CHARS:
        raise AuditInputError(f"quote exceeds {MAX_QUOTE_CHARS} character limit")
    result: dict[str, Any] = {"status": "unverified", "source": str(path),
                              "requested_line": line, "matches": []}
    try:
        source, body = _read_text(root, path)
    except _Unavailable as exc:
        result["message"] = str(exc)
        return result
    result["source"] = source
    cursor = 0
    last_position, current_line = 0, 1
    line_span = quote.count("\n") - int(quote.endswith("\n"))
    elsewhere: set[int] = set()
    while True:
        position = body.find(quote, cursor)
        if position < 0:
            break
        current_line += body.count("\n", last_position, position)
        last_position, start_line = position, current_line
        if line is None or start_line == line:
            result["matches"].append({
                "line_start": start_line,
                "line_end": start_line + line_span,
                "column_start": position - body.rfind("\n", 0, position),
            })
            if len(result["matches"]) == MAX_QUOTE_MATCHES:
                result["matches_truncated"] = body.find(quote, position + 1) >= 0
                break
        elif len(elsewhere) < MAX_QUOTE_MATCHES:
            elsewhere.add(start_line)
        cursor = position + 1
    result["status"] = "verified" if result["matches"] else "mismatch"
    result["message"] = ("exact quote and anchor verified" if result["matches"]
                         else "exact quote not present at the declared location")
    if elsewhere and not result["matches"]:
        result["actual_start_lines"] = sorted(elsewhere)
    return result


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise AuditInputError(f"{label} must be an object with text keys")
    return value


def _keys(value: Mapping[str, Any], allowed: set[str], required: set[str], label: str) -> None:
    extra, missing = set(value) - allowed, required - set(value)
    if extra:
        raise AuditInputError(f"unsupported {label} field(s): {', '.join(sorted(extra))}")
    if missing:
        raise AuditInputError(f"missing {label} field(s): {', '.join(sorted(missing))}")


def _text_field(value: Any, label: str, limit: int = 1024) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise AuditInputError(f"{label} must be nonempty text of at most {limit} characters")
    return value


def _choice(value: Any, choices: set[str] | frozenset[str], label: str) -> str:
    if not isinstance(value, str) or value not in choices:
        raise AuditInputError(f"{label} must be one of: {', '.join(sorted(choices))}")
    return value


def _decimal(value: Any, label: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise AuditInputError(f"{label} must be a finite decimal number, not bool or null")
    if isinstance(value, float) and not math.isfinite(value):
        raise AuditInputError(f"{label} must be finite")
    if isinstance(value, str) and (not value.strip() or len(value) > 128):
        raise AuditInputError(f"{label} must be a bounded decimal number")
    try:
        token = str(value).strip()
        if len(token) > 128 or not re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", token):
            raise AuditInputError(f"{label} must be a finite decimal literal")
        number = Decimal(token)
    except (InvalidOperation, ValueError) as exc:
        raise AuditInputError(f"{label} is not a decimal number") from exc
    if not number.is_finite():
        raise AuditInputError(f"{label} must be finite; NaN and infinity are forbidden")
    if len(number.as_tuple().digits) > 30 or abs(number.as_tuple().exponent) > 50:
        raise AuditInputError(f"{label} exceeds the 30-digit / exponent-50 numeric bound")
    return number


def _decimal_text(value: Decimal) -> str:
    if value == 0:
        return "0"
    text = format(value, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def _source_spec(value: Any) -> Mapping[str, Any]:
    source = _mapping(value, "source")
    _keys(source, {"path", "format", "records_key", "where"}, {"path", "format"}, "source")
    _text_field(source["path"], "source.path", 4096)
    _choice(source["format"], {"csv", "json"}, "source.format")
    if "records_key" in source:
        if source["format"] != "json":
            raise AuditInputError("records_key is only valid for JSON")
        _text_field(source["records_key"], "records_key", 128)
    where = _mapping(source.get("where", {}), "source.where")
    if len(where) > 16:
        raise AuditInputError("at most 16 equality filters are supported")
    for key, val in where.items():
        _text_field(key, "filter field", 128)
        if val is not None and not isinstance(val, (str, int, float, Decimal, bool)):
            raise AuditInputError("filter values must be scalars, not expressions or containers")
        if isinstance(val, str) and len(val) > 4096:
            raise AuditInputError("filter text exceeds limit")
        if isinstance(val, (int, float, Decimal)) and not isinstance(val, bool):
            _decimal(val, "filter value")
    return source


def _equal_scalar(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float, Decimal)) and isinstance(right, (int, float, Decimal)):
        return _decimal(left, "source filter value") == _decimal(right, "filter value")
    return type(left) is type(right) and left == right


def _load_records(root: os.PathLike[str] | str, source: Mapping[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path, text = _read_text(root, source["path"])
    try:
        if source["format"] == "csv":
            reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
            headers = reader.fieldnames
            if not headers or any(not name for name in headers) or len(set(headers)) != len(headers):
                raise _Unavailable("CSV requires nonempty, unique column names")
            rows = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise _Unavailable("CSV record has missing or excess columns")
                rows.append(row)
                if len(rows) > MAX_RECORDS:
                    raise _Unavailable(f"source exceeds {MAX_RECORDS} record limit")
        else:
            def bad_constant(token: str) -> None:
                raise ValueError(f"nonfinite JSON number {token}")

            def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
                obj: dict[str, Any] = {}
                for key, item in pairs:
                    if key in obj:
                        raise ValueError(f"duplicate JSON key: {key}")
                    obj[key] = item
                return obj

            payload = json.loads(text, parse_float=Decimal, parse_constant=bad_constant,
                                 object_pairs_hook=unique_object)
            if "records_key" in source:
                if not isinstance(payload, dict) or source["records_key"] not in payload:
                    raise _Unavailable("declared JSON records_key is absent")
                payload = payload[source["records_key"]]
            if not isinstance(payload, list) or any(not isinstance(row, dict) for row in payload):
                raise _Unavailable("JSON source must contain an array of record objects")
            if len(payload) > MAX_RECORDS:
                raise _Unavailable(f"source exceeds {MAX_RECORDS} record limit")
            rows = payload
    except (csv.Error, json.JSONDecodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, _Unavailable):
            raise
        raise _Unavailable(f"source cannot be parsed: {exc}") from exc
    where = source.get("where", {})
    try:
        selected = [row for row in rows if all(key in row and _equal_scalar(row[key], val)
                                               for key, val in where.items())]
    except AuditInputError as exc:
        raise _Unavailable(f"invalid source filter value: {exc}") from exc
    return selected, {"path": path, "rows_total": len(rows), "rows_selected": len(selected)}


def _aggregation_spec(spec: Any, *, comparison: bool = False) -> Mapping[str, Any]:
    spec = _mapping(spec, "comparison" if comparison else "claim")
    if comparison:
        _keys(spec, {"source", "operation", "field"}, {"source", "operation"}, "comparison")
    _source_spec(spec["source"])
    operation = spec["operation"]
    _choice(operation, {"value", "mean", "sum", "count"}, "operation")
    if comparison and operation == "count":
        raise AuditInputError("comparison operation cannot be count")
    if operation == "count":
        if "field" in spec:
            raise AuditInputError("count counts records; omit field")
    else:
        _text_field(spec.get("field"), "field", 128)
    return spec


def _aggregate(root: os.PathLike[str] | str, spec: Mapping[str, Any]) -> tuple[Decimal, dict[str, Any]]:
    rows, provenance = _load_records(root, spec["source"])
    if not rows:
        raise _Unavailable("selected source group is empty")
    operation = spec["operation"]
    if operation == "count":
        return Decimal(len(rows)), provenance
    if operation == "value" and len(rows) != 1:
        raise _Unavailable("value requires exactly one selected record")
    values = []
    for index, row in enumerate(rows, 1):
        if spec["field"] not in row or row[spec["field"]] is None or row[spec["field"]] == "":
            raise _Unavailable(f"selected record {index} lacks a numeric value for {spec['field']}")
        try:
            values.append(_decimal(row[spec["field"]], f"selected record {index}"))
        except AuditInputError as exc:
            raise _Unavailable(f"source numeric value rejected: {exc}") from exc
    total = sum(values, Decimal(0))
    value = values[0] if operation == "value" else total / len(values) if operation == "mean" else total
    return value, provenance


def _convert_unit(value: Decimal, source_unit: str, reported_unit: str) -> Decimal:
    if source_unit == reported_unit:
        return value
    if (source_unit, reported_unit) == ("fraction", "percent"):
        return value * 100
    if (source_unit, reported_unit) == ("percent", "fraction"):
        return value / 100
    raise AuditInputError(f"incompatible units: {source_unit} to {reported_unit}")


def reconcile_number(root: os.PathLike[str] | str, claim: Mapping[str, Any]) -> dict[str, Any]:
    """Reconcile a reported number against a bounded CSV/JSON declaration.

    See the module docstring for the complete schema. Source data never become
    executable expressions. An absent or unusable source produces unverified,
    while a readable, calculable disagreement produces mismatch.
    """
    claim = _mapping(claim, "claim")
    _keys(claim, {"id", "source", "operation", "field", "reported", "source_unit",
                  "reported_unit", "rounding", "tolerance", "comparison", "change"},
          {"source", "operation", "reported", "source_unit", "reported_unit"}, "claim")
    _aggregation_spec(claim)
    reported = _decimal(claim["reported"], "reported")
    tolerance = _decimal(claim.get("tolerance", "0"), "tolerance")
    if tolerance < 0:
        raise AuditInputError("tolerance must be nonnegative")
    source_unit, reported_unit = claim["source_unit"], claim["reported_unit"]
    _choice(source_unit, UNITS, "source_unit")
    _choice(reported_unit, UNITS, "reported_unit")
    if claim["operation"] == "count" and (source_unit != "number" or reported_unit != "number"):
        raise AuditInputError("count requires number units")
    if "id" in claim:
        _text_field(claim["id"], "id", 128)
    rounding = claim.get("rounding")
    if rounding is not None:
        rounding = _mapping(rounding, "rounding")
        _keys(rounding, {"places", "mode"}, {"places"}, "rounding")
        places = rounding["places"]
        if isinstance(places, bool) or not isinstance(places, int) or not -12 <= places <= 12:
            raise AuditInputError("rounding.places must be an integer from -12 to 12")
        _choice(rounding.get("mode", "half_even"), {"half_even", "half_up"}, "rounding.mode")
    if ("comparison" in claim) != ("change" in claim):
        raise AuditInputError("comparison and change must be specified together")
    if "comparison" in claim:
        _aggregation_spec(claim["comparison"], comparison=True)
        _choice(claim["change"], {"relative_percent", "percentage_points"}, "change")
        if claim["change"] == "relative_percent":
            if reported_unit != "percent" or source_unit == "percentage_point":
                raise AuditInputError("relative_percent requires percent output and number/fraction/percent source")
        elif source_unit not in {"fraction", "percent"} or reported_unit != "percentage_point":
            raise AuditInputError("percentage_points requires fraction/percent source and percentage_point output")
    else:
        _convert_unit(Decimal(0), source_unit, reported_unit)
    result: dict[str, Any] = {"status": "unverified", "reported": _decimal_text(reported),
                              "reported_unit": reported_unit, "tolerance": _decimal_text(tolerance)}
    if "id" in claim:
        result["id"] = claim["id"]
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        try:
            current, provenance = _aggregate(root, claim)
            result["source"] = provenance
            if "comparison" in claim:
                baseline, baseline_provenance = _aggregate(root, claim["comparison"])
                result["baseline"] = baseline_provenance
                if claim["change"] == "relative_percent":
                    if baseline == 0:
                        raise _Unavailable("relative change is undefined for a zero baseline")
                    calculated = (current - baseline) / baseline * 100
                else:
                    calculated = _convert_unit(current - baseline, source_unit, "percent")
            else:
                calculated = _convert_unit(current, source_unit, reported_unit)
        except _Unavailable as exc:
            result["message"] = str(exc)
            return result
        rounded = calculated
        if rounding is not None:
            mode = ROUND_HALF_EVEN if rounding.get("mode", "half_even") == "half_even" else ROUND_HALF_UP
            rounded = calculated.quantize(Decimal(1).scaleb(-rounding["places"]), rounding=mode)
        error = abs(rounded - reported)
        result.update({"status": "verified" if error <= tolerance else "mismatch",
                       "calculated": _decimal_text(calculated),
                       "rounded_calculated": _decimal_text(rounded),
                       "absolute_error": _decimal_text(error),
                       "message": "reported value agrees with declared calculation" if error <= tolerance
                       else "reported value disagrees with declared calculation"})
    return result


def paired_run_stats(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, Any]:
    """Return deterministic descriptive paired statistics; never infer a p-value.

    Run IDs must be nonempty text and must match exactly. No automatic dropping,
    positional pairing, or implicit seed imputation is permitted. Invalid
    numbers raise AuditInputError; missing pairs/empty inputs are unverified.
    """
    left, right = _mapping(left, "left runs"), _mapping(right, "right runs")
    if len(left) > MAX_RECORDS or len(right) > MAX_RECORDS:
        raise AuditInputError(f"at most {MAX_RECORDS} paired runs are supported")
    for key in set(left) | set(right):
        _text_field(key, "run ID", 128)
    result: dict[str, Any] = {"status": "unverified", "n": 0,
                              "difference_convention": "right_minus_left",
                              "inference_status": "unverified", "p_value": None,
                              "confidence_interval": None}
    if set(left) != set(right):
        result.update({"message": "paired run IDs do not match; no rows were silently dropped",
                       "missing_from_left": sorted(set(right) - set(left)),
                       "missing_from_right": sorted(set(left) - set(right))})
        return result
    if not left:
        result["message"] = "no paired runs are available"
        return result
    ids = sorted(left)
    a = [_decimal(left[key], f"left run {key}") for key in ids]
    b = [_decimal(right[key], f"right run {key}") for key in ids]
    with localcontext() as context:
        context.prec = DECIMAL_PRECISION
        differences = [new - old for old, new in zip(a, b)]

        def describe(values: list[Decimal]) -> dict[str, Any]:
            mean = sum(values, Decimal(0)) / len(values)
            variance = (sum(((value - mean) ** 2 for value in values), Decimal(0)) / (len(values) - 1)
                        if len(values) > 1 else None)
            return {"n": len(values), "mean": _decimal_text(mean),
                    "sample_sd": None if variance is None else _decimal_text(variance.sqrt())}

        result.update({"status": "verified" if len(ids) > 1 else "unverified",
                       "descriptive_status": "verified", "n": len(ids), "run_ids": ids,
                       "left": describe(a), "right": describe(b), "difference": describe(differences),
                       "paired_differences": {key: _decimal_text(value) for key, value in zip(ids, differences)},
                       "message": "descriptive calculations verified; inferential assumptions were not assessed"
                       if len(ids) > 1 else "one paired run: sample SD and effect inference are not established",
                       "limitations": ["No p-value or confidence interval is implied by these descriptive statistics.",
                                       "Zero observed difference does not establish equivalence or absence of an effect.",
                                       "Matched run labels do not establish independent experimental units."]})
    return result


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _actionable(value: Any) -> bool:
    return _nonempty(value) and value.strip().casefold() not in {
        "fix", "fix it", "done", "tbd", "todo", "n/a", "none", "check", "improve", "待定", "修复", "完成",
        "looks good", "reviewer approved", "approved", "lgtm", "all good", "看起来没问题", "审稿人同意"
    }


def _probability_claims(value: Any) -> list[str]:
    forbidden = {"acceptance_probability", "acceptance_chance", "acceptance_odds", "publication_probability",
                 "probability_of_acceptance", "estimated_acceptance_probability", "chance_of_acceptance"}
    found: list[str] = []
    pending = [(value, "$", 0)]
    visited = 0
    while pending:
        node, path, depth = pending.pop()
        visited += 1
        if depth > 32 or visited > 20_000:
            found.append("report structure exceeds validation bounds")
            break
        if isinstance(node, Mapping):
            for key, item in node.items():
                normalized = str(key).strip().casefold().replace(" ", "_").replace("-", "_")
                if normalized in forbidden and item is not None and item not in (
                        "unknown", "unavailable", "not estimated", "not estimable"):
                    found.append(f"unsupported acceptance-probability claim at {path}.{key}")
                pending.append((item, f"{path}.{key}", depth + 1))
        elif isinstance(node, (list, tuple)):
            pending.extend((item, f"{path}[{index}]", depth + 1) for index, item in enumerate(node))
    return found


def _evidence(record: Any, root: os.PathLike[str] | str | None,
              location: Any = None) -> dict[str, Any]:
    if not isinstance(record, Mapping):
        return {"status": "unverified", "message": "evidence record is missing"}
    location = location if isinstance(location, Mapping) else {}
    path, quote = record.get("path", location.get("path")), record.get("quote")
    if record.get("path") is not None and location.get("path") is not None and record["path"] != location["path"]:
        return {"status": "mismatch", "message": "evidence path conflicts with issue location"}
    if record.get("line") is not None and location.get("line") is not None and record["line"] != location["line"]:
        return {"status": "mismatch", "message": "evidence line conflicts with issue location"}
    if not _nonempty(path) or not _nonempty(quote):
        return {"status": "unverified", "message": "evidence requires an artifact path and exact quote"}
    line = record.get("line", location.get("line"))
    try:
        _line_number(line)
        if root is None:
            return {"status": "unverified", "message": "no root supplied; evidence was not checked"}
        return verify_quote(root, path, quote, line=line)
    except (AuditInputError, FileNotFoundError, OSError) as exc:
        return {"status": "mismatch", "message": f"invalid evidence declaration: {exc}"}


def evaluate_check(root: os.PathLike[str] | str, specification: Mapping[str, Any]) -> dict[str, Any]:
    """Actually rerun one bounded quote or number check, with no project execution.

    A verified quote means only exact text is present. A verified number means
    only the declared arithmetic reconciles. Neither establishes semantic truth.
    """
    specification = _mapping(specification, "check.evaluation")
    kind = specification.get("kind")
    _choice(kind, {"quote", "number"}, "check.evaluation.kind")
    if kind == "quote":
        _keys(specification, {"kind", "path", "quote", "line"}, {"kind", "path", "quote"}, "quote evaluation")
        result = verify_quote(root, specification["path"], specification["quote"], specification.get("line"))
    else:
        _keys(specification, {"kind", "claim"}, {"kind", "claim"}, "number evaluation")
        result = reconcile_number(root, specification["claim"])
    return dict(result, evaluation_kind=kind, execution_scope="builtin_declarative_check_only")


def _closure(revision_evidence: Any, check: Any,
             root: os.PathLike[str] | str | None) -> dict[str, Any]:
    revision = _evidence(revision_evidence, root)
    result: dict[str, Any] = {"status": "unverified", "revision_evidence": revision,
                              "closure_scope": "recorded_evidence_only"}
    if not isinstance(check, Mapping):
        result["message"] = "closure requires a recorded check, not an author's assertion"
        return result
    method = check.get("method")
    if not _actionable(method) or method.strip().casefold() in {
        "author says done", "author assertion", "author confirmation", "作者说已完成", "作者确认"
    }:
        result["message"] = "closure requires a specific check method, not an author's assertion"
        return result
    record = _evidence(check.get("evidence"), root)
    result["check_evidence"] = record
    evaluation = None
    if "evaluation" in check:
        if root is None:
            result["message"] = "no root supplied; declarative check could not be rerun"
            return result
        try:
            evaluation = evaluate_check(root, check["evaluation"])
        except (AuditInputError, OSError) as exc:
            result.update(status="mismatch", message=f"declarative check rejected: {exc}")
            return result
        result["closure_scope"] = "declarative_check_recomputed"
        result["check_evaluation"] = evaluation
    elif not _actionable(check.get("observations")):
        result["message"] = "manual check requires specific recorded observations"
        return result
    if revision["status"] == "mismatch" or record["status"] == "mismatch":
        result.update(status="mismatch", message="closure evidence contradicts its declared location")
    elif evaluation is not None and evaluation["status"] == "mismatch":
        result.update(status="mismatch", message="recomputed declarative check failed")
    elif evaluation is not None and evaluation["status"] != "verified":
        result["message"] = "recomputed declarative check remains unverified"
    elif check.get("status") != "passed":
        result["message"] = "recorded check has not passed"
    elif revision["status"] == "verified" and record["status"] == "verified":
        result.update(status="verified", message="revision and check record anchors verified; semantic judgment is not authenticated")
    else:
        result["message"] = "revision evidence or check record remains unverified"
    return result


def validate_issue(issue: Mapping[str, Any], root: os.PathLike[str] | str | None = None) -> dict[str, Any]:
    """Validate an issue without elevating unsupported assertions into findings.

    ``status`` is valid/invalid/unverified. ``effective_status`` is the strongest
    evidentiary state actually established. An unsuccessful closure preserves a
    supported issue as confirmed/open; it does not erase the original finding.
    """
    result: dict[str, Any] = {"status": "invalid", "effective_status": "unverified", "errors": [], "warnings": [],
                              "validation_scope": "record_structure_and_exact_evidence_anchors"}
    if not isinstance(issue, Mapping):
        result["errors"].append("issue must be an object")
        return result
    result["id"] = issue.get("id")
    errors, warnings = result["errors"], result["warnings"]
    errors.extend(_probability_claims(issue))
    if not _nonempty(issue.get("id")):
        errors.append("issue requires a nonempty id")
    if not isinstance(issue.get("severity"), str) or issue.get("severity") not in SEVERITIES:
        errors.append("severity must be critical, major, minor, or editorial")
    requested = issue.get("status", "unverified")
    if not isinstance(requested, str) or requested not in {"confirmed", "unverified", "closed"}:
        errors.append("issue status must be confirmed, unverified, or closed")
        requested = "unverified"
    if not _actionable(issue.get("fix")):
        errors.append("issue requires a specific actionable fix")
    if not _actionable(issue.get("acceptance_check")):
        errors.append("issue requires a specific acceptance check")
    if requested in {"confirmed", "closed"}:
        location = issue.get("location")
        if not isinstance(location, Mapping) or not _nonempty(location.get("path")):
            warnings.append("confirmed issue requires a concrete source location")
            evidence = {"status": "unverified", "message": "issue location missing"}
        else:
            evidence = _evidence(issue.get("evidence"), root, location)
        result["evidence_check"] = evidence
        if evidence["status"] == "verified":
            result["effective_status"] = "confirmed"
        elif evidence["status"] == "mismatch":
            errors.append(f"issue evidence mismatch: {evidence['message']}")
        else:
            warnings.append(f"issue remains unverified: {evidence['message']}")
    if requested == "closed":
        closure = _closure(issue.get("revision_evidence"), issue.get("check"), root)
        result["closure_check"] = closure
        if closure["status"] == "verified" and result["effective_status"] == "confirmed":
            result["effective_status"] = "closed"
        elif closure["status"] == "mismatch":
            errors.append(closure["message"])
        else:
            warnings.append(f"issue cannot close: {closure['message']}")
    if errors:
        result["status"] = "invalid"
        if result["effective_status"] == "closed":
            result["effective_status"] = "confirmed"
    elif requested == "unverified":
        result["status"] = "valid"
    elif result["effective_status"] != requested:
        result["status"] = "unverified"
    else:
        result["status"] = "valid"
    return result


def _validate_coverage(coverage: Any, root: os.PathLike[str] | str | None) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    results: dict[str, Any] = {}
    if not isinstance(coverage, Mapping):
        return ["coverage must be an object"], warnings, results
    for name, declaration in coverage.items():
        if not isinstance(name, str) or not isinstance(declaration, Mapping):
            errors.append("coverage entries require a text name and object declaration")
            continue
        status = declaration.get("status")
        if not isinstance(status, str) or status not in {"passed", "unverified", "not_applicable"}:
            errors.append(f"coverage.{name} has an unsupported status")
            continue
        if status != "passed":
            results[name] = {"status": status,
                             "validation_scope": "inspection_record_anchors_and_artifact_presence"}
            if status == "unverified":
                warnings.append(f"coverage.{name} is unverified")
            continue
        records = declaration.get("evidence")
        checked = [_evidence(record, root) for record in records] if isinstance(records, list) else []
        artifacts = declaration.get("artifacts", [])
        missing = []
        if not isinstance(artifacts, list):
            errors.append(f"coverage.{name}.artifacts must be a list of paths")
            artifacts = []
        visual = declaration.get("kind") == "visual" or any(
            token in name.casefold() for token in ("figure", "image", "visual", "图")
        )
        if visual and not artifacts:
            missing.append("<visual source artifact not declared>")
        for artifact in artifacts:
            if root is None:
                missing.append(str(artifact))
                continue
            try:
                path = resolve_under_root(root, artifact, must_exist=False)
                if not path.is_file():
                    missing.append(str(artifact))
            except (AuditInputError, OSError) as exc:
                errors.append(f"coverage.{name} artifact rejected: {exc}")
                missing.append(str(artifact))
        passed = bool(checked) and all(item["status"] == "verified" for item in checked) and not missing
        results[name] = {"status": "passed" if passed else "unverified", "evidence_checks": checked,
                         "missing_artifacts": missing,
                         "validation_scope": "inspection_record_anchors_and_artifact_presence"}
        if any(item["status"] == "mismatch" for item in checked):
            errors.append(f"coverage.{name} evidence does not match the declared source")
        if not passed:
            warnings.append(f"coverage.{name} cannot pass without verifiable evidence and required artifacts")
    return errors, warnings, results


def validate_report(report: Mapping[str, Any], root: os.PathLike[str] | str | None = None) -> dict[str, Any]:
    """Validate evidence states, reviewer declarations, and optional coverage.

    No finding quota exists: ``{'issues': []}`` is valid. A valid report can
    contain explicitly unverified issues; it must not call missing audits passed.
    Declared cross-family metadata is checked for consistency, not authenticated.
    """
    result: dict[str, Any] = {"status": "invalid", "errors": [], "warnings": [], "issues": []}
    if not isinstance(report, Mapping):
        result["errors"].append("report must be an object")
        return result
    errors, warnings = result["errors"], result["warnings"]
    errors.extend(_probability_claims(report))
    issues = report.get("issues")
    if not isinstance(issues, list) or len(issues) > MAX_RECORDS:
        errors.append("issues must be a list within the record limit; an empty list is allowed")
        issues = []
    seen = set()
    for issue in issues:
        validation = validate_issue(issue, root=root)
        result["issues"].append(validation)
        issue_id = validation.get("id")
        if isinstance(issue_id, str):
            if issue_id in seen:
                errors.append(f"duplicate issue id: {issue_id}")
            seen.add(issue_id)
        errors.extend(f"{issue_id or 'issue'}: {message}" for message in validation["errors"])
        warnings.extend(f"{issue_id or 'issue'}: {message}" for message in validation["warnings"])
    reviewers = report.get("reviewers", [])
    if not isinstance(reviewers, list) or len(reviewers) > 64:
        errors.append("reviewers must be a list of at most 64 declarations")
        reviewers = []
    families, model_families, reviewer_ids = set(), {}, set()
    for reviewer in reviewers:
        if not isinstance(reviewer, Mapping) or any(not _nonempty(reviewer.get(key)) for key in ("id", "model", "family")):
            errors.append("each reviewer requires id, model, and declared family")
            continue
        identity = reviewer["id"].strip()
        if identity in reviewer_ids:
            errors.append(f"duplicate reviewer id: {identity}")
        reviewer_ids.add(identity)
        model, family = reviewer["model"].strip().casefold(), reviewer["family"].strip().casefold()
        if model in model_families and model_families[model] != family:
            errors.append(f"the same model cannot be declared as different families: {reviewer['model']}")
        model_families[model] = family
        families.add(family)
    independence = report.get("independence_claim", "none")
    if not isinstance(independence, str) or independence not in {"none", "multi_persona", "cross_family"}:
        errors.append("independence_claim must be none, multi_persona, or cross_family")
    if independence == "cross_family":
        if len(families) < 2 or len(model_families) < 2:
            errors.append("cross_family requires different declared model families; same-model personas are not independent")
        else:
            warnings.append("Model-family identities are declared metadata and were not authenticated by this offline check.")
    if "coverage" in report:
        coverage_errors, coverage_warnings, coverage = _validate_coverage(report["coverage"], root)
        errors.extend(coverage_errors)
        warnings.extend(coverage_warnings)
        result["coverage"] = coverage
    unresolved = any(item["status"] == "unverified" for item in result["issues"])
    unresolved |= any(item["status"] == "unverified" for item in result.get("coverage", {}).values())
    result["status"] = "invalid" if errors else "unverified" if unresolved else "valid"
    return result


def recheck_issue(issue: Mapping[str, Any], revision_evidence: Mapping[str, Any] | None,
                  check: Mapping[str, Any] | None,
                  root: os.PathLike[str] | str | None = None) -> dict[str, Any]:
    """Close only after original evidence, revision evidence, and a passing record.

    Return closed/open/unverified plus the complete validation. Caller-owned
    inputs are never mutated. A bare author claim or a missing check stays open.
    """
    if not isinstance(issue, Mapping):
        raise AuditInputError("issue must be an object")
    candidate = dict(issue, status="closed", revision_evidence=revision_evidence, check=check)
    validation = validate_issue(candidate, root=root)
    effective = validation["effective_status"]
    return {"status": "closed" if validation["status"] == "valid" and effective == "closed"
            else "open" if effective == "confirmed" else "unverified",
            "issue_id": issue.get("id"), "validation": validation}
