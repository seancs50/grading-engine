# Family Spec: `ax + b = c` Linear Equation, v1

## 1. FAMILY IDENTITY

### Family ID

`linear_equation_ax_plus_b_eq_c__int_prompt__x_only__v1`

### Title

Solve one one-variable linear equation of canonical prompt form `ax + b = c`.

### Exact Boundary

This family MUST apply if and only if all conditions below are true:

- the surface prompt form contains exactly one equation
- the prompt variable is exactly lowercase `x`
- normalization of the surface prompt form yields the canonical normalized form `a*x + b = c`
- `a`, `b`, and `c` are exact signed integers
- `a != 0`
- `|a| > 1`
- `b != 0`
- the equation has exactly one solution over the reals
- the prompt contains no other variable, parameter, function, relation, or diagram dependency

This family MUST NOT be selected if any condition above is false.

### Allowed Surface Forms

The surface prompt form MUST match one of the forms below and no other form:

- `ax + b = c`
- `ax - d = c`, where normalization sets `b = -d`
- `-ax + b = c`
- `-ax - d = c`

### Canonical Normalized Form

The canonical normalized form for this family MUST be exactly:

`a*x + b = c`

with exact normalized signed integers `a`, `b`, and `c`.

Normalization MUST occur before family instance identity is determined.

The canonical family instance is the exact normalized tuple `(a, b, c)` together with variable `x`.

Two prompts are the same family instance if and only if they normalize to the same exact `(a, b, c)` tuple and the same exact variable `x`.

### Explicit Out-of-Scope Prompt Forms

The prompt is out of scope, and this family MUST fail closed, if it contains any of the forms below:

- `a = 0`
- `|a| = 1`
- `b = 0`
- fractions or decimals in the prompt coefficients or constants
- variable terms on both sides
- identities or contradictions
- inequalities
- simultaneous equations
- fractions with the variable in a denominator
- brackets that expand to create the equation
- contextual word problems
- diagrams or labels required for interpretation
- reordered prompt statements such as `b + ax = c`, `c = ax + b`, or `ax = c - b`

### Supported Student Route

A supported student route in this family MUST be exactly one of the route definitions in section 3 and no other route.

### Unsupported Route

An unsupported route is any parseable route that is mathematically meaningful but not encoded in section 3.

The following routes are explicitly unsupported and MUST escalate with `escalate.unsupported_route` when atom evaluation would require them:

- divide first from the prompt state
- move the variable term to the right side
- multiply first by a reciprocal
- use balancing by hidden cancellation without an exact parseable source-target pair
- use a transposition idiom that does not reduce to an exact supported state transition
- jump from the prompt state directly to a simplified numeric final answer

### Unsupported Notation

The following notation is explicitly unsupported in this family and MUST escalate with `escalate.unsupported_notation` when atom evaluation would require it:

- any variable symbol other than exact lowercase `x`
- decimal final answers
- prose-only method descriptions
- arrow-only or cancellation-only working that does not define exact source and target states
- direct grouped-solve forms that do not use exact slash or exact fraction-bar division

### Unsupported Evidence Shape

The following evidence shapes are explicitly unsupported in this family:

- an answer box or detached final value with no parseable transition from an earlier equation state
- unbound scratch fragments that cannot be attached to one ordered solution path
- a line that omits the equality relation
- a line that combines more than one incompatible equation state into one evidence item

## 2. CANONICAL QUESTION FORM

### Canonical Form

The canonical prompt state for this family MUST be:

`a*x + b = c`

with exact normalized integer values `a`, `b`, and `c`.

### Normalization Function

The normalization function for this family MUST take one surface equation string as input and MUST return exactly one tuple `(a, b, c)` as output if and only if the surface prompt form matches one allowed surface form from section 1.

The normalization function MUST apply exactly the rules below and no other transformation:

- `ax + b = c` -> `(a, b, c)`
- `ax - d = c` -> `(a, -d, c)`
- `-ax + b = c` -> `(-a, b, c)`
- `-ax - d = c` -> `(-a, -d, c)`

