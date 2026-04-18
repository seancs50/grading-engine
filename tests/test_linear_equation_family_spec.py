from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = REPO_ROOT / "families" / "linear_equation_ax_plus_b_eq_c.md"
SPEC_TEXT = SPEC_PATH.read_text(encoding="utf-8")


def _extract_heading_block(heading_pattern: str, next_heading_pattern: str) -> str:
    pattern = rf"{heading_pattern}\n(.*?)(?=\n{next_heading_pattern})"
    match = re.search(pattern, SPEC_TEXT, flags=re.DOTALL)
    assert match, f"missing block starting {heading_pattern!r}"
    return match.group(1)


def _extract_test_block(test_id: str) -> str:
    pattern = (
        rf"### Test `{re.escape(test_id)}`\n(.*?)(?=\n### Test `|\n## 11\. IMPLEMENTATION NOTES FOR LATER)"
    )
    match = re.search(pattern, SPEC_TEXT, flags=re.DOTALL)
    assert match, f"missing golden test block for {test_id}"
    return match.group(1)


def _parse_atom_outcomes(block: str) -> dict[str, tuple[str, str]]:
    matches = re.findall(
        r"- `(M1|M2|A1)`: `(awarded|withheld|escalated)`, primary reason `([^`]+)`",
        block,
    )
    assert matches, "expected atom outcomes were not found"
    return {atom: (outcome, reason) for atom, outcome, reason in matches}


def _parse_total(block: str) -> int:
    match = re.search(r"#### Expected Total\s+`(\d+)`", block, flags=re.DOTALL)
    assert match, "expected total was not found"
    return int(match.group(1))


def test_family_spec_file_exists():
    assert SPEC_PATH.exists()
    assert "linear_equation_ax_plus_b_eq_c__int_prompt__x_only__v1" in SPEC_TEXT


@pytest.mark.parametrize(
    ("test_id", "expected_outcomes", "expected_total"),
    [
        (
            "T01_perfect_r1",
            {
                "M1": ("awarded", "award.direct"),
                "M2": ("awarded", "award.direct"),
                "A1": ("awarded", "award.direct"),
            },
            3,
        ),
        (
            "T02_perfect_r2_grouped",
            {
                "M1": ("awarded", "award.direct"),
                "M2": ("awarded", "award.direct"),
                "A1": ("awarded", "award.direct"),
            },
            3,
        ),
        (
            "T03_answer_only_no_method",
            {
                "M1": ("withheld", "withhold.no_visible_method"),
                "M2": ("withheld", "withhold.unmet_dependency"),
                "A1": ("withheld", "withhold.unmet_dependency"),
            },
            0,
        ),
        (
            "T04_ft_success_from_wrong_isolated_rhs",
            {
                "M1": ("withheld", "withhold.invalid_method"),
                "M2": ("awarded", "award.follow_through"),
                "A1": ("awarded", "award.follow_through"),
            },
            2,
        ),
        (
            "T05_ft_denied_changed_coefficient",
            {
                "M1": ("withheld", "withhold.invalid_method"),
                "M2": ("withheld", "withhold.unmet_dependency"),
                "A1": ("withheld", "withhold.unmet_dependency"),
            },
            0,
        ),
        (
            "T06_unsupported_divide_first_route",
            {
                "M1": ("escalated", "escalate.unsupported_route"),
                "M2": ("escalated", "escalate.unsupported_route"),
                "A1": ("escalated", "escalate.unsupported_route"),
            },
            0,
        ),
        (
            "T07_parse_failure",
            {
                "M1": ("escalated", "escalate.ambiguous_parse"),
                "M2": ("escalated", "escalate.ambiguous_parse"),
                "A1": ("escalated", "escalate.ambiguous_parse"),
            },
            0,
        ),
        (
            "T08_compressed_working_ambiguous",
            {
                "M1": ("escalated", "escalate.multiple_interpretations"),
                "M2": ("escalated", "escalate.multiple_interpretations"),
                "A1": ("escalated", "escalate.multiple_interpretations"),
            },
            0,
        ),
        (
            "T09_contradiction_locality",
            {
                "M1": ("awarded", "award.direct"),
                "M2": ("awarded", "award.direct"),
                "A1": ("escalated", "escalate.contradictory_work"),
            },
            2,
        ),
        (
            "T10_multiple_candidate_paths",
            {
                "M1": ("escalated", "escalate.multiple_interpretations"),
                "M2": ("escalated", "escalate.multiple_interpretations"),
                "A1": ("escalated", "escalate.multiple_interpretations"),
            },
            0,
        ),
        (
            "T11_visible_correction_then_direct",
            {
                "M1": ("awarded", "award.direct"),
                "M2": ("awarded", "award.direct"),
                "A1": ("awarded", "award.direct"),
            },
            3,
        ),
    ],
)
def test_golden_cases_define_exact_atom_outcomes_and_totals(
    test_id: str,
    expected_outcomes: dict[str, tuple[str, str]],
    expected_total: int,
) -> None:
    block = _extract_test_block(test_id)
    assert _parse_atom_outcomes(block) == expected_outcomes
    assert _parse_total(block) == expected_total


