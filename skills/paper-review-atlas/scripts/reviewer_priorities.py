"""Reviewer-priority routing from explicit evidence records; no LLM or network."""
from audit_checks import AuditInputError

RULES = {f"CFX{i:02d}" for i in range(17, 23)}

def choice(facts, key, values):
    value = facts.get(key)
    if not isinstance(value, str) or value not in values:
        raise AuditInputError(key + " must be one of " + ", ".join(sorted(values)))
    return value

def flag(facts, key):
    value = facts.get(key)
    if type(value) is not bool:
        raise AuditInputError(key + " must be a boolean")
    return value

def policy(rule, facts):
    if not isinstance(rule, str) or rule not in RULES:
        raise AuditInputError("unknown reviewer-priority rule")
    if not isinstance(facts, dict):
        raise AuditInputError("facts must be an object")
    result = {"rule": rule, "basis": "reviewer-supplied facts; conditional routing, not a manuscript verdict"}
    if rule == "CFX17":
        profile = choice(facts, "profile", {"importance_selective", "soundness_only", "unknown"})
        verified = flag(facts, "policy_verified")
        criterion = choice(facts, "criterion", {"importance", "validity"})
        action = ("assess_validity" if criterion == "validity" else
                  "retrieve_venue_policy" if not verified or profile == "unknown" else
                  "no_importance_veto" if profile == "soundness_only" else "assess_venue_fit")
    elif rule == "CFX18":
        claim = choice(facts, "claim_type", {"mechanism", "performance"})
        effect = flag(facts, "effect_supported")
        discriminating = flag(facts, "discriminating_evidence")
        action = ("request_effect_evidence" if not effect else
                  "test_mechanism_or_narrow_claim" if claim == "mechanism" and not discriminating else
                  "assess_mechanism_support" if claim == "mechanism" else "retain_measured_effect")
    elif rule == "CFX19":
        purpose = choice(facts, "request_purpose", {"current_claim", "new_scope", "already_resolved", "unspecified"})
        narrower = flag(facts, "supported_narrower_claim")
        action = ({"new_scope": "optional_extension", "already_resolved": "close_resolved_request",
                   "unspecified": "specify_evidence_gap"}.get(purpose) or
                  ("test_or_narrow_claim" if narrower else "minimum_sufficient_test"))
    elif rule == "CFX20":
        basis = choice(facts, "objection_basis", {"module_count", "method_name", "sota_rank", "located_prior_result"})
        verified = flag(facts, "prior_result_verified")
        action = ("build_contribution_map" if basis != "located_prior_result" else
                  "assess_incremental_contribution" if verified else "verify_prior_result")
    elif rule == "CFX21":
        frozen = flag(facts, "reports_frozen")
        isolated = flag(facts, "contexts_isolated")
        shared = flag(facts, "shared_concerns_before_freeze")
        origin = choice(facts, "finding_origin", {"reviewer", "audit"})
        count = facts.get("reports_raising_concern")
        if type(count) is not int or not 0 <= count <= 1000:
            raise AuditInputError("reports_raising_concern must be an integer in [0, 1000]")
        action = ("freeze_before_synthesis" if not frozen else
                  "separate_audit_finding" if origin == "audit" else
                  "label_shared_context_views" if not isolated or shared else
                  "record_convergent_reports" if count >= 2 else "record_nonconsensus_finding")
        result["statistical_independence_established"] = False
    else:
        access = choice(facts, "source_access", {"full_text", "transcript", "title_only", "unavailable"})
        conflict = flag(facts, "conflicts_with_verified_policy")
        scope = choice(facts, "advice_scope", {"general", "venue_specific", "style_preference"})
        action = ("pending_source_no_attribution" if access in {"title_only", "unavailable"} else
                  "use_verified_policy" if conflict else
                  "optional_style" if scope == "style_preference" else "conditional_review_rule")
    return {**result, "action": action}
