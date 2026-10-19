from collections.abc import Sequence

from pipeline.schema import AdjustedLocalNetMargin, RaceRecord, ValidationIssue

def format_report(
    race_id_count: int,
    completed_races: Sequence[RaceRecord],
    valid_records: Sequence[RaceRecord],
    validation_issues: Sequence[ValidationIssue],
    analyzed_records: Sequence[AdjustedLocalNetMargin],
) -> str:
    total_revenue = sum(record.record.revenue for record in analyzed_records)
    total_cost = sum(record.record.operating_cost for record in analyzed_records)
    total_margin = sum(record.adjusted_net_margin for record in analyzed_records)

    lines = [
        "F1 Race Report Pipeline",
        "="* 72,
        f"Total races: {race_id_count}",
        f"Completed races: {completed_races}",
        f"Remaining races: {race_id_count - completed_races}",
        f"Valid rows: {len(valid_records)}",
        f"Malformed rows flagged: {len(validation_issues)}",
        "",
        "Completed Race Weekend Report",
        "-" * 72,
        (
            f"{'Race ID':<10} {'Race Name':<20} {'Winning Team':<20} {'Revenue':>7} "
            f"{'Costs':>10} {'Net Margin':>18}"
        ),
    ]

    lines.extend(
        f"{item.record.race_id:<10} "
        f"{item.record.race_name:<20} "
        f"{item.record.winning_team:<20} "
        f"${item.record.revenue:.2f} "
        f"${item.record.operating_cost:>10.2f} "
        f"${item.adjusted_net_margin:>12,.2f}"
        for item in analyzed_records
    )

    lines.extend(
        [
            "",
            "Completed Race Weekend Totals",
            "-" * 72,
            f"Revenue:      ${total_revenue:,.2f}",
            f"Operating cost: ${total_cost:,.2f}",
            f"Net margin:   ${total_margin:,.2f}",
            "",
            "Validation flags",
            "-" * 72,
        ]
    )

    if validation_issues:
        lines.extend(
            f"Row {issue.row_number}: {issue.race_id} {issue.winning_team}: "
            + "; ".join(issue.reasons)
            for issue in validation_issues
        )
    else:
        lines.append("No malformed rows.")

    return "\n".join(lines)
