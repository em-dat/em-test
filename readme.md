# EM-TEST

EM-TEST is a testing framework for the [EM-DAT](https://www.emdat.be/) public 
data relying on the [`pandas`](https://pandas.pydata.org/) and 
[`pandera`](https://pandera.readthedocs.io/en/stable/) Python packages.

> [!IMPORTANT]
> This version of EM-TEST has been built for EM-DAT public data on 2024/08/26.
> Some tests should fail for version prior to this date. EM-TEST is not suited 
> for EM-DAT versions prior to September, 26, 2023. 

## Why using EM-TEST?

The EM-DAT database is a long-lasting project that has started in 1988. In the
past, data was encoded manually sometimes using free text fields without
constraints. The EM-TEST framework was initially developed to identify issues
in the data, prior to the redesign of the database. EM-TEST is to some extent 
redundant with many existing constraints in the EM-DAT database. 
So, why using EM-TEST? Here is five reasons:

1. EM-DAT database constraints are invisible to the end-users, while EM-TEST is
   open-source and transparently illustrates implemented testing.
2. EM-DAT is changing over time based on projects and feedback, using EM-TEST
   allows you to check if two or more EM-DAT files are compatible.
3. EM-TEST reports exceptions to existing standards such as ISO3,
   country names, region names that were used in the past but not referred in
   today's reference.
4. Some EM-TEST cases may not be implemented in the database constraints as
   they are more fit to Python pandas Dataframe validation. If EM-TEST is run
   periodically by the EM-DAT team, you may have interest in running EM-TEST to
   validate recent changes in the database.
5. You need a more rigorous testing or need to apply testing to a former
   archive of EM-DAT? You can download EM-TEST and quickly customize the
   validation scheme to fit your own needs.

## EM-DAT Validation Schema

### Data Type Validation

The table shows type constraints check with the implemented validation schema.

| Column                                     | Type      | Nullable | Unique |
|--------------------------------------------|-----------|----------|--------|
| DisNo.                                     | str       | False    | True   |
| Historic                                   | str       | False    | False  |
| Classification Key                         | str       | False    | False  |
| Disaster Group                             | str       | False    | False  |
| Disaster Subgroup                          | str       | False    | False  |
| Disaster Type                              | str       | False    | False  |
| Disaster Subtype                           | str       | False    | False  |
| External IDs                               | str       | True     | False  |
| Event Name                                 | str       | True     | False  |
| ISO                                        | str       | False    | False  |
| Country                                    | str       | False    | False  |
| Subregion                                  | str       | False    | False  |
| Region                                     | str       | False    | False  |
| Location                                   | str       | True     | False  |
| Origin                                     | str       | True     | False  |
| Associated Types                           | str       | True     | False  |
| OFDA/BHA Response                          | str       | False    | False  |
| Appeal                                     | str       | False    | False  |
| Declaration                                | str       | False    | False  |
| AID Contribution ('000 US$)                | float     | True     | False  |
| Magnitude                                  | float     | True     | False  |
| Magnitude Scale                            | str       | True     | False  |
| Latitude                                   | float     | True     | False  |
| Longitude                                  | float     | True     | False  |
| River Basin                                | str       | True     | False  |
| Start Year                                 | int       | False    | False  |
| Start Month                                | float[^1] | True     | False  |
| Start Day                                  | float[^1] | True     | False  |
| End Year                                   | int       | False    | False  |
| End Month                                  | float[^1] | True     | False  |
| End Day                                    | float[^1] | True     | False  |
| Total Deaths                               | float[^1] | True     | False  |
| No. Injured                                | float[^1] | True     | False  |
| No. Affected                               | float[^1] | True     | False  |
| No. Homeless                               | float[^1] | True     | False  |
| Total Affected                             | float[^1] | True     | False  |
| Reconstruction Costs ('000 US$)            | float     | True     | False  |
| Reconstruction Costs, Adjusted ('000 US$)  | float     | True     | False  |
| Insured Damage ('000 US$)                  | float     | True     | False  |
| Insured Damage, Adjusted ('000 US$)        | float     | True     | False  |
| Total Damage ('000 US$)                    | float     | True     | False  |
| Total Damage, Adjusted ('000 US$)          | float     | True     | False  |
| CPI                                        | float     | True     | False  |
| Admin Units                                | str       | True     | False  |
| Entry Date                                 | Timestamp | False    | False  |
| Last Update                                | Timestamp | False    | False  |

[^1]: Integer type in Python is not nullable, hence these values are typed as
float numbers.

### Column Checks

For each column in EM-DAT, `pandera` makes it possible to test and validate
column's content with [Checks](https://pandera.readthedocs.io/en/stable/checks.html).
The current checks are listed in the table below.

Most test are implemented as errors, meaning that they should imperatively 
pass to consider the EM-DAT dataset valid. Warnings, instead, are used to 
notify an abnormal, yet, possible value. Column checks have four possible 
warnings on the 'ISO', 'Country', 'Start Year', and 'CPI' columns. 

EM-DAT may contain ISO country codes or country names
that are not listed in the currently used reference
(See[EM-DAT Documentation](https://doc.emdat.be/docs/data-structure-and-content/spatial-information/#united-nations-m49-standard-country-or-area-codes)). EM-DAT has a few exceptions for oversea 
territories and historical countries not included in the current reference. 
This is somewhat normal given polical changes throughout History, yet,
EM-TEST allows to explicitly flag which cases are in EM-DAT thanks to the 
implemented warning. 

Regarding the warning comparing the Start Year to the year included in the 
DisNo., `check_disno_vs_start_year `,  both year should be identical. However, 
it may happen that in the final reference used to describe the disaster event, 
the official start date has been updated. Such a change is more likely for slow
onset disasters like droughts. For this reason, the test is implemented as a
warning that will retrieve these cases, as well as potential errors in the
year definition. 

Finally, we test the 'CPI' value to be in the range 0-100. Technically,
CPI should only be greater than 0. EM-DAT rescales de CPI values such that the
last-year CPI is set to 100, which makes it very unlikely to have values above
100, because it would refer to a year of deflation 
(See [EM-DAT Documentation](https://doc.emdat.be/docs/protocols/economic-adjustment/)). 

| Column                                    | Test Name                        | Test Description                                         | Test Type |
|-------------------------------------------|----------------------------------|----------------------------------------------------------|-----------|
| DisNo.                                    | check_disno                      | Validate value using regular expression                  | Error     |
| Historic                                  | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| Classification Key                        | check_classification_key         | Test whether value is in the reference list              | Error     |
| Disaster Group                            | check_group                      | Test whether value is in the reference list              | Error     |
| Disaster Subgroup                         | check_subgroup                   | Test whether value is in the reference list              | Error     |
| Disaster Type                             | check_type                       | Test whether value is in the reference list              | Error     |
| Disaster Subtype                          | check_subtype                    | Test whether value is in the reference list              | Error     |
| External IDs                              | validate_external_id             | Validate values using regular expressions                | Error     |
| Event Name                                | -                                | -                                                        | -         |
| ISO                                       | validate_iso3_code               | Validate values using regular expressions                | Error     |
|                                           | check_iso3_code                  | Test whether value is in the reference list              | Warning   |
| Country                                   | check_country                    | Test whether value is in the reference list              | Warning   |
| Subregion                                 | check_subregion                  | Test whether value is in the reference list              | Error     |
| Region                                    | check_region                     | Test whether value is in the reference list              | Error     |
| Location                                  | -                                | -                                                        | -         |
| Origin                                    | -                                | -                                                        | -         |
| Associated Types                          | -                                | -                                                        | -         |
| OFDA/BHA Response                         | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| Appeal                                    | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| Declaration                               | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| AID Contribution ('000 US$)               | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Magnitude                                 | -                                | -                                                        | -         |
| Magnitude Scale                           | check_magnitude_unit             | Test whether value is in the reference list              | Error     |
| Latitude                                  | in_range(-90., 90.)              | Test whether value is within range -90-90                | Error     |
| Longitude                                 | in_range(-180., 180.)            | Test whether value is within range -180-180              | Error     |
| River Basin                               | -                                | -                                                        | -         |
| Start Year                                | in_range(1900, CURRENT_YEAR)     | Test whether value is within range 1900-{CURRENT_YEAR}   | Error     |
|                                           | check_disno_vs_start_year[^2]    | Test that start year is the same as in DisNo             | Warning   |   
| Start Month                               | check_month                      | Test whether value is a valid month number (1-12)        | Error     |
| Start Day                                 | check_day                        | Test whether value is a valid day number (1-31)          | Error     |
| End Year                                  | in_range(1900, CURRENT_YEAR)     | Test whether value is within range 1900-{CURRENT_YEAR}   | Error     |
| End Month                                 | check_month                      | Test whether value is a valid month number (1-12)        | Error     |
| End Day                                   | check_day                        | Test whether value is a valid day number (1-31)          | Error     |
| Total Deaths                              | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| No. Injured                               | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| No. Affected                              | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| No. Homeless                              | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Total Affected                            | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Reconstruction Costs ('000 US$)           | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Reconstruction Costs, Adjusted ('000 US$) | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Insured Damage ('000 US$)                 | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Insured Damage, Adjusted ('000 US$)       | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Total Damage ('000 US$)                   | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| Total Damage, Adjusted ('000 US$)         | greater_than(0.)                 | Test whether value is greater than 0                     | Error     |
| CPI                                       | in_range(0., 110.)               | Test whether value is within range 0-100                 | Warning   |
| Admin Units                               | is_valid_json                    | Test whether value is a json string                      | Error     |
| Entry Date                                | in_range(1988/1/1, CURRENT_DATE) | Test whether value is within valid date range            | Error     |
| Last Update                               | in_range(1988/1/1, CURRENT_DATE) | Test whether value is within valid date range            | Error     |

[^2]: Comparing Start Year to DisNo. is not considered as a multi-column check
because DisNo. is the index of the Column Series in `pandera`. Hence, the test
is not implemented at the DataFrame level.

### Multi-column Checks

The `pandera` package makes it possible to define 
[Wide Checks](https://pandera.readthedocs.io/en/stable/checks.html#wide-checks) 
at the Dataframe level, enabling multi-column checks. The currently implemented
multi-column checks are list below. 

| Columns                                                          | Test Name                         | Test Description                                                                                | Test Type |
|------------------------------------------------------------------|-----------------------------------|-------------------------------------------------------------------------------------------------|-----------|
| Latitude, Longitude                                              | check_both_lat_lon_coordinates    | Test whether latitude and longitude coordinates are either both defined or undefined            | Error     |
| Start Month, Start Day                                           | check_no_start_day_if_no_month    | Test whether Start Day is set if Start Month is not                                             | Error     |
| End Month, End Day                                               | check_no_end_day_if_no_month      | Test whether End Day is set if End Month is not                                                 | Error     |
| Start Year, End Year                                             | check_start_end_year_consistency  | Test whether start year is prior or equal to end year                                           | Error     |
| Start Year, Start Month, End Year, End Month                     | check_start_end_month_consistency | Test whether start year is prior or equal to end year at the month resolution                   | Error     |
| Start Year, Start Month, Start Day, End Year, End Month, End Day | check_start_end_day_consistency   | Test whether start year is prior or equal to end year at the day resolution                     | Error     |
| Disaster Subtype, Magnitude                                      | check_coldwave_magnitude          | Test whether coldwave magnitude is in realistic range (<=10°C)                                  | Error     |
| Disaster Type, Magnitude                                         | check_earthquake_magnitude        | Test whether earthquake magnitude is in realistic range (3 to 10)                               | Error     |
| Disaster Subtype, Magnitude                                      | check_heatwave_magnitude          | Test whether heatwave magnitude is in realistic range (>=25°C)                                  | Error     |
| Disaster Type, Magnitude                                         | check_other_magnitude             | Test whether disaster different from earthquake, cold and heat waves have magnitude above zero  | Error     |


## How to Use?

### Prerequisites

EM-TEST was developed using Python 3.11 with the following dependencies:

```
openpyxl~=3.1
pandas~=2.2
pandera~=0.20
```

### Installation

1. Download the project or clone the repository to your local machine using Git

```bash
git clone https://github.com/em-dat/EM-TEST.git
```

2. Navigate to the project's directory
3. Create a Python virtual environment

On macOS and Linux:
```bash
python3 -m venv env       # Create virtual environment
source env/bin/activate   # Activate virtual environment
```

On Windows:
```bash
py -m venv env            # Create virtual environment
.\env\Scripts\activate    # Activate virtual environment
```
4. Install the project and its dependencies

```bash
pip install -r requirements.txt    # Install the dependencies
python setup.py install            # Install the project
```

Check out the subsequent sections to understand how to use the project.

### Validate EM-DAT Content


First, import `pandas` and the `emdat_schema` defined in `emtest` using
`pandera`. EM-DAT data can be loaded and parsed into a `pandas.DataFrame`, then
validated using the `emdat_schema.validate` method.

```python
import pandas as pd
from emtest import emdat_schema
emdat = pd.read_excel(
        PATH_TO_EMDAT_XLSX_FILE, # Replace with you file
        index_col='DisNo.',
        parse_dates=['Entry Date', 'Last Update']
)
emdat_schema.validate(emdat)
```

See the "examples" folder of this repository.

## Useful Links

- [EM-DAT Project Website](https://www.emdat.be/)
- [EM-DAT Project Documentation](https://doc.emdat.be)
- [EM-DAT Data Download Portal](https://public.emdat.be/)
- [Pandera Documentation: the Open-source Framework for Precision Data Testing](https://pandera.readthedocs.io/en/stable/index.html)

