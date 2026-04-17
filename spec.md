# Handwritten IB-Style Math Grading Engine: Marking Logic Spec

This document is the normative contract for the marking logic of a standalone handwritten IB-style math grading engine. Later schemas, parser behavior, engine code, tests, and ingestion layers MUST conform to this contract. This document covers marking logic only. It does not define APIs, storage, OCR, UI, or syllabus-wide coverage.

## 1. Purpose and Scope

This system awards exam-style marks from structured student mathematical working. It is not a final-answer checker, not a generic OCR-plus-compare system, and not a black-box grader.

For this milestone, student work is assumed to already exist as manually structured mathematical steps, states, and transitions. OCR, handwriting recognition, page segmentation, and vision extraction are out of scope.

Support expands by narrow question family, not by whole syllabus topic. A family is a bounded class of questions with a fixed set of accepted routes, mark atoms, dependencies, follow-through rules, equivalence rules, and failure behavior. If a family is not explicitly supported, auto-marking is not allowed.

## 2. Core Philosophy

The engine MUST obey these principles:

- Deterministic: identical structured input under the same family definition MUST produce identical atom outcomes, totals, and explanations.
- Fail-closed: if family rules and structured evidence do not determine one unique outcome for an atom, the atom MUST escalate.
- Explicit evidence only: the engine MUST NOT infer unseen working, student intent, or examiner generosity.
- Explicit rule coverage only: unsupported routes, notation, equivalence, or FT behavior MUST NOT receive guessed credit.
- No black-box decisions: every mark outcome MUST be traceable to explicit rule evaluation over structured evidence.
- No answer-only credit when method is required: a correct-looking result alone is insufficient if the family requires visible method.
- Ambiguity that changes marks MUST escalate.

## 3. Mark Taxonomy

### `M` marks: method

Meaning: credit for performing a family-accepted mathematical method or transformation toward the required result.

Award an `M` atom if and only if:

- the family defines the atom as `M`
- the required method step is visible in the structured working or in an explicitly permitted compressed form
- the shown transition is a family-accepted transformation
- all declared dependencies are satisfied

Do not award an `M` atom when:

- method visibility is required and only an answer state is present
- the transition is invalid
- the route is unsupported
- the atom depends on prior evidence or atoms that are not satisfied

### `A` marks: accuracy

Meaning: credit for a correct result, value, expression, or conclusion.

Award an `A` atom if and only if:

- the family defines the atom as `A`
- the target state is correct under the family’s exact equivalence, domain, sign, rounding, and form rules
- all declared dependencies are satisfied

Do not award an `A` atom when:

- the result is incorrect
- the result is only accidentally correct after a required method dependency fails
- the result depends on an equivalence or form rule that the family has not encoded

### `B` marks: independent marks

Meaning: credit for an independently markable item that does not depend on the main method chain.

Award a `B` atom if and only if:

- the family defines the atom as `B`
- the item is directly and unambiguously evidenced
- the atom has no unmet declared dependency

Do not award a `B` atom when:

- the item is ambiguous
- independence is not explicitly encoded
- the item actually relies on failed prior work

### `FT` / `CF`: follow-through / carried-forward credit

`FT` / `CF` is not a base mark type. It is a controlled evaluation mode for an `M` or `A` atom.

Award by FT if and only if:

- the atom is an `M` or `A` atom
- the family explicitly enables FT for that atom
- all FT rules in section 6 pass

`B` atoms MUST NOT use FT.

## 4. Mark Atom Model

The engine MUST award marks as atomic, testable conditions. One atom represents one assessable mark unit and awards exactly one mark when awarded.

Each atom MUST define:

- `id`: unique within the family
- `type`: `M`, `A`, or `B`
- `description`: exact statement of the credited item
- `value`: fixed at `1`
- `path binding rule`: how the atom attaches to a single ordered student solution path
- `dependencies`: an exact boolean condition over named earlier atoms or named evidence predicates
- `evidence rule`: the exact structured states, transitions, or assertions required
- `success predicate`: the exact award condition
- `withhold predicates`: the exact deterministic no-credit conditions
- `escalation predicates`: the exact conditions that block deterministic marking
- `FT policy`: either `disallowed` or an explicit FT rule reference
- `explanation requirements`: the explanation content required by section 10

Each atom MUST resolve to exactly one outcome:

- `awarded`
- `withheld`
- `escalated`

Outcome semantics are fixed:

