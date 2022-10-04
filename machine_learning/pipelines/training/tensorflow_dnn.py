import json
import os
from typing import NamedTuple

import kfp
import kfp.components as comp
import kfp.dsl as dsl


def download_file_from_gcs_bucket(
    gcs_bucket_name: str, file_name: str, downloaded_path: comp.OutputPath()
):
    """Function to download data from gcs bucket."""
    from google.cloud import storage

    client = storage.Client()
    bucket = client.bucket(gcs_bucket_name)
    blob = bucket.blob(file_name)
    blob.download_to_filename(downloaded_path)


download_file_from_gcs_bucket_op = kfp.components.create_component_from_func(
    download_file_from_gcs_bucket,
    output_component_file="download_file_from_gcs_bucket.yaml",
    # base_image="python:3.9.14-slim-buster",
    # packages_to_install=["google-cloud-storage~=2.5.0"]
    base_image="asia.gcr.io/ai-hospital-services-prototype/machine_learning_training:tensorflow_dnn",
)


def train_model(
    data_path: comp.InputPath(),
    symptoms_tokeniser_path: comp.OutputPath(),
    causes_tokeniser_path: comp.OutputPath(),
    model_path: comp.OutputPath(),
):
    """Function to train model."""
    import numpy as np
    import pandas as pd
    import tensorflow as tf

    data = pd.read_csv(data_path, sep="|")
    data.describe()
    data.columns = data.columns.str.lower().str.replace(" ", "_")
    data.head()
    symptoms_corpus = (
        data.subjective_symptom + ";" + data.objective_symptom + ";" + data.gender
    )
    symptoms_corpus = list(map(lambda item: item.replace("; ", ";"), symptoms_corpus))
    symptoms_corpus = list(map(lambda item: item.replace(" ;", ";"), symptoms_corpus))
    print(symptoms_corpus)

    symptoms_tokeniser = tf.keras.preprocessing.text.Tokenizer(
        split=";",
        filters="",
    )
    symptoms_tokeniser.fit_on_texts(symptoms_corpus)
    print(symptoms_tokeniser.index_word)

    symptoms_sequences = symptoms_tokeniser.texts_to_sequences(symptoms_corpus)
    print(symptoms_sequences)

    symptoms_padded = tf.keras.preprocessing.sequence.pad_sequences(
        symptoms_sequences, padding="pre"
    )
    symptoms_padded = np.array(symptoms_padded)
    print(symptoms_padded)

    causes_corpus = data.subjective_symptom + "|" + data.cause
    print(causes_corpus)

    causes_tokeniser = tf.keras.preprocessing.text.Tokenizer(
        split="\n",
        filters="",
    )
    causes_tokeniser.fit_on_texts(causes_corpus)
    print(causes_tokeniser.index_word)

    causes_sequences = causes_tokeniser.texts_to_sequences(causes_corpus)
    print(causes_sequences)

    causes_padded = tf.keras.preprocessing.sequence.pad_sequences(
        causes_sequences, padding="pre"
    )
    causes_padded = np.array(causes_padded) - 1
    print(causes_padded)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Embedding(
                input_dim=len(symptoms_tokeniser.index_word) + 1,
                output_dim=16,
                input_length=max(map(len, symptoms_padded)),
            ),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(8, activation="softmax"),
        ]
    )
    model.compile(
        loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"]
    )
    model.summary()

    tf.keras.backend.clear_session()
    tf.random.set_seed(42)
    model.fit(
        x=symptoms_padded,
        y=causes_padded,
        epochs=500,
        callbacks=[tf.keras.callbacks.TensorBoard(log_dir="logs")],
    )
    model.evaluate(x=symptoms_padded, y=causes_padded)

    with open(file=symptoms_tokeniser_path, mode="w") as f:
        f.write(symptoms_tokeniser.to_json())
    with open(file=causes_tokeniser_path, mode="w") as f:
        f.write(causes_tokeniser.to_json())
    model.save(f"{model_path}/model.h5")