The normalization function MUST NOT perform any transformation beyond sign normalization.

The normalization function MUST reject:

- any reordering such as `b + ax = c`
- any swapped equality orientation such as `c = ax + b`
- any algebraic rewriting such as `ax = c - b`
- any expansion, factorization, simplification, or coefficient inference beyond the exact sign normalization rules above

### Variable Assumptions

- the only supported unknown is exact lowercase `x`
- the variable is scalar and real
- no other symbol may function as an unknown in the bound solution path

### Coefficient and Constant Constraints

- `a` MUST be an exact signed integer with `a != 0` and `|a| > 1`
- `b` MUST be an exact signed integer with `b != 0`
- `c` MUST be an exact signed integer
- negative coefficients and negative constants are allowed
- rational and decimal prompt coefficients or constants are forbidden

### Prompt-Level Equivalence

Prompt-level reordered equation statements are forbidden.

The family MAY normalize only prompt sign syntax of the forms `+ b` and `- d` into the canonical signed integer `b`.

No other prompt-level equivalence is allowed.

## 3. ACCEPTED SOLUTION ROUTES

This family supports exactly two routes.

### Route `R1`: Isolate Constant, Then Divide

#### Route ID

`R1_isolate_constant_then_divide`

#### Route Description

The student removes the free constant from the variable side and then divides by the original coefficient.

#### Ordered Expected Transformation Pattern

The route MUST follow this exact ordered pattern:

1. canonical prompt state `a*x + b = c`
2. isolated-term state `a*x = k`, where `k = c - b`
3. final solution state `x = k / a` or an exact accepted equivalent final value form from section 7

#### Visible-Method Requirements

- step 1 MUST appear as one parseable transition from the canonical prompt state to one isolated-term state
- step 2 MUST appear as one parseable transition from one isolated-term state to one final solution state
- each credited transition MUST have an exact source state and exact target state on one bound solution path
- the operation symbol MAY be implicit if and only if the source-target pair uniquely determines the supported transformation

#### Compressed-Working Rules

The route MAY compress within one step if and only if the compressed transition still matches one exact supported step:

- prompt state directly to the isolated-term state is accepted for step 1
- isolated-term state directly to the final solution state is accepted for step 2

The route MUST NOT compress across both steps into one direct prompt-to-numeric-final transition.

#### Unsupported Variants

The following route variants are unsupported and MUST escalate with `escalate.unsupported_route`:

- prompt state to `x + b/a = c/a`
- prompt state to `x = s` with no denominator or grouped inverse-constant expression visible
- prompt state to any state that changes the coefficient before the constant is removed

### Route `R2`: Direct Grouped Solve

#### Route ID

`R2_direct_grouped_solve`

#### Route Description

The student moves directly from the canonical prompt state to an exact grouped final solve form that visibly encodes both removing the constant and dividing by the original coefficient.

#### Ordered Expected Transformation Pattern

The route MUST follow this exact one-transition pattern:

1. canonical prompt state `a*x + b = c`
2. grouped final state `x = q`

The target `q` MUST be exactly one of the forms below:

- `(c - b) / a`
- `k / a`, where `k` is the exact canonical integer value `c - b`

If the prompt surface form was `ax - d = c`, the grouped numerator MAY appear as `c + d`, but that surface form MUST normalize to the same exact canonical family-structured representation as `c - b`.

#### Visible-Method Requirements

- the target state MUST keep the denominator `a` visible
- if the numerator is unevaluated, the numerator MUST be explicitly grouped
- the grouped form MUST make both the inverse-constant step and the division step visible in one exact parseable state
- grouped expressions MUST use parentheses whenever parentheses are required to preserve one unique parse under standard operator precedence

#### Compressed-Working Rules

This route is the only accepted cross-step compressed form in this family.

This route MUST NOT accept a target state that removes the visible denominator or hides the grouped inverse-constant structure.

#### Unsupported Variants

The following variants are unsupported and MUST escalate with `escalate.unsupported_route` or `escalate.multiple_interpretations` as stated:

