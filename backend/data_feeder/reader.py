from dataclasses import dataclass

import pandas as pd


@dataclass(init=True)
class AssociativeSymptom:
    """Class for associative symptom."""

    symptom: str = None
    subjective_symptom: str = None


@dataclass(init=True)
class ProvisionalDiagnosisAdvise:
    """Class for provisional diagnosis advise."""

    provisional_diagnosis: str = None

    @dataclass(init=True)
    class Advise:
        advised_investigations: list[str]
        management: str = None
        surgical_management: str = None

    advises: list[Advise] = None


def fetch_subjective_symptoms() -> list[str]:
    """Function to fetch subjective symptoms."""
    data = _load_clean_data()
    return pd.unique(data.subjective_symptom.dropna())


def fetch_associated_symptoms() -> list[AssociativeSymptom]:
    """Function to fetch associated symptoms."""
    data = _load_clean_data()
    associated_symptoms = []
    for _, row in data.iterrows():
        associated_symptoms_split = row.associated_symptoms.split("|")
        for associated_symptom in associated_symptoms_split:
            find = [
                x
                for x in associated_symptoms
                if x.symptom == associated_symptom
                and x.subjective_symptom == row.subjective_symptom
            ]
            if len(find) == 0:
                associated_symptoms.append(
                    AssociativeSymptom(
                        symptom=associated_symptom,
                        subjective_symptom=row.subjective_symptom,
                    )
                )
    return associated_symptoms


def fetch_gender() -> list[str]:
    """Function to fetch gender."""
    data = _load_clean_data()
    return pd.unique(data.gender.dropna())


def fetch_age_groups() -> list[str]:
    """Function to fetch age groups."""
    data = _load_clean_data()
    return pd.unique(data.age.dropna())


def fetch_investigations() -> list[str]:
    """Function to fetch investigations."""
    data = _load_clean_data()
    investigations = []
    for _, row in data.iterrows():
        if pd.isna(row.investigations_done):
            continue
        investigations_split = row.investigations_done.split("|")
        for i in investigations_split:
            find = [x for x in investigations if x == i]
            if len(find) == 0:
                investigations.append(i)
    return investigations


def fetch_provisional_diagnosis_advises() -> list[ProvisionalDiagnosisAdvise]:
    """Function to fetch provisional diagnosis advises."""
    data = _load_clean_data()
    result = []
    for _, row in data.iterrows():
        if pd.isna(row.subjective_symptom) or pd.isna(row.provisional_diagnosis):
            continue

        provisional_diagnosis = row.subjective_symptom + "|" + row.provisional_diagnosis
        advised_investigations = (
            "" if pd.isna(row.advised_investigations) else row.advised_investigations
        )
        management = "" if pd.isna(row.management) else row.management
        surgical_management = (
            "" if pd.isna(row.surgical_management) else row.surgical_management
        )
        newAdvise = ProvisionalDiagnosisAdvise.Advise(
            advised_investigations=advised_investigations,
            management=management,
            surgical_management=surgical_management,
        )

        existing = False
        for provisional_diagnosis_advise in result:
            if (
                provisional_diagnosis_advise.provisional_diagnosis
                == provisional_diagnosis
            ):
                adviseFound = False
                for advise in provisional_diagnosis_advise.advises:
                    if advise == newAdvise:
                        adviseFound = True
                        break
                if not adviseFound:
                    provisional_diagnosis_advise.advises.append(newAdvise)
                existing = True
        if not existing:
            result.append(
                ProvisionalDiagnosisAdvise(
                    provisional_diagnosis=provisional_diagnosis, advises=[newAdvise]
                )
            )

    return result


# def fetch_advised_investigations() -> list[str]:
#     """Function to fetch advised investigations."""
#     data = _load_clean_data()
#     return pd.unique(data.advised_investigations.dropna())


# def fetch_management() -> list[str]:
#     """Function to fetch management."""
#     data = _load_clean_data()
#     return pd.unique(data.management.dropna())


# def fetch_surgical_management() -> list[str]:
#     """Function to fetch surgical management."""
#     data = _load_clean_data()
#     return pd.unique(data.surgical_management.dropna())


def _load_clean_data():
    # load
    data = pd.read_csv("./data/data_processed.txt", sep="\t")
    # remove all na rows
    data = data.dropna(axis=0, how="all")
    # remove all na columns
    data = data.dropna(axis=1, how="all")
    # strip strings
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    return data