- `awarded` grants `1` mark
- `withheld` grants `0` marks
- `escalated` grants `0` auto-awarded marks and records a blocking escalation

If an escalation predicate and a withhold predicate are both true for the same atom, `escalated` takes precedence.

## 5. Dependency Rules

Dependencies determine whether an atom is allowed to evaluate on a given solution path.

A dependency definition MUST be one of:

- `none`
- an exact boolean expression over named earlier atoms
- an exact boolean expression over named earlier atoms plus named evidence predicates

Natural-language dependencies such as “appropriate method” or “working seen” are not sufficient unless they are reduced to exact named predicates in the family definition.

`Requires valid method` means all named method dependencies are awarded on the same bound solution path, either directly or by explicit FT where the dependent atom permits FT satisfaction.

The engine MUST enforce all dependency rules below:

- An atom with an unmet dependency MUST resolve to `withheld`.
- An `A` atom MUST NOT evaluate as awarded from an isolated correct-looking line if its dependency path is not satisfied.
- The engine MUST bind each atom to one ordered solution path. It MUST NOT combine evidence from inconsistent paths to build a synthetic dependency chain.
- Each family’s dependency graph MUST be acyclic.
- If more than one path binding is possible for an atom and different bindings change the outcome, the atom MUST resolve to `escalated`.

## 6. Follow-Through Rules

Follow-through means evaluating a later `M` or `A` atom relative to one earlier erroneous student state instead of the canonical correct state.

FT is allowed for an atom if and only if all conditions below are true:

- the atom’s `FT policy` is not `disallowed`
- the policy names exactly one eligible carried source state or source atom
- that source is earlier on the same bound solution path
- that source is parseable, incorrect relative to the canonical path, and free of internal contradiction
- the later step is derivable from that carried source by a family-accepted transformation
- every reused value, sign, symbol, and form that originates from the carried source remains consistent with that carried source unless the family defines an explicit recovery step
- all non-FT dependencies of the atom are satisfied

FT is disallowed, and the atom MUST resolve to `withheld`, when:

- the family forbids FT for that atom
- the atom is a `B` atom
- the later step would require carrying more than one earlier error state and the family has not explicitly defined multi-error FT
- the later step abandons the carried source and switches to a different erroneous value on a deterministic path

FT MUST resolve to `escalated`, not `withheld`, when:

- the engine cannot uniquely identify the carried source
- the engine cannot determine whether the student is following the carried source or a corrected canonical path
- contradictory later work makes the carried source unresolved

Interaction with mark types is fixed:

- An `M` atom awarded by FT still requires visible method and a valid transformation from the carried source.
- An `A` atom awarded by FT still requires all declared method dependencies to be satisfied directly or by explicit FT.
- FT never waives visibility, dependency, equivalence, domain, sign, rounding, or form requirements.

If the student visibly corrects an earlier error and then continues from the corrected state, later atoms MUST be evaluated on the corrected state, not by FT.

## 7. Evidence Rules

Creditable evidence MUST be tied to structured mathematical states, transitions, or assertions. Raw text similarity, prose intent, or visual resemblance is not evidence.

For a step to count as valid evidence, the family rules MUST be able to identify:

- a parseable prior state, unless the atom is defined as a state-only atom
- a parseable resulting state, unless the atom is defined as an assertion-only atom
- the exact transition, relation, or assertion being credited
- the bound solution path on which the evidence sits

Visible method is mandatory whenever the atom or one of its dependencies tests method. In those cases, a final answer state alone is not enough.

Compressed working is acceptable if and only if:

- the family defines the exact compressed pattern as accepted evidence
- the compressed form identifies one unique credited transformation
- no omitted intermediate choice point could change the mark outcome

Missing intermediate working has fixed outcomes:

- if the family requires the missing step and the remaining evidence still yields one deterministic interpretation, the atom MUST resolve to `withheld`
- if the missing step leaves multiple plausible interpretations that change the mark outcome, the atom MUST resolve to `escalated`

Every awarded atom MUST cite the exact evidence items that satisfied it.

## 8. Equivalence Rules

Equivalence acceptance is family-scoped and explicit. If a family does not encode an equivalence rule for an atom, that atom uses exact structured equality.

For each atom that accepts non-exact forms, the family MUST define the accepted equivalence classes. The family MUST state for each of the following whether it is allowed or disallowed for that atom:

