
from pipeline.reporter import format_report
from pipeline.validator import validate_records
from pipeline.transformer import(
    adjusted_net_margin, 
    isolate_weekend_over_records)


from datetime import date


    

def load_synthetic_records() -> list[dict[str, object]]:
    return [
        {
            "race_id": "1",
            "race_name": "US Grand Prix",
            "race_date": "2023-03-19",
            "circuit_name": "Circuit of the Americas",
            "winning_team": "Red Bull",
            "weekend_over": True,
            "revenue": "70",
            "operating_cost": "15",
            #To reduce clutter, both operating cost and revenue are in millions#
            "currency": "USD" 
            
        },
        {
            "race_id": "2",
            "race_name": "Montreal Grand Prix",
            "race_date": "2023-03-26",
            "circuit_name": "Circuit Gilles Villeneuve",
            "winning_team": "Mercedes",
            "weekend_over": True, 
            "revenue": "50",
            "operating_cost": "9",
            #To reduce clutter, both operating cost and revenue are in millions#
            "currency": "CAD"
        },

        {
            "race_id": "3",
            "race_name": "British Grand Prix",
            "race_date": "2023-04-09",
            "circuit_name": "Silverstone Circuit",
            "winning_team": "Undecided",
            "weekend_over": False,
            "revenue": "10",
            "operating_cost": "6",
            #To reduce clutter, both operating cost and revenue are in millions#
            "currency": "GBP"
        },
        {
            "race_id": "4",
            "race_name": "Monaco Grand Prix",
            "race_date": "2023-05-28",
            "circuit_name": "Circuit de Monaco",
            "winning_team": "Undecided",
            "weekend_over": False,
            "revenue": "80",
            "operating_cost": "-20",
            #To reduce clutter, both operating cost and revenue are in millions#
            "currency": "EURO"
        },
        
        {
            "race_id": "5",
            "race_name": "Miami Grand Prix",
            "race_date": "2023-09-17",
            "circuit_name": "Miami International Autodrome",
            "winning_team": "Alpine",
            "weekend_over": True,
            "revenue": "60",
            "operating_cost": "12",
            #To reduce clutter, both operating cost and revenue are in millions#
            "currency": "USD"
        },
    ]

def run_pipline() -> str:
    race_records = load_synthetic_records()
    valid_records, validation_issues = validate_records(race_records)
    weekend_over_records = isolate_weekend_over_records(valid_records)
    analyzed_records = adjusted_net_margin(weekend_over_records)

    return format_report(
        race_id_count=len(race_records),
        valid_records=valid_records,
        validation_issues=validation_issues,
        completed_races=len(weekend_over_records),
        analyzed_records=analyzed_records,
    )

def main() -> None:
    print(run_pipline())

if __name__ == "__main__":
    main()