- `x = s` directly from the prompt state, even when `s` is correct
- `x = c - b / a`
  This form MUST escalate with `escalate.multiple_interpretations` if parsing yields more than one valid interpretation that changes the atom trace.
- `x = (c + b) / a` when the prompt requires `c - b`
- `x = (c - b) * (1/a)`
- any direct grouped form that replaces exact integer arithmetic with decimals

## 4. MARK ATOM SET

This family contains exactly three atoms and no `B` atoms.

### Family Evidence Predicates Used by Dependencies

`p.ft_isolated_source_present` is true if and only if all conditions below are true on the bound solution path:

- there is exactly one earlier parseable state `Sft` of form `a*x = k_ft`
- the coefficient of `x` in `Sft` is the exact original prompt coefficient `a`
- `k_ft` is an exact scalar value
- `Sft` is produced by a parseable transition OR a standalone equation state that is uniquely attachable to the canonical prompt state as an isolated-term form
- `k_ft != c - b`

If no transition is present, `Sft` MUST still be uniquely derivable from the canonical prompt form as one isolated-term state with unchanged coefficient `a`.

If more than one candidate `Sft` exists and they change the atom outcome, primary reason code, bound path, or explanation evidence references, the affected atom MUST escalate with `escalate.multiple_interpretations`.

### Path Selection and Binding Rules

Path binding in this family MUST be deterministic and MUST apply the rules below in order:

1. if multiple candidate paths exist, choose the path with the earliest valid `M1` candidate
2. if more than one candidate path still remains, choose the path with the earliest final valid `A1` state
3. if more than one candidate path still remains after rules 1 and 2, the affected atom MUST escalate with `escalate.multiple_interpretations`

Correction overrides earlier path segments. If the student visibly corrects earlier work by restating the canonical prompt state or one correct isolated-term state and then continues, later atoms MUST bind to that corrected continuation if and only if that continuation is uniquely bindable on one candidate path.

FT MUST apply only within one single bound path.

### Atom `M1`

- `id`: `M1`
- `type`: `M`
- `description`: perform the supported constant-removal method from the canonical prompt state
- `dependencies`: `none`
- `path binding rule`: bind to the unique path containing the earliest canonical prompt state and the earliest later transition from that state that is a candidate for `R1` step 1 or `R2`
- `evidence rule`: one parseable transition from the canonical prompt state either to an isolated-term state for `R1` or to one grouped final state for `R2`
- `success predicate`: `M1` is awarded if and only if one of the conditions below is true:
- `success predicate`: for `R1`, the transition target is exactly `a*x = c - b` after canonical integer evaluation
- `success predicate`: for `R2`, the transition target is exactly `x = (c - b) / a` or `x = k / a` with visible denominator `a` and exact canonical `k = c - b`
- `withhold predicates`: `withhold.no_visible_method` if the path contains only a final answer state or other state-only evidence with no supported transition from the prompt state
- `withhold predicates`: `withhold.invalid_method` if the transition is parseable as an `R1` or `R2` candidate but the algebra or arithmetic is invalid
- `withhold predicates`: `withhold.insufficient_evidence` if no parseable supported transition exists and no escalation predicate is true
- `escalation predicates`: `escalate.unsupported_route` if the shown route is mathematically meaningful but not `R1` or `R2`
- `escalation predicates`: `escalate.unsupported_notation` if the route would require unsupported notation from section 1
- `escalation predicates`: `escalate.ambiguous_parse`, `escalate.multiple_interpretations`, and `escalate.contradictory_work` apply exactly as defined in `spec.md`
- `FT policy`: `disallowed`
- `explanation requirements`: cite the canonical prompt state reference, the transition reference, the target state reference, the route id used, and the exact primary reason code

### Atom `M2`

