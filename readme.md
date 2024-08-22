# EM-TEST

EM-TEST is a testing framework for the [EM-DAT](www.emdat.be) public data
relying on the [`pandas`]() and [`pandera`]() Python packages.

## TODO

- [ ] Add useful error messages
- [ ] Add warnings (use lazy error validation and flag desired error as
  warnings)
- [ ] Validate admin units
- [ ] Validate entry and last updated.
- [ ] Allow for negative magnitude
- [ ] Add data for test cases

## Why using EM-TEST?

The EM-DAT database is a long-lasting project that has started in 1988. In the
past, data was encoded manually sometimes using free text fields without
constraints. The EM-TEST framework was initially developed to identify issues
in the data, prior to the redesign of the database. EM-TEST is now redundant
with many existing constraints in the EM-DAT database. So, why using EM-TEST?
Here is five reasons:

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

## How EM-TEST Works?

## EM-DAT Validation Scheme

EM-DAT validation scheme is available with the command:
```python
from emtest import emdat_schema 
```

### Data Type Validation

| Column                                    | Type      | Nullable | Unique |
|-------------------------------------------|-----------|----------|--------|
| DisNo.                                    | str       | False    | True   |
| Historic                                  | str       | False    | False  |
| Classification Key                        | str       | False    | False  |
| Disaster Group                            | str       | False    | False  |
| Disaster Subgroup                         | str       | False    | False  |
| Disaster Type                             | str       | False    | False  |
| Disaster Subtype                          | str       | False    | False  |
| External IDs                              | str       | True     | False  |
| Event Name                                | str       | True     | False  |
| ISO                                       | str       | False    | False  |
| Country                                   | str       | False    | False  |
| Subregion                                 | str       | False    | False  |
| Region                                    | str       | False    | False  |
| Location                                  | str       | True     | False  |
| Origin                                    | str       | True     | False  |
| Associated Types                          | str       | True     | False  |
| OFDA/BHA Response                         | str       | False    | False  |
| Appeal                                    | str       | False    | False  |
| Declaration                               | str       | False    | False  |
| AID Contribution ('000 US$)               | float     | True     | False  |
| Magnitude                                 | float     | True     | False  |
| Magnitude Scale                           | str       | True     | False  |
| Latitude                                  | float     | True     | False  |
| Longitude                                 | float     | True     | False  |
| River Basin                               | str       | True     | False  |
| Start Year                                | int       | False    | False  |
| Start Month                               | float[^1] | True     | False  |
| Start Day                                 | float[^1] | True     | False  |
| End Year                                  | int       | False    | False  |
| End Month                                 | float[^1] | True     | False  |
| End Day                                   | float[^1] | True     | False  |
| Total Deaths                              | float[^1] | True     | False  |
| No. Injured                               | float[^1] | True     | False  |
| No. Affected                              | float[^1] | True     | False  |
| No. Homeless                              | float[^1] | True     | False  |
| Total Affected                            | float[^1] | True     | False  |
| Reconstruction Costs ('000 US$)           | float     | True     | False  |
| Reconstruction Costs, Adjusted ('000 US$) | float     | True     | False  |
| Insured Damage ('000 US$)                 | float     | True     | False  |
| Insured Damage, Adjusted ('000 US$)       | float     | True     | False  |
| Total Damage ('000 US$)                   | float     | True     | False  |
| Total Damage, Adjusted ('000 US$)         | float     | True     | False  |
| CPI                                       | float     | True     | False  |
| Admin Units                               | str       | True     | False  |
| Entry Date                                | Timestamp | False    | False  |
| Last Update                               | Timestamp | False    | False  |

[^1]: Integer type in Python is not nullable, hence these values are typed as
float numbers.

### Column Checks

For each column in EM-DAT, `pandera` makes it possible to test and validate
column's content with [Checks](https://pandera.readthedocs.io/en/stable/checks.html).
The current checks are listed in the table below. 

| Column                                    | Test Name                        | Test Description                                         | Test Type |
|-------------------------------------------|----------------------------------|----------------------------------------------------------|-----------|
| DisNo.                                    | check_disno                      | Validate value using regular expression.                 | Error     |
| Historic                                  | check_yes_no                     | Test whether value is either 'Yes' or 'No'.              | Error     |
| Classification Key                        | check_classification_key         | Test whether value is in the reference list.             | Error     |
| Disaster Group                            | check_group                      | Test whether value is in the reference list.             | Error     |
| Disaster Subgroup                         | check_subgroup                   | Test whether value is in the reference list.             | Error     |
| Disaster Type                             | check_type                       | Test whether value is in the reference list.             | Error     |
| Disaster Subtype                          | check_subtype                    | Test whether value is in the reference list.             | Error     |
| External IDs                              | validate_external_id             | Validate values using regular expressions.               | Error     |
| Event Name                                | -                                | -                                                        | -         |
| ISO                                       | validate_iso3_code               | Validate values using regular expressions.               | Error     |
|                                           | check_iso3_code                  | Test whether value is in the reference list.             | Warning   |
| Country                                   | check_country                    | Test whether value is in the reference list.             | Warning   |
| Subregion                                 | check_subregion                  | Test whether value is in the reference list.             | Error     |
| Region                                    | check_region                     | Test whether value is in the reference list.             | Error     |
| Location                                  | -                                | -                                                        | -         |
| Origin                                    | -                                | -                                                        | -         |
| Associated Types                          | -                                | -                                                        | -         |
| OFDA/BHA Response                         | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| Appeal                                    | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| Declaration                               | check_yes_no                     | Test whether value is either 'Yes' or 'No'               | Error     |
| AID Contribution ('000 US$)               | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Magnitude                                 | not_equal_to(0.)                 | Test whether value differ from 0.                        | Error     |
| Magnitude Scale                           | check_magnitude_unit             | Test whether value is in the reference list.             | Error     |
| Latitude                                  | in_range(-90., 90.)              | Test whether value is within range -90-90.               | Error     |
| Longitude                                 | in_range(-180., 180.)            | Test whether value is within range -180-180.             | Error     |
| River Basin                               | -                                | -                                                        | -         |
| Start Year                                | in_range(1900, CURRENT_YEAR)     | Test whether value is within range 1900-{CURRENT_YEAR}.  | Error     |
| Start Month                               | check_month                      | Test whether value is a valid month number (1-12).       | Error     |
| Start Day                                 | check_day                        | Test whether value is a valid day number (1-31).         | Error     |
| End Year                                  | in_range(1900, CURRENT_YEAR)     | Test whether value is within range 1900-{CURRENT_YEAR}.  | Error     |
| End Month                                 | check_month                      | Test whether value is a valid month number (1-12).       | Error     |
| End Day                                   | check_day                        | Test whether value is a valid day number (1-31).         | Error     |
| Total Deaths                              | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| No. Injured                               | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| No. Affected                              | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| No. Homeless                              | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Total Affected                            | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Reconstruction Costs ('000 US$)           | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Reconstruction Costs, Adjusted ('000 US$) | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Insured Damage ('000 US$)                 | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Insured Damage, Adjusted ('000 US$)       | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Total Damage ('000 US$)                   | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| Total Damage, Adjusted ('000 US$)         | greater_than(0.)                 | Test whether value is greater than 0.                    | Error     |
| CPI                                       | in_range(0., 100.)               | Test whether value is within range 0-100.                | Error     |
| Admin Units                               | is_valid_json                    | Test whether value is a json string.                     | Error     |
| Entry Date                                | in_range(1988/1/1, CURRENT_DATE) | Test whether value is within valid date range.           | Error     |
| Last Update                               | in_range(1988/1/1, CURRENT_DATE) | Test whether value is within valid date range.           | Error     |

## How to Use?

### Installation

```
pip install
```

### Validate EM-DAT Content

### Type-specific Validation



None

## Useful Links

- [EM-DAT Project Website](www.emdat.be)
- [EM-DAT Project Documentation](https://doc.emdat.be)
- [EM-DAT Data Download Portal](https://public.emdat.be/)
- [Pandera Documentation: the Open-source Framework for Precision Data Testing](https://pandera.readthedocs.io/en/stable/index.html)

## References

```
@InProceedings{ niels_bantilan-proc-scipy-2020,
  author    = { {N}iels {B}antilan },
  title     = { pandera: {S}tatistical {D}ata {V}alidation of {P}andas {D}ataframes },
  booktitle = { {P}roceedings of the 19th {P}ython in {S}cience {C}onference },
  pages     = { 116 - 124 },
  year      = { 2020 },
  editor    = { {M}eghann {A}garwal and {C}hris {C}alloway and {D}illon {N}iederhut and {D}avid {S}hupe },
  doi       = { 10.25080/Majora-342d178e-010 }
}
```