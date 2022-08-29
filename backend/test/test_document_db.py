import api.document_db
from bson.objectid import ObjectId


class MockSubjectiveSymptoms:
    def find(_, filter):
        return [
            {"_id": ObjectId("63083e7c5b96e72df489b67d"), "symptom": "test symptom"}
        ]


class MockObjectiveSymptoms:
    def find(_, filter):
        return [
            {
                "_id": ObjectId("63083f3e5b96e72df489b683"),
                "symptom": "test symptom",
                "subjective_symptom_id": ObjectId("63083e7c5b96e72df489b67d"),
            }
        ]


class MockEtiologies:
    def find(_, filter):
        return [
            {
                "_id": ObjectId("630840445b96e72df489b6a7"),
                "cause": "test cause",
                "etiology": "test etiology",
                "subjective_symptom_id": ObjectId("63083e7c5b96e72df489b67d"),
            }
        ]

    def find_one(_, filter):
        return {
            "_id": ObjectId("630840445b96e72df489b6a7"),
            "cause": filter["cause"],
            "etiology": "test etiology",
            "subjective_symptom_id": ObjectId(filter["subjective_symptom_id"]),
        }


class MockDrugs:
    def find(_, filter):
        return [
            {
                "_id": ObjectId("6308420c5b96e72df489b6b9"),
                "dose": "test dose",
                "drug_category": "test drug category",
                "drug_use": "test drug use",
                "etiology_id": ObjectId(filter["etiology_id"]),
                "mode_of_action": "test mode of action",
            }
        ]


class MockDatabase:
    subjective_symptoms = MockSubjectiveSymptoms()
    objective_symptoms = MockObjectiveSymptoms()
    etiologies = MockEtiologies()
    drugs = MockDrugs()


class MockServer:
    ai_hospital_services = MockDatabase()


class TestDocumentDB:
    def test_read_all_subjective_symptoms(_, mocker):
        # arrange
        mocker.patch.object(api.document_db.State, "MONGODB_CLIENT", MockServer())
        spy_subjective_symptoms_find = mocker.spy(
            api.document_db.State.MONGODB_CLIENT.ai_hospital_services.subjective_symptoms,
            "find",
        )

        # act
        result = api.document_db.read_all_subjective_symptoms()

        # assert
        spy_subjective_symptoms_find.assert_called_once_with({})
        assert result[0] == {
            "_id": "63083e7c5b96e72df489b67d",
            "symptom": "test symptom",
        }

    def test_read_all_objective_symptoms(_, mocker):
        # arrange
        mocker.patch.object(api.document_db.State, "MONGODB_CLIENT", MockServer())
        spy_objective_symptoms_find = mocker.spy(
            api.document_db.State.MONGODB_CLIENT.ai_hospital_services.objective_symptoms,
            "find",
        )

        # act
        result = api.document_db.read_all_objective_symptoms()

        # assert
        spy_objective_symptoms_find.assert_called_once_with({})
        assert result[0] == {
            "_id": "63083f3e5b96e72df489b683",
            "symptom": "test symptom",
            "subjective_symptom_id": "63083e7c5b96e72df489b67d",
        }

    def test_read_all_etiologies(_, mocker):
        # arrange
        mocker.patch.object(api.document_db.State, "MONGODB_CLIENT", MockServer())
        spy_etiologies_find = mocker.spy(
            api.document_db.State.MONGODB_CLIENT.ai_hospital_services.etiologies,
            "find",
        )

        # act
        result = api.document_db.read_all_etiologies()

        # assert
        spy_etiologies_find.assert_called_once_with({})
        assert result[0] == {
            "_id": "630840445b96e72df489b6a7",
            "cause": "test cause",
            "etiology": "test etiology",
            "subjective_symptom_id": "63083e7c5b96e72df489b67d",
        }

    def test_read_etiology(_, mocker):
        # arrange
        mocker.patch.object(api.document_db.State, "MONGODB_CLIENT", MockServer())
        spy_etiology_find_one = mocker.spy(
            api.document_db.State.MONGODB_CLIENT.ai_hospital_services.etiologies,
            "find_one",
        )

        # act
        result = api.document_db.read_etiology("63083e7c5b96e72df489b67d", "test cause")

        # assert
        spy_etiology_find_one.assert_called_once_with(
            {
                "subjective_symptom_id": ObjectId("63083e7c5b96e72df489b67d"),
                "cause": "test cause",
            }
        )
        assert result == str(
            {
                "_id": "630840445b96e72df489b6a7",
                "cause": "test cause",
                "etiology": "test etiology",
                "subjective_symptom_id": "63083e7c5b96e72df489b67d",
            }
        )

    def test_read_drugs(_, mocker):
        # arrange
        mocker.patch.object(api.document_db.State, "MONGODB_CLIENT", MockServer())
        spy_drugs_find = mocker.spy(
            api.document_db.State.MONGODB_CLIENT.ai_hospital_services.drugs,
            "find",
        )

        # act
        result = api.document_db.read_drugs("630840445b96e72df489b6a7")

        # assert
        spy_drugs_find.assert_called_once_with(
            {"etiology_id": ObjectId("630840445b96e72df489b6a7")}
        )
        assert result[0] == {
            "_id": "6308420c5b96e72df489b6b9",
            "dose": "test dose",
            "drug_category": "test drug category",
            "drug_use": "test drug use",
            "etiology_id": "630840445b96e72df489b6a7",
            "mode_of_action": "test mode of action",
        }