- `id`: `M2`
- `type`: `M`
- `description`: solve for `x` by dividing by the original coefficient on a supported direct or carried source
- `dependencies`: `M1 OR p.ft_isolated_source_present`
- `path binding rule`: bind to the same path as `M1`; if `M1` is awarded by `R1`, bind to the earliest later transition from the isolated-term state to a final solution state; if `M1` is awarded by `R2`, bind to the same direct grouped-solve transition; if `M1` is not awarded and `p.ft_isolated_source_present` is true, bind to the unique FT source state and the earliest later transition from that source to a final solution state
- `evidence rule`: one parseable transition either from an isolated-term state `a*x = k` to a final solution state `x = q`, or the one direct grouped-solve transition from `R2`
- `success predicate`: `M2` is awarded if and only if one of the conditions below is true:
- `success predicate`: for `R1`, the transition divides both sides of one isolated-term source state by the exact original coefficient `a` and the target isolates `x`
- `success predicate`: for `R2`, the grouped final state visibly preserves the exact denominator `a`
- `success predicate`: for FT, the source state is the unique `Sft` from `p.ft_isolated_source_present` and the target is exactly derivable from `Sft` by dividing both sides by the original coefficient `a`
- `withhold predicates`: `withhold.unmet_dependency` if neither `M1` nor `p.ft_isolated_source_present` is true
- `withhold predicates`: `withhold.invalid_method` if the division step is parseable on a supported route but mathematically invalid
- `withhold predicates`: `withhold.insufficient_evidence` if the dependency is satisfied but no parseable supported division transition exists
- `withhold predicates`: `withhold.follow_through_not_permitted` if the step would require carrying more than one earlier erroneous source state or a source state that is not of exact form `a*x = k_ft`
- `escalation predicates`: `escalate.unsupported_route` if the shown route requires divide-first or another unencoded route
- `escalation predicates`: `escalate.unsupported_notation` if the route would require unsupported notation from section 1
- `escalation predicates`: `escalate.unresolved_follow_through_source` if the engine cannot determine whether the student is using the unique FT source or a corrected source
- `escalation predicates`: `escalate.ambiguous_parse`, `escalate.multiple_interpretations`, and `escalate.contradictory_work` apply exactly as defined in `spec.md`
- `FT policy`: allowed only from one earlier unique source state satisfying `p.ft_isolated_source_present`
- `explanation requirements`: cite the source state reference, the transition reference, the target state reference, the dependency verdict, the FT source reference when FT is used, the route id used, and the exact primary reason code

### Atom `A1`

- `id`: `A1`
- `type`: `A`
- `description`: give the correct final solution value for `x` in an accepted final form
- `dependencies`: `M2`
- `path binding rule`: bind to the same path and the same final target state used by `M2`
- `evidence rule`: one final parseable state from the `M2` evidence that isolates `x`
- `success predicate`: `A1` is awarded if and only if one of the conditions below is true:
- `success predicate`: when `M2` is awarded directly, the final state is exactly equal to the canonical solution value `(c - b) / a` under the accepted final-form equivalence rules in section 7
- `success predicate`: when `M2` is awarded by FT, the final state is exactly equal to the carried solution value `k_ft / a` under the accepted final-form equivalence rules in section 7
- `withhold predicates`: `withhold.unmet_dependency` if `M2` is not awarded
- `withhold predicates`: `withhold.incorrect_result` if the final state is parseable and isolated but not equal to the exact required final value for the direct or FT case
- `escalation predicates`: `escalate.unsupported_notation` if the final state uses unsupported notation from section 1
- `escalation predicates`: `escalate.ambiguous_parse`, `escalate.multiple_interpretations`, and `escalate.contradictory_work` apply exactly as defined in `spec.md`
- `FT policy`: allowed if and only if `M2` is awarded by FT from one unique FT source state
- `explanation requirements`: cite the final state reference, the dependency verdict, the FT source reference when FT is used, the exact primary reason code, and the exact accepted-form rule used

## 5. DEPENDENCY GRAPH

The dependency graph for this family is exact and acyclic:

- `M1`: `none`
- `M2`: `M1 OR p.ft_isolated_source_present`
- `A1`: `M2`

### Dependency Consequences

- `A1` MUST NOT be awarded from answer-only evidence
- `A1` MUST be blocked whenever `M2` is not awarded
- `M2` MUST NOT be awarded from answer-only evidence
- `M2` MAY be awarded by FT when `M1` is not awarded if and only if `p.ft_isolated_source_present` is true and the later division step is valid

