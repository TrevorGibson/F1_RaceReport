# F1 Race Report Data Pipeline
This program takes data from F1 Race Weekends and provides a clear report on winning teams, total revenue, costs, and profit across the whole weekend. Weekends are divided into two categories, depending on whether the race weekend has finished or not. The data pipeline validates the data before producing the report and also shows any problems that the detection system did raise so the problems can be fixed.

## Requirements
This program requires Python 3.10 or newer and does not require any external libraries. If this is changed in the future, all requirements will be listed in the requirements.txt file.

## Running the program
From the project root, run:

```console
python main.py
```

## Structure
OOP_DataIngestTransformPipeline/
├── main.py                 # Entry point
├── requirements.txt        # External Libraries (None)
└── pipeline/
    ├── __init__.py         # Package initialization
    ├── schema.py           # Immutable transaction and result data classes
    ├── validator.py        # Data Validation and Conversion
    ├── transformer.py      # Functional filtering and calculates prices in EUROS
    └── reporter.py         # Formats and creates the report
```

## How the Pipeline Works
main.py stores load_synthetic_records, where the F1 Race Data is stored. There are 4 correct entries and 1 with a misentry

validate_records checks and converts input values. Valid rows become RaceRecord instances; invalid rows are recorded as ValidationIssue instances with their row number, source, and reasons.

isolate_weekend_over filters out race weekends that have not finished yet. currency is used to associate each race with its country's currency, which is converted to euros, and net margins calculates the profit

format_report takes the analyzed, valid, and malformed data and organizes it into a presentable form

schema.py ensures that the data classes are frozen and are not changed through the process, and run_pipeline executes the whole process from the beginning so it can be done an infinite number of times

## Example Validation
The fourth race, Monaco, has an invalid operational cost. The value is -20, which is not allowed as it cannot be negative, as stated by the validator. Any value that is flagged as invalid is not counted in the final calculations

## Calculations
This program uses standard profit calculations (revenue - costs = profit), where the profit is then multipled by the rate of conversion to find the total profit of the race weekend in EUROS
