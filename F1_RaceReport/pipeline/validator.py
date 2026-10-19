from collections.abc import Iterable, Mapping
from datetime import date
import math

from pipeline.schema import (
    SUPPORTED_CURRENCY,
    SUPPORTED_WINNING_TEAMS, 
    RaceRecord,
    ValidationIssue,
)

def _parse_date(value: object) -> date | None:
    try:
        return date.fromisoformat(str(value).strip())
    except (TypeError, ValueError):
        return None

def _parse_number(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, float, str)):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None

def _parse_active(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"true", "1", "yes"}:
            return True
        if normalized in {"false", "0", "no"}:
            return False
    return None

def validate_records(
    raw_records: Iterable[Mapping[str, object]],
) -> tuple[list[RaceRecord], list[ValidationIssue]]:
    valid_records: list[RaceRecord] = []
    issues: list[ValidationIssue] = []
    reasons: list[str] = []

    for row_number, raw in enumerate(raw_records, start=1):
        race_id = str(raw.get("race_id", "")).strip()
        winning_team = str(raw.get("winning_team", "")).strip()
        reasons: list[str] = []


        if race_id is None:
            reasons.append("invalid race ID")

        race_name = str(raw.get("race_name", "")).strip()
        if not race_name:
            reasons.append("missing race name")

        race_date = _parse_date(raw.get("race_date"))
        if race_date is None:
            reasons.append("invalid race date (expected YYYY-MM-DD)")

        circuit_name = str(raw.get("circuit_name", "")).strip()
        if not circuit_name:
            reasons.append("missing circuit name")

        winning_team = str(raw.get("winning_team", "")).strip()
        if winning_team not in SUPPORTED_WINNING_TEAMS:
            reasons.append(f"unsupported winning team: {winning_team or '(missing)'}")

        revenue = _parse_number(raw.get("revenue"))
        if revenue is None:
            reasons.append("revenue must be a finite number")
        elif revenue < 0:
            reasons.append("revenue cannot be negative")

        operating_cost = _parse_number(raw.get("operating_cost"))
        if operating_cost is None:
            reasons.append("operating cost must be a finite number")
        elif operating_cost < 0:
            reasons.append("operating cost cannot be negative")

        currency = str(raw.get("currency", "")).strip()
        if currency not in SUPPORTED_CURRENCY:
            reasons.append(f"unsupported currency: {currency or '(missing)'}")

        weekend_over = _parse_active(raw.get("weekend_over"))
        if weekend_over is None:
            reasons.append("weekend_over must be a boolean value (true/false)")

    

        if reasons:
            issues.append(
                ValidationIssue(
                    row_number=row_number,
                    race_id=race_id or "(missing)",
                    winning_team=winning_team or "(missing)",
                    reasons=tuple(reasons),
                )
            )
            continue

        if (
            race_id is None
            or race_name is None
            or race_date is None
            or circuit_name is None
            or winning_team is None
            or revenue is None
            or operating_cost is None
            or currency is None
            or weekend_over is None
        ):
            raise RuntimeError("Validated race fields were unexpectedly missing")

        valid_records.append(
            RaceRecord(
                race_id=race_id,
                race_name=race_name,
                race_date=race_date,
                circuit_name=circuit_name,
                winning_team=winning_team,
                revenue=revenue,
                operating_cost=operating_cost,
                currency=currency,
                weekend_over=weekend_over,
            )
        )

    return valid_records, issues