train_model_op = kfp.components.create_component_from_func(
    train_model,
    output_component_file="train_model.yaml",
    base_image="asia.gcr.io/ai-hospital-services-prototype/machine_learning_training:tensorflow_dnn",
)


def test_model(
    symptoms_tokeniser_path: comp.InputPath(),
    causes_tokeniser_path: comp.InputPath(),
    model_path: comp.InputPath(),
) -> bool:
    """Function to test model."""
    import numpy as np
    import tensorflow as tf

    # TODO: read from train model step
    symptoms_padded_maxlen = 9

    with open(file=symptoms_tokeniser_path, mode="r") as f:
        loaded_symptoms_tokeniser = tf.keras.preprocessing.text.tokenizer_from_json(
            f.read()
        )
    with open(file=causes_tokeniser_path, mode="r") as f:
        loaded_causes_tokeniser = tf.keras.preprocessing.text.tokenizer_from_json(
            f.read()
        )
    loaded_model = tf.keras.models.load_model(f"{model_path}/model.h5")
    loaded_model.summary()

    test_symptoms = ["vomiting; cramping; feeling nausea; diarrhoea"]
    test_gender = ["female"]
    test_symptoms_corpus = [a + ";" + b for a in test_symptoms for b in test_gender]
    test_symptoms_corpus = test_symptoms_corpus[0].split(";")
    test_symptoms_corpus = [str(item).lower().strip() for item in test_symptoms_corpus]
    test_symptoms_corpus = ";".join(test_symptoms_corpus)
    print(test_symptoms_corpus)

    test_symptoms_sequences = loaded_symptoms_tokeniser.texts_to_sequences(
        [test_symptoms_corpus]
    )
    test_symptoms_padded = tf.keras.preprocessing.sequence.pad_sequences(
        test_symptoms_sequences,
        padding="pre",
        maxlen=symptoms_padded_maxlen,
    )
    test_symptoms_padded = np.array(test_symptoms_padded)
    print(test_symptoms_padded)

    test_causes_probabilities = loaded_model.predict(test_symptoms_padded)[0]
    print(test_causes_probabilities)

    test_causes_rankings = np.argsort(test_causes_probabilities).tolist()
    print(test_causes_rankings)
    print(loaded_causes_tokeniser.index_word)
    print(
        loaded_causes_tokeniser.index_word[test_causes_rankings[-1] + 1],
        round(test_causes_probabilities[test_causes_rankings[-1]] * 100, 2),
    )
    print(
        loaded_causes_tokeniser.index_word[test_causes_rankings[-2] + 1],
        round(test_causes_probabilities[test_causes_rankings[-2]] * 100, 2),
    )
    print(
        loaded_causes_tokeniser.index_word[test_causes_rankings[-3] + 1],
        round(test_causes_probabilities[test_causes_rankings[-3]] * 100, 2),
    )

    return (
        loaded_causes_tokeniser.index_word[test_causes_rankings[-1] + 1]
        == "vomiting|food poisoning"
    )


test_model_op = kfp.components.create_component_from_func(
    test_model,
    output_component_file="test_model.yaml",
    base_image="asia.gcr.io/ai-hospital-services-prototype/machine_learning_training:tensorflow_dnn",
)


def trained_files_to_gcs(
    test_result: bool,
    gcs_bucket_name: str,
    symptoms_tokeniser_path: comp.InputPath(),
    causes_tokeniser_path: comp.InputPath(),
    model_path: comp.InputPath(),
) -> bool:
    """Function to upload training output to gcs bucket."""
    from google.cloud import storage

    if not test_result:
        return

    client = storage.Client()
    bucket = client.bucket(gcs_bucket_name)

    with open(file=symptoms_tokeniser_path, mode="r") as file:
        blob = bucket.blob("symptoms_tokeniser.json")
        blob.upload_from_file(file)

    with open(file=causes_tokeniser_path, mode="r") as file:
        blob = bucket.blob("causes_tokeniser.json")
        blob.upload_from_file(file)

    with open(file=f"{model_path}/model.h5", mode="rb") as file:
        blob = bucket.blob("model.h5")
        blob.upload_from_file(file, content_type="bytes")

    return True