## 6. FOLLOW-THROUGH RULES FOR THIS FAMILY

This family permits FT only in one narrow case.

### Atoms That Permit FT

- `M1`: FT disallowed
- `M2`: FT allowed only from one unique earlier isolated-term source state `a*x = k_ft`
- `A1`: FT allowed only when `M2` is awarded by FT

### Allowed FT Source

The only allowed FT source is one exact earlier state `Sft` on the bound path with form:

`a*x = k_ft`

where:

- the coefficient of `x` is the exact original prompt coefficient `a`
- the variable is exact lowercase `x`
- the source is parseable
- the source is incorrect relative to the canonical value `c - b`
- the source is unique on the bound path for the atom being evaluated

### Consistent Carried Error

A carried error is consistent in this family if and only if all conditions below are true:

- the only incorrect component is the right-side scalar value `k_ft`
- the left side remains exactly `a*x`
- the original coefficient `a` is unchanged
- the later step divides by the same exact `a`

### Creditable Later FT Transformations

Under FT, the following later transformations are creditable and no others:

- `a*x = k_ft` to `x = k_ft / a`
- `a*x = k_ft` to an exact accepted equivalent final rational value of `k_ft / a`

### FT Break Conditions

The following conditions break FT and MUST withhold or escalate exactly as stated:

- if the carried source changes the coefficient of `x`, `M2` MUST resolve to `withhold.unmet_dependency`
- if the carried source changes the variable symbol, the affected atom MUST resolve to `escalate.unsupported_notation`
- if the later step requires carrying more than one erroneous source state, `M2` MUST resolve to `withhold.follow_through_not_permitted`
- if the student visibly corrects the earlier error by restating the canonical prompt state or one correct isolated-term state and then continues, later atoms MUST evaluate on the corrected state and MUST NOT use FT
- if the engine cannot determine whether the student is using the carried source or a corrected source, the affected atom MUST resolve to `escalated` with `escalate.unresolved_follow_through_source`

### Direct Grouped Solve and FT

`R2` MUST NOT be used as an FT route.

If a later grouped-solve state would require FT, the affected atom MUST resolve to `withhold.follow_through_not_permitted` or `escalated` with `escalate.unresolved_follow_through_source` according to the exact FT break condition above.

## 7. EQUIVALENCE AND FORM RULES

Anything not explicitly allowed in this section MUST be treated as incorrect, unsupported, or escalated under `spec.md`.

### Family-Wide Canonical Meaning

All accepted states in this family MUST normalize to canonical family-structured representations over exact integers and exact rational values.

Decimal normalization is not supported in this family.

The parser for this family MUST enforce standard operator precedence.

`x = (c - b) / a` MUST be accepted as one valid grouped expression form.

`x = k / a` MUST be accepted as one valid grouped expression form.

`x = c - b / a` MUST resolve to `escalated` with `escalate.multiple_interpretations`.

Any form that yields more than one valid parse tree and changes the atom outcome, primary reason code, bound path, or explanation trace MUST resolve to `escalated` with `escalate.multiple_interpretations`.

### Atom-Scoped Rules for `M1`

- algebraic equivalence allowed: no
- ordering equivalence allowed: no
- sign normalization allowed: yes, for canonical signed integers only
- factor normalization allowed: no
- exact alternate representations allowed: yes, only between `x = (c - b)/a` and `x = k/a` in `R2`, where `k` is the exact integer `c - b`
- notation variants allowed: exact `+` and exact `-` sign forms only
- domain restrictions: none beyond the family boundary
- rounding or precision requirements: exact only

### Atom-Scoped Rules for `M2`

- algebraic equivalence allowed: limited
- ordering equivalence allowed: no
- sign normalization allowed: yes, one factor of `-1` MAY move between numerator and denominator in one exact rational quotient
- factor normalization allowed: no
- exact alternate representations allowed: yes, only between `x = k/a` and one exact equivalent isolated final rational value form
- notation variants allowed: exact slash or exact fraction-bar division only
- domain restrictions: none beyond the family boundary
- rounding or precision requirements: exact only

