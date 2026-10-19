

from collections.abc import Iterable, Mapping
from types import MappingProxyType

from pipeline.schema import (
    RaceRecord,
    AdjustedLocalNetMargin,
)

REGIONAL_CURRENCY_CONVERSION_RATES: Mapping[str, float] = MappingProxyType(
    {
        "USD": 0.89,
        "CAD": 0.63,
        "GBP": 1.19,
        "EURO": 1.0,
        #Currency conversion rates from listed type to EURO#
    }
)

def adjusted_net_margin(
        record: Iterable[RaceRecord],
        converted_currency: Mapping[str, float] = REGIONAL_CURRENCY_CONVERSION_RATES) -> list[AdjustedLocalNetMargin]:
    return [
        AdjustedLocalNetMargin(
            record=record,
            adjusted_net_margin=(
                (record.revenue - record.operating_cost)
                * converted_currency.get(record.currency, 1.0)
            ),
        )
        for record in record
    ]

def isolate_weekend_over_records(
    records: Iterable[RaceRecord],  
    ) -> list[RaceRecord]:
    return list(filter(lambda record: record.weekend_over, records))