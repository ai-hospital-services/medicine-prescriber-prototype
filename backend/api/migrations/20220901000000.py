from bson import json_util
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        existing_collections = self.db.list_collection_names()

        path = "./api/migrations/data/20220901000000"
        with (open(f"{path}/subjective_symptoms.json", "r") as file):
            data = file.read()
            data = json_util.loads(data)
            self.db.subjective_symptoms.insert_many(data)
        with (open(f"{path}/objective_symptoms.json", "r") as file):
            data = file.read()
            data = json_util.loads(data)
            self.db.objective_symptoms.insert_many(data)
        with (open(f"{path}/etiologies.json", "r") as file):
            data = file.read()
            data = json_util.loads(data)
            self.db.etiologies.insert_many(data)
        with (open(f"{path}/drugs.json", "r") as file):
            data = file.read()
            data = json_util.loads(data)
            self.db.drugs.insert_many(data)

        for collection in existing_collections:
            self.db[collection].drop()

    def downgrade(self):
        if self.db.drugs is not None:
            self.db.drugs.drop()
        if self.db.etiologies is not None:
            self.db.etiologies.drop()
        if self.db.objective_symptoms is not None:
            self.db.objective_symptoms.drop()
        if self.db.subjective_symptoms is not None:
            self.db.subjective_symptoms.drop()