def test_follow_through_success_block_explicitly_marks_ft_usage() -> None:
    block = _extract_test_block("T04_ft_success_from_wrong_isolated_rhs")
    assert "FT source `S1`" in block
    outcomes = _parse_atom_outcomes(block)
    assert outcomes["M2"] == ("awarded", "award.follow_through")
    assert outcomes["A1"] == ("awarded", "award.follow_through")


def test_visible_correction_block_explicitly_rebinds_without_ft() -> None:
    block = _extract_test_block("T11_visible_correction_then_direct")
    assert "MUST bind later atoms to the corrected continuation" in block
    assert "MUST NOT use FT" in block


def test_boundary_rejects_abs_a_equals_one() -> None:
    out_of_scope = _extract_heading_block(
        r"### Explicit Out-of-Scope Prompt Forms",
        r"### Supported Student Route",
    )
    assert "- `|a| = 1`" in out_of_scope


def test_boundary_rejects_b_equals_zero() -> None:
    out_of_scope = _extract_heading_block(
        r"### Explicit Out-of-Scope Prompt Forms",
        r"### Supported Student Route",
    )
    assert "- `b = 0`" in out_of_scope


def test_boundary_rejects_reordered_prompts() -> None:
    out_of_scope = _extract_heading_block(
        r"### Explicit Out-of-Scope Prompt Forms",
        r"### Supported Student Route",
    )
    assert "b + ax = c" in out_of_scope
    assert "c = ax + b" in out_of_scope


def test_notation_rules_reject_decimal_final_answers() -> None:
    unsupported_notation = _extract_heading_block(
        r"### Unsupported Notation",
        r"### Unsupported Evidence Shape",
    )
    form_rules = _extract_heading_block(
        r"### Unsimplified Intermediate and Final Forms",
        r"### Cancellation and Compression",
    )
    assert "- decimal final answers" in unsupported_notation
    assert "- for `A1`, a decimal final answer is not accepted" in form_rules


def test_notation_rules_reject_unsupported_variable_symbol() -> None:
    unsupported_notation = _extract_heading_block(
        r"### Unsupported Notation",
        r"### Unsupported Evidence Shape",
    )
    assert "- any variable symbol other than exact lowercase `x`" in unsupported_notation


def test_grouped_expression_parsing_is_fail_closed() -> None:
    canonical_meaning = _extract_heading_block(
        r"### Family-Wide Canonical Meaning",
        r"### Atom-Scoped Rules for `M1`",
    )
    route_r2 = _extract_heading_block(
        r"### Route `R2`: Direct Grouped Solve",
        r"## 4\. MARK ATOM SET",
    )
    assert "The parser for this family MUST enforce standard operator precedence." in canonical_meaning
    assert "`x = c - b / a` MUST resolve to `escalated` with `escalate.multiple_interpretations`." in canonical_meaning
    assert "grouped expressions MUST use parentheses" in route_r2


def test_path_binding_rules_define_deterministic_tiebreakers() -> None:
    binding_rules = _extract_heading_block(
        r"### Path Selection and Binding Rules",
        r"### Atom `M1`",
    )
    assert "choose the path with the earliest valid `M1` candidate" in binding_rules
    assert "choose the path with the earliest final valid `A1` state" in binding_rules
    assert "the affected atom MUST escalate with `escalate.multiple_interpretations`" in binding_rules
    assert "Correction overrides earlier path segments." in binding_rules
    assert "FT MUST apply only within one single bound path." in binding_rules


def test_ft_source_definition_allows_only_unique_attachable_isolated_term_sources() -> None:
    ft_predicate_block = _extract_heading_block(
        r"### Family Evidence Predicates Used by Dependencies",
        r"### Path Selection and Binding Rules",
    )
    assert (
        "produced by a parseable transition OR a standalone equation state that is uniquely attachable"
        in ft_predicate_block
    )
    assert (
        "If no transition is present, `Sft` MUST still be uniquely derivable from the canonical prompt form"
        in ft_predicate_block
    )
    assert "the affected atom MUST escalate with `escalate.multiple_interpretations`" in ft_predicate_block