### Atom-Scoped Rules for `A1`

- algebraic equivalence allowed: yes, exact rational equivalence only
- ordering equivalence allowed: yes, only between `x = q` and `q = x`
- sign normalization allowed: yes
- factor normalization allowed: yes, exact rational reduction or unreduced exact rational form are both accepted
- exact alternate representations allowed: yes, integer form and exact rational form are both accepted when mathematically equal
- notation variants allowed: exact equality with isolated `x` only
- domain restrictions: none beyond the family boundary
- rounding or precision requirements: exact only

### Unsimplified Intermediate and Final Forms

- for `R1` step 1, the isolated-term state MUST be numerically evaluated to exact integer `k`; unevaluated `a*x = c - b` is not supported in `R1`
- for `R2`, the grouped numerator MAY be unevaluated or evaluated, but the denominator `a` MUST remain visible
- for `A1`, an unreduced exact rational final answer is accepted
- for `A1`, a decimal final answer is not accepted

### Cancellation and Compression

- compression is accepted only in the exact route forms from section 3
- hidden cancellation, transposition shorthand, or mental arithmetic with no exact supported state transition is not accepted

## 8. WITHHOLD VS ESCALATE DECISIONS

The following decision map is exact for common family cases.

### Correct Final Answer With No Visible Method

- `M1`: `withheld` with `withhold.no_visible_method`
- `M2`: `withheld` with `withhold.unmet_dependency`
- `A1`: `withheld` with `withhold.unmet_dependency`

### Invalid Algebraic Move On Supported Route

- the affected method atom: `withheld` with `withhold.invalid_method`
- downstream atoms: `withheld` with `withhold.unmet_dependency`, unless a later FT rule explicitly permits award

### Mathematically Plausible But Unsupported Route

- each affected atom: `escalated` with `escalate.unsupported_route`

### Ambiguous Parse

- each affected atom: `escalated` with `escalate.ambiguous_parse`

### Contradictory Work On The Bound Path

- an atom whose cited evidence or dependency source is contradictory: `escalated` with `escalate.contradictory_work`
- an atom whose evidence and dependencies remain isolated and deterministic: resolve normally

### Multiple Candidate Paths

- each affected atom: `escalated` with `escalate.multiple_interpretations`

### Skipped Intermediate Step With One Unique Supported Interpretation

- if the step matches `R2` exactly, the affected atoms resolve normally
- if the step matches one exact `R1` transition exactly, the affected atom for that step resolves normally

### Skipped Intermediate Step With Multiple Valid Interpretations

- each affected atom: `escalated` with `escalate.multiple_interpretations`

### Corrected Earlier Error

- later atoms MUST bind to the corrected continuation if the correction is explicit and uniquely bound
- later atoms MUST NOT use FT after an explicit correction state

### Answer Obtained From One Carried Wrong Intermediate

- `M2`: `awarded` with `award.follow_through` if and only if the carried source is the unique allowed FT source and the division is valid
- `A1`: `awarded` with `award.follow_through` if and only if the final value equals the carried value `k_ft / a`

### Hidden Switch From Wrong Intermediate To Correct Canonical Result

- each affected atom: `escalated` with `escalate.unresolved_follow_through_source` if the engine cannot determine whether the student corrected or carried the earlier error

## 9. EXPLANATION TRACE REQUIREMENTS

Each family explanation MUST satisfy `spec.md` and the family-specific requirements below.

### `M1`

The explanation MUST cite:

- the canonical prompt state reference
- the transition reference used for the decision
- the target state reference
- the route id `R1_isolate_constant_then_divide` or `R2_direct_grouped_solve`
- the exact primary reason code

### `M2`

The explanation MUST cite:

- the source state reference
- the transition reference used for the decision
- the target state reference
- the dependency verdict
- the FT source reference when FT is used
- the exact primary reason code

### `A1`

The explanation MUST cite:

- the final state reference
- the dependency verdict
- the FT source reference when FT is used
- the exact accepted-form rule used
- the exact primary reason code

## 10. GOLDEN TESTS

### Pseudo-Format

The pseudo-format in this section is normative for the golden tests in this file.

- `path pN:` starts one ordered candidate path
- `S#:` defines one state
- `T#:` defines one transition from one named source state to one named target state
- `A#:` defines one assertion

Each test below uses exactly that format.

### Test `T01_perfect_r1`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 3x = 6
  T2: S1 -> S2
  S2: x = 2
```

#### Expected Atom Outcomes

- `M1`: `awarded`, primary reason `award.direct`, evidence `S0,T1,S1`
- `M2`: `awarded`, primary reason `award.direct`, evidence `S1,T2,S2`
- `A1`: `awarded`, primary reason `award.direct`, evidence `S2`

#### Expected Total

`3`

#### Expected Explanation-Critical References

- `M1` MUST cite `S0,T1,S1`
- `M2` MUST cite `S1,T2,S2`
- `A1` MUST cite `S2`

### Test `T02_perfect_r2_grouped`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: x = (11 - 5) / 3
```

#### Expected Atom Outcomes

- `M1`: `awarded`, primary reason `award.direct`, evidence `S0,T1,S1`
- `M2`: `awarded`, primary reason `award.direct`, evidence `S0,T1,S1`
- `A1`: `awarded`, primary reason `award.direct`, evidence `S1`

#### Expected Total

`3`

#### Expected Explanation-Critical References

- all atoms MUST cite `S1`
- `M1` and `M2` MUST cite route id `R2_direct_grouped_solve`

### Test `T03_answer_only_no_method`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  S1: x = 2
```

#### Expected Atom Outcomes

- `M1`: `withheld`, primary reason `withhold.no_visible_method`, evidence `S0,S1`
- `M2`: `withheld`, primary reason `withhold.unmet_dependency`, evidence `S1`
- `A1`: `withheld`, primary reason `withhold.unmet_dependency`, evidence `S1`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- `M1` MUST cite `S0,S1`
- `M2` MUST cite dependency failure
- `A1` MUST cite dependency failure

### Test `T04_ft_success_from_wrong_isolated_rhs`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 3x = 5
  T2: S1 -> S2
  S2: x = 5/3
```

#### Expected Atom Outcomes

- `M1`: `withheld`, primary reason `withhold.invalid_method`, evidence `S0,T1,S1`
- `M2`: `awarded`, primary reason `award.follow_through`, evidence `S1,T2,S2`, FT source `S1`
- `A1`: `awarded`, primary reason `award.follow_through`, evidence `S2`, FT source `S1`

#### Expected Total

`2`

#### Expected Explanation-Critical References

- `M2` MUST cite FT source `S1`
- `A1` MUST cite FT source `S1`

### Test `T05_ft_denied_changed_coefficient`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 6x = 6
  T2: S1 -> S2
  S2: x = 1
```

#### Expected Atom Outcomes

- `M1`: `withheld`, primary reason `withhold.invalid_method`, evidence `S0,T1,S1`
- `M2`: `withheld`, primary reason `withhold.unmet_dependency`, evidence `S1,T2,S2`
- `A1`: `withheld`, primary reason `withhold.unmet_dependency`, evidence `S2`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- `M2` MUST cite that `S1` is not an allowed FT source because the coefficient differs from the prompt coefficient

### Test `T06_unsupported_divide_first_route`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: x + 5/3 = 11/3
  T2: S1 -> S2
  S2: x = 2
```

#### Expected Atom Outcomes

- `M1`: `escalated`, primary reason `escalate.unsupported_route`, evidence `S0,T1,S1`
- `M2`: `escalated`, primary reason `escalate.unsupported_route`, evidence `S0,T1,S1`
- `A1`: `escalated`, primary reason `escalate.unsupported_route`, evidence `S2`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- the explanation MUST identify divide-first as the blocking unsupported route

