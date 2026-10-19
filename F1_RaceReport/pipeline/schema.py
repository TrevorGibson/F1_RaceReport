

from dataclasses import dataclass

from datetime import date

SUPPORTED_WINNING_TEAMS = frozenset(
    {"Red Bull", "Mercedes","Ferrari", "Mclaren", "Alpine", "Aston Martin", "Audi", "Haas", "VCarb", "Williams","Cadillac", "Undecided"}
)

SUPPORTED_CURRENCY = frozenset(
    {"USD", "CAD", "GBP", "EURO"}
)

@dataclass(frozen=True, slots=True)
class RaceRecord:
    race_id: int
    race_name: str
    race_date: date
    circuit_name: str
    winning_team: str
    weekend_over: bool
    revenue: float
    operating_cost: float
    currency: str



@dataclass(frozen=True, slots=True)
class AdjustedLocalNetMargin:
    record: RaceRecord
    adjusted_net_margin: float

@dataclass(frozen=True, slots=True)
class ValidationIssue:
    row_number: int
    race_id: int
    winning_team: str
    reasons: tuple[str]