trained_files_to_gcs_op = kfp.components.create_component_from_func(
    trained_files_to_gcs,
    output_component_file="trained_files_to_gcs.yaml",
    base_image="asia.gcr.io/ai-hospital-services-prototype/machine_learning_training:tensorflow_dnn",
)


def trained_files_to_base64(
    test_result: bool,
    symptoms_tokeniser_path: comp.InputPath(),
    causes_tokeniser_path: comp.InputPath(),
    model_path: comp.InputPath(),
) -> NamedTuple(
    "out",
    [
        ("symptoms_tokeniser_base64", "str"),
        ("causes_tokeniser_base64", "str"),
        ("model_base64", "str"),
    ],
):
    """Function to convert trained files to base64 encoded strings."""
    import base64

    if not test_result:
        return

    with open(file=symptoms_tokeniser_path, mode="r") as file:
        symptoms_tokeniser_content = file.read()
        symptoms_tokeniser_bytes = symptoms_tokeniser_content.encode("utf-8")
        symptoms_tokeniser_bytes_base64 = base64.encodebytes(symptoms_tokeniser_bytes)
        symptoms_tokeniser_base64 = symptoms_tokeniser_bytes_base64.decode(
            "utf-8"
        ).replace("\n", "")

    with open(file=causes_tokeniser_path, mode="r") as file:
        causes_tokeniser_content = file.read()
        causes_tokeniser_bytes = causes_tokeniser_content.encode("utf-8")
        causes_tokeniser_bytes_base64 = base64.encodebytes(causes_tokeniser_bytes)
        causes_tokeniser_base64 = causes_tokeniser_bytes_base64.decode("utf-8").replace(
            "\n", ""
        )

    with open(file=f"{model_path}/model.h5", mode="rb") as file:
        model_bytes = file.read()
        model_bytes_base64 = base64.encodebytes(model_bytes)
        model_base64 = model_bytes_base64.decode("utf-8").replace("\n", "")

    return (symptoms_tokeniser_base64, causes_tokeniser_base64, model_base64)


trained_files_to_base64_op = kfp.components.create_component_from_func(
    trained_files_to_base64,
    output_component_file="trained_files_to_base64.yaml",
    base_image="asia.gcr.io/ai-hospital-services-prototype/machine_learning_training:tensorflow_dnn",
)