### Test `T07_parse_failure`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: x = (11 ◊ 5) / 3
```

#### Expected Atom Outcomes

- `M1`: `escalated`, primary reason `escalate.ambiguous_parse`, evidence `S0,T1,S1`
- `M2`: `escalated`, primary reason `escalate.ambiguous_parse`, evidence `S0,T1,S1`
- `A1`: `escalated`, primary reason `escalate.ambiguous_parse`, evidence `S1`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- the explanation MUST cite `S1` as not parseable into one complete family-structured representation

### Test `T08_compressed_working_ambiguous`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: x = 11 - 5 / 3
```

#### Expected Atom Outcomes

- `M1`: `escalated`, primary reason `escalate.multiple_interpretations`, evidence `S0,T1,S1`
- `M2`: `escalated`, primary reason `escalate.multiple_interpretations`, evidence `S0,T1,S1`
- `A1`: `escalated`, primary reason `escalate.multiple_interpretations`, evidence `S1`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- the explanation MUST cite that the grouped-solve target is not uniquely interpretable

### Test `T09_contradiction_locality`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 3x = 6
  T2: S1 -> S2
  S2: x = 2
  A1: x = 3
```

#### Expected Atom Outcomes

- `M1`: `awarded`, primary reason `award.direct`, evidence `S0,T1,S1`
- `M2`: `awarded`, primary reason `award.direct`, evidence `S1,T2,S2`
- `A1`: `escalated`, primary reason `escalate.contradictory_work`, evidence `S2,A1`

#### Expected Total

`2`

#### Expected Explanation-Critical References

- `A1` MUST cite both `S2` and `A1`
- `M1` and `M2` MUST remain bound to their own non-contradictory evidence

### Test `T10_multiple_candidate_paths`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 3x = 6
  T2: S1 -> S2
  S2: x = 2

path p2:
  S0b: 3x + 5 = 11
  T1b: S0b -> S1b
  S1b: 3x = 9
  T2b: S1b -> S2b
  S2b: x = 3
```

#### Expected Atom Outcomes

- `M1`: `escalated`, primary reason `escalate.multiple_interpretations`
- `M2`: `escalated`, primary reason `escalate.multiple_interpretations`
- `A1`: `escalated`, primary reason `escalate.multiple_interpretations`

#### Expected Total

`0`

#### Expected Explanation-Critical References

- the explanation MUST cite that more than one candidate path remains and that the path outcomes differ

### Test `T11_visible_correction_then_direct`

#### Prompt / Family Instance

`3x + 5 = 11`

Canonical tuple: `(3, 5, 11)`

#### Structured Student Evidence

```text
path p1:
  S0: 3x + 5 = 11
  T1: S0 -> S1
  S1: 3x = 5
  S0c: 3x + 5 = 11
  T2: S0c -> S2
  S2: 3x = 6
  T3: S2 -> S3
  S3: x = 2
```

#### Expected Atom Outcomes

- `M1`: `awarded`, primary reason `award.direct`, evidence `S0c,T2,S2`
- `M2`: `awarded`, primary reason `award.direct`, evidence `S2,T3,S3`
- `A1`: `awarded`, primary reason `award.direct`, evidence `S3`

#### Expected Total

`3`

#### Expected Explanation-Critical References

- the explanation MUST bind later atoms to the corrected continuation `S0c,T2,S2,T3,S3`
- the explanation MUST NOT use FT

## 11. IMPLEMENTATION NOTES FOR LATER

This family intentionally does not support the cases below in v1:

- prompt coefficients or constants that are fractional or decimal
- `|a| = 1`
- `b = 0`
- prompt-level reordering
- variable-on-both-sides equations
- divide-first working
- direct prompt-to-numeric-final compression
- decimal final answers
- transposition shorthand without exact parseable states

The implementation for this family MUST remain fail closed on any case not explicitly encoded in this document.

Possible later extensions exist but are forbidden in v1:

- prompt decimals and exact rational prompt coefficients
- `ax = c` and `x + b = c` degenerate subfamilies
- variable on both sides with route-specific atoms
- additional exact notation variants
- direct decimal acceptance with exact conversion rules
