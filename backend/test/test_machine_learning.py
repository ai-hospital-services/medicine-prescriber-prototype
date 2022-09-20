import array as arr

import api.machine_learning


class MockSymptomsTokeniser:
    def texts_to_sequences(_, corpus):
        return [[1, 2, 3]]

    word_index = {
        "test subjective symptom": 1,
        "test objective symptom": 2,
        "test gender": 3,
    }


class MockCausesTokeniser:
    index_word = {
        1: "test cause 1",
        2: "test cause 2",
        3: "test cause 3",
    }


class MockModel:
    def predict(_, symptoms_padded):
        return [[0.5, 0.25, 0.15, 0.04, 0.03, 0.01, 0.01, 0.01]]


class TestMachineLearning:
    def mock_pad_sequences(sequence, padding, maxlen):
        return [[0, 0, 0, 0, 0, 0, 1, 2, 3]]

    def mock_array(array):
        return arr.array("i", [0, 0, 0, 0, 0, 0, 1, 2, 3])

    def mock_argsort(array):
        return arr.array("i", [7, 6, 5, 4, 3, 2, 1, 0])

    def test_predict_cause(_, mocker):
        # arrange
        mocker.patch.object(
            api.machine_learning.State, "SYMPTOMS_TOKENISER", MockSymptomsTokeniser()
        )
        mocker.patch(
            "api.machine_learning.tf.keras.preprocessing.sequence.pad_sequences",
            TestMachineLearning.mock_pad_sequences,
        )
        mocker.patch("api.machine_learning.np.array", TestMachineLearning.mock_array)
        mocker.patch.object(api.machine_learning.State, "MODEL", MockModel())
        mocker.patch(
            "api.machine_learning.np.argsort", TestMachineLearning.mock_argsort
        )
        mocker.patch.object(
            api.machine_learning.State, "CAUSES_TOKENISER", MockCausesTokeniser()
        )
        spy_symptoms_tokeniser_texts_to_sequences = mocker.spy(
            api.machine_learning.State.SYMPTOMS_TOKENISER,
            "texts_to_sequences",
        )
        spy_tf_pad_sequences = mocker.spy(
            api.machine_learning.tf.keras.preprocessing.sequence,
            "pad_sequences",
        )
        spy_numpy_array = mocker.spy(
            api.machine_learning.np,
            "array",
        )
        spy_model_predict = mocker.spy(
            api.machine_learning.State.MODEL,
            "predict",
        )
        spy_numpy_argsort = mocker.spy(
            api.machine_learning.np,
            "argsort",
        )

        # act
        result = api.machine_learning.predict_cause(
            "test subjective symptom", "test objective symptom", "test gender"
        )

        # assert
        spy_symptoms_tokeniser_texts_to_sequences.assert_called_once_with(
            ["test subjective symptom;test objective symptom;test gender"]
        )
        spy_tf_pad_sequences.assert_called_once_with(
            [[1, 2, 3]], padding="pre", maxlen=9
        )
        spy_numpy_array.assert_called_once_with([[0, 0, 0, 0, 0, 0, 1, 2, 3]])
        spy_model_predict.assert_called_once_with(
            arr.array("i", [0, 0, 0, 0, 0, 0, 1, 2, 3])
        )
        spy_numpy_argsort.assert_called_once_with(
            [0.5, 0.25, 0.15, 0.04, 0.03, 0.01, 0.01, 0.01]
        )
        assert result == [
            ("test cause 1", 50.00),
            ("test cause 2", 25.00),
            ("test cause 3", 15.00),
        ]