@dsl.pipeline(
    name="Machine learning training pipeline - tensorflow dnn",
    description="Machine learning training pipeline for tensorflow dnn",
)
def training_tensorflow_dnn_pipeline(
    gcs_bucket_name, file_name, secret_name, secret_namespace
):
    """Function to run machine leaarning training pipeline using tensorflow dnn."""
    download_file_from_gcs_bucket_task = download_file_from_gcs_bucket_op(
        gcs_bucket_name=gcs_bucket_name,
        file_name=file_name,
    )
    download_file_from_gcs_bucket_task.container.set_image_pull_policy("Always")
    download_file_from_gcs_bucket_task.set_caching_options(False)
    download_file_from_gcs_bucket_task.execution_options.caching_strategy.max_cache_staleness = (
        "P0D"
    )
    # TODO: try pipeline based on arm64
    # download_file_from_gcs_bucket_task.add_toleration(
    #     {"key": "kubernetes.io/arch", "value": "arm64"}
    # )
    # download_file_from_gcs_bucket_task.add_node_selector_constraint(
    #     "kubernetes.io/arch", "arm64"
    # )

    train_model_task = train_model_op(
        data=download_file_from_gcs_bucket_task.outputs["downloaded"]
    )
    train_model_task.container.set_image_pull_policy("Always")
    train_model_task.set_caching_options(False)
    train_model_task.execution_options.caching_strategy.max_cache_staleness = "P0D"

    test_model_task = test_model_op(
        symptoms_tokeniser=train_model_task.outputs["symptoms_tokeniser"],
        causes_tokeniser=train_model_task.outputs["causes_tokeniser"],
        model=train_model_task.outputs["model"],
    )
    test_model_task.container.set_image_pull_policy("Always")
    test_model_task.set_caching_options(False)
    test_model_task.execution_options.caching_strategy.max_cache_staleness = "P0D"

    trained_files_to_gcs_task = trained_files_to_gcs_op(
        test_model_task.output,
        gcs_bucket_name=gcs_bucket_name,
        symptoms_tokeniser=train_model_task.outputs["symptoms_tokeniser"],
        causes_tokeniser=train_model_task.outputs["causes_tokeniser"],
        model=train_model_task.outputs["model"],
    )
    trained_files_to_gcs_task.container.set_image_pull_policy("Always")
    trained_files_to_gcs_task.set_caching_options(False)
    trained_files_to_gcs_task.execution_options.caching_strategy.max_cache_staleness = (
        "P0D"
    )

    trained_files_to_base64_task = trained_files_to_base64_op(
        test_model_task.output,
        symptoms_tokeniser=train_model_task.outputs["symptoms_tokeniser"],
        causes_tokeniser=train_model_task.outputs["causes_tokeniser"],
        model=train_model_task.outputs["model"],
    )
    trained_files_to_base64_task.container.set_image_pull_policy("Always")
    trained_files_to_base64_task.set_caching_options(False)
    trained_files_to_base64_task.execution_options.caching_strategy.max_cache_staleness = (
        "P0D"
    )

    k8s_manifest = """{
        "apiVersion": "v1",
        "kind": "Secret",
        "metadata": {
            "name": "<SECRET_NAME>",
            "namespace": "<SECRET_NAMESPACE>"
        },
        "type": "Opaque",
        "data": {
            "model.h5": "<MODEL_BASE64>"
        }
    }"""
    # "symptoms_tokeniser.json": "<SYMPTOMS_TOKENISER_BASE64>",
    # "causes_tokeniser.json": "<CAUSES_TOKENISER_BASE64>",

    k8s_resource_op = dsl.ResourceOp(
        name="Trained files to k8s testing secret",
        action="apply",
        k8s_resource=json.loads(
            k8s_manifest.replace("<SECRET_NAME>", f"{secret_name}").replace(
                "<SECRET_NAMESPACE>", f"{secret_namespace}"
            )
            # TODO: overcome the limitation of argument list too long issue: https://github.com/argoproj/argo-workflows/issues/7586
            #     "<SYMPTOMS_TOKENISER_BASE64>",
            #     f"{trained_files_to_base64_task.outputs['symptoms_tokeniser_base64']}",
            # )
            # .replace(
            #     "<CAUSES_TOKENISER_BASE64>",
            #     f"{trained_files_to_base64_task.outputs['causes_tokeniser_base64']}",
            # )
            .replace(
                "<MODEL_BASE64>",
                f"{trained_files_to_base64_task.outputs['model_base64']}",
            )
        ),
    )
    k8s_resource_op.set_caching_options(False)


kfp.compiler.Compiler().compile(
    pipeline_func=training_tensorflow_dnn_pipeline, package_path="pipeline.yaml"
)

client = kfp.Client(host="http://localhost:3000")
client.create_run_from_pipeline_func(
    training_tensorflow_dnn_pipeline,
    arguments={
        "gcs_bucket_name": f"{os.environ.get('GCS_STORAGE_BUCKET_NAME')}",
        "file_name": f"{os.environ.get('DATA_FILE_NAME')}",
        "secret_name": f"{os.environ.get('SECRET_NAME')}",
        "secret_namespace": f"{os.environ.get('SECRET_NAMESPACE')}",
    },
)