- algebraic equivalence allowed
- ordering equivalence allowed
- sign normalization allowed
- factor normalization allowed
- exact alternate representations allowed
- notation variants allowed
- domain restrictions
- rounding or precision requirements

An atom MUST NOT be awarded on the basis of an unlisted equivalence. If mark resolution depends on an equivalence, notation, tolerance, or domain rule that the family has not encoded, the atom MUST resolve to `escalated`.

Equivalence acceptance in one family MUST NOT transfer to another family.

## 9. Failure and Escalation Rules

`Withheld` and `escalated` are different outcomes and MUST be used differently.

An atom MUST resolve to `withheld` if and only if:

- the evidence is parseable on one deterministic path
- the family has the rules required to evaluate the atom
- no escalation predicate is true
- at least one success predicate is false

The default deterministic withhold reasons are:

- `withhold.unmet_dependency`
- `withhold.no_visible_method`
- `withhold.invalid_method`
- `withhold.incorrect_result`
- `withhold.insufficient_evidence`
- `withhold.follow_through_not_permitted`

An atom MUST resolve to `escalated` if and only if deterministic evaluation is blocked by ambiguity, contradiction, or missing family support.

The default escalation reasons are:

- `escalate.ambiguous_parse`
- `escalate.multiple_interpretations`
- `escalate.unsupported_route`
- `escalate.unsupported_notation`
- `escalate.contradictory_work`
- `escalate.missing_family_rule`
- `escalate.unresolved_follow_through_source`

The following cases MUST escalate rather than receive guessed marks:

- ambiguous parsing of a symbol, state, operator, or transition
- multiple plausible interpretations that affect marks
- unsupported solution route
- unsupported notation or layout
- contradictory student work that affects the atom
- missing equivalence, tolerance, domain, or FT rule needed for resolution

If an escalation condition affects only some atoms, unaffected atoms MUST still resolve normally if their evidence and dependencies remain isolated and deterministic.

## 10. Explanation Model

Every atom decision MUST be explainable deterministically.

For each atom, the engine MUST output:

- atom id
- atom type
- outcome
- awarded mark value
- primary reason code
- bound solution path reference
- evidence references used for the decision
- dependency verdicts
- FT verdict, including source reference when FT is used

The primary reason code MUST come from the closed set in section 9 or from:

- `award.direct`
- `award.follow_through`

Primary reason code selection MUST be deterministic. If more than one reason is true, the engine MUST choose the first matching reason in this priority order:

1. `escalate.ambiguous_parse`
2. `escalate.multiple_interpretations`
3. `escalate.contradictory_work`
4. `escalate.unsupported_route`
5. `escalate.unsupported_notation`
6. `escalate.missing_family_rule`
7. `escalate.unresolved_follow_through_source`
8. `withhold.unmet_dependency`
9. `withhold.no_visible_method`
10. `withhold.insufficient_evidence`
11. `withhold.follow_through_not_permitted`
12. `withhold.invalid_method`
13. `withhold.incorrect_result`
14. `award.follow_through`
15. `award.direct`

Question-level explanations MUST be derivable as the ordered list of atom explanations plus the total awarded marks.

## 11. Family-Based Expansion Model

Support enters the system one narrow family at a time. A family MUST contain, before live auto-marking:

- an exact family boundary
- the accepted prompts or prompt pattern covered by that boundary
- the supported solution routes
- the unsupported routes and unsupported notation that must escalate
- the full atom set
- the dependency graph
- the FT policy for every atom
- the equivalence rules for every atom that uses non-exact matching
- golden tests covering award, withhold, and escalation cases
- stable deterministic explanation traces for those tests

Auto-marking for a family is forbidden until all of the above exist and the golden tests pass. There is no generic fallback grader for unsupported families.

## 12. First Milestone Framing

The first milestone is limited to:

- manually structured student working
- 3 to 5 narrow question families
- deterministic atom-level mark awards
- deterministic explanation traces
- fail-closed escalation for unsupported or ambiguous cases
- no OCR

## 13. Out of Scope

The following are out of scope for this spec and milestone:

- OCR
- handwriting recognition
- image segmentation
- teacher review UI
- syllabus-wide support
- generic reasoning extraction
- black-box grading
- unconstrained natural-language interpretation of student intent
- confidence scoring beyond fail-closed escalation

This document is the contract for step 1 only: mark taxonomy and marking logic. It does not define later schemas, parser implementation, engine code, or ingestion.
