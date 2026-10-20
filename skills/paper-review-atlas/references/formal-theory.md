# Equations, algorithms, and theoretical claims

Use this protocol for formal results, technical derivations, algorithm specifications, and mathematical consistency. Match rigor to the claim and article type.

## Contents

- Establish the formal object
- Audit notation and equations
- Check proofs and assumptions
- Compare theory with implementation and evidence
- Report bounded conclusions

## Establish the formal object

Inventory definitions, assumptions, propositions, lemmas, theorems, corollaries, algorithms, and complexity/convergence claims.
Record the exact result being claimed and its domain.
Distinguish a formal theorem, heuristic derivation, illustrative argument, empirical observation, and conjecture.
Do not demand a theorem for every engineering explanation; do demand correct labeling of the evidence type.
Identify which central conclusions depend on each result.
Build a compact dependency map from assumptions through lemmas to the final claim.
Check whether an imported result is stated accurately and whether its conditions apply here.
For a crucial external theorem, inspect the original statement or a reliable primary source; otherwise mark the dependency unverified.

## Audit notation and equations

Check that each symbol is defined before or near meaningful use and has a consistent role.
Distinguish vectors, matrices, sets, distributions, random variables, realizations, estimators, and parameters.
Check indices, summation limits, dimensions, shapes, units, domains, and boundary conditions.
Check whether an overloaded symbol can be understood unambiguously or hides a different quantity.
Verify signs, transpose/conjugate operations, normalization constants, denominators, logarithm bases, and inequality direction.
Check the domain of logarithms, divisions, inverses, roots, expectations, and conditional probabilities.
Inspect omitted conditions such as positivity, nonzero denominators, invertibility, measurability, integrability, boundedness, or finite support when the argument needs them.
Check whether probabilities are normalized and whether losses/scores have the direction described in text.
Distinguish a strict inequality from a non-strict one and an almost-sure claim from one in expectation.
Track whether equations express definitions, exact equalities, approximations, bounds, or asymptotic relationships.
Require an explanation for approximation regimes that matter to the conclusion.
Check equation numbering, references, and correspondence with variable names in pseudocode and code.
Do not infer a mathematical error from PDF text extraction when the rendered equation is correct.

## Check proofs and assumptions

Read the statement before the proof: are all quantifiers, domains, probability levels, constants, and conditions explicit?
Check the order of quantifiers; “for each task there exists a policy” differs from “one policy works for all tasks.”
Check whether existence is being mistaken for uniqueness, constructibility, efficiency, or practical attainability.
Verify that intermediate lemmas are proved or properly invoked.
Look for circular dependence, unstated strengthening, changing assumptions, and steps that only hold in special cases.
For induction, inspect base cases, induction hypothesis, transition, and the allowed index range.
For contradiction, confirm that the negated statement is the actual target.
For optimization, check feasibility, differentiability/subgradients, convexity assumptions, constraint qualifications, local/global distinctions, and attained versus infimum values as relevant.
For convergence, identify the notion of convergence, limiting object, initialization, step schedule, noise assumptions, and finite versus asymptotic statement.
For probabilistic bounds, track independence, conditioning, adaptivity, union bounds, distributional assumptions, and whether constants depend on the variables being bounded.
For adaptive data analysis, check whether reuse of data changes the applicability of a concentration or generalization argument.
For computational complexity, state input size, operation model, worst/average/amortized case, preprocessing, storage, and oracle/subroutine costs.
For multiple size parameters, identify the limiting variable and state which other parameters are fixed, bounded, or grow with it.
Compare relevant growth regimes separately when their relationship changes the conclusion; do not silently treat an architectural dimension as constant in one method and variable in the other.
Distinguish an upper bound, a lower bound, a tight order, and an explicit cost expression. Two loose Big-O upper bounds alone do not establish which implementation is faster or which true cost grows faster.
Use justified tight bounds, a valid upper/lower-bound separation, or explicit cost expressions for an asymptotic ordering. Track the assumptions under which a ratio, limit, or inequality supports that ordering.
For example, costs of tight orders `Θ(nk)` and `Θ(n log n)` have different comparisons when `k` is fixed, proportional to `log(n)`, or grows faster than `log(n)`; equal orders alone leave constants and practical performance unresolved.
Keep an asymptotic claim separate from a finite-workload crossover. Tie a reported practical crossover to actual measurements and their hardware, implementation, memory, precision, and workload conditions; label an analytical crossover as a prediction under its cost model.
Do not describe a polynomial algorithm as practical without considering the actual exponent, constants, and input regime.
Check whether a claimed speedup compares equivalent accuracy, approximation quality, or task success.

Try simple boundary cases and counterexamples:

- Empty/singleton sets where permitted.
- Zero, equal, degenerate, extreme, or repeated values.
- Ties, nonunique optima, singular matrices, and disconnected graphs.
- Minimal horizon and increasing horizon.
- Perfect/noisy/adversarial observations within the stated assumptions.
- Limit cases where a claimed strict improvement should become equality.

A counterexample invalidates a claim only if it satisfies every relevant assumption.
If it violates an assumption, it may reveal a practical limitation but is not a proof failure.
Do not dismiss a valid counterexample because the tested benchmarks do not exhibit it.
Do not assert a proof is complete merely because no counterexample was found.

## Compare theory with implementation and evidence

Check whether the implemented algorithm matches the theorem's object: approximation, clipping, finite precision, stochastic sampling, early stopping, and heuristics can alter guarantees.
Identify assumptions made for theory that the experiments do not enforce.
A theorem may remain correct while its practical relevance is limited; report these separately.
An empirical improvement does not prove a universal convergence or optimality claim.
A formal bound may explain a trend without predicting an exact numerical result; evaluate the actual stated claim.
Check whether plots illustrating a theorem use values and domains within its assumptions.
For derived metrics or custom losses, verify that their algebraic behavior matches the interpretation in prose.
Distinguish correctness of a mathematical expression from validity of its use as a scientific model.

Symbolic algebra, numeric evaluation, and small exhaustive searches can provide useful diagnostics when host tools are available.
Record tool version, expression, assumptions, domain, input values, precision, and observed output for executed checks.
Do not claim an executable proof assistant or formal verification was used unless it actually was.
Symbolic simplification under hidden assumptions is not a universal proof.
Finite enumeration proves only the enumerated finite domain unless a separate argument extends it.
Numerical agreement can miss singular cases, instability, quantifier errors, and measure-zero exceptions.
Do not insert generated proof steps that have not been checked into an author manuscript as established mathematics.

## Report bounded conclusions

For each finding, quote the exact statement or step and identify the violated condition or missing justification.
Explain the consequence: notation repair, local derivation gap, weaker guarantee, invalid theorem, or unknown applicability.
Provide a concrete remedy: add the missing assumption, supply a lemma, fix a derivation, restrict the result, replace the proof, or relabel a heuristic.
Do not automatically weaken a valid result because it is ambitious; preserve its full justified scope.
Do not inflate a harmless notation typo into a fatal theoretical issue when the intended statement and proof remain clear.
Conversely, a one-character inequality change can be major if it reverses the central result.
For an unverified proof gap, state exactly which inference cannot yet be justified and what would close it.
For a claimed counterexample, include its values, assumptions check, calculation, and contradiction.
Close a finding only after inspecting the revised statement, all affected dependencies, and the repaired reasoning.
Record whether the work was a human/model-assisted proof review, numerical diagnostic, symbolic computation, or actual machine-checked proof.
