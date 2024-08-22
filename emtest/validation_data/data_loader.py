from pathlib import Path

import pandas as pd
import toml

CLASSIFICATION_FILE = Path(
    f"{Path(__file__).parent}/classification_tree.toml")

# accessed 24.07.02
AREAS_FILE = Path(
    f"{Path(__file__).parent}/UNSD_M49_standards.csv")


def load_classification(file: Path = CLASSIFICATION_FILE):
    """Load classification tree from toml file and return it as a dataframe

    Parameters
    ----------
    file : str
        file path to toml file

    Returns
    -------
    pd.DataFrame

    Example
    -------

    >>> df = load_classification('classification_tree.toml')
    >>> df.loc[0]
    classif_key    nat-bio-ani-ani
    group                  Natural
    subgroup            Biological
    type           Animal incident
    subtype        Animal incident
    Name: 0, dtype: object

    """
    data = toml.load(file)
    rows = data['rows']
    df = pd.DataFrame(rows)
    return df


def load_UNSD_areas(file: Path = AREAS_FILE):
    """Load unsd area codes from csv file and return it as a dataframe

    Parameters
    ----------
    file : str
        file path to csv file

    Returns
    -------
    pd.DataFrame

    References
    ----------
    https://unstats.un.org/unsd/methodology/m49/overview/

    Example
    -------

    >>> df = load_UNSD_areas('UNSD_M49_standards.csv')
    >>> df.loc[0]
    Global Code                                              1
    Global Name                                          World
    Region Code                                            2.0
    Region Name                                         Africa
    Sub-region Code                                       15.0
    Sub-region Name                            Northern Africa
    Intermediate Region Code                               NaN
    Intermediate Region Name                               NaN
    Country or Area                                    Algeria
    M49 Code                                                12
    ISO-alpha2 Code                                         DZ
    ISO-alpha3 Code                                        DZA
    Least Developed Countries (LDC)                        NaN
    Land Locked Developing Countries (LLDC)                NaN
    Small Island Developing States (SIDS)                  NaN
    Name: 0, dtype: object
    """
    df = pd.read_csv(file, sep=';')
    return df


if __name__ == '__main__':
    import doctest

    doctest.testmod()
