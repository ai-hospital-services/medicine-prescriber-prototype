from bson import json_util
from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        existing_collections = self.db.list_collection_names()

        path = "./api/migrations/data/20230203030416_0.5.0"
        with open(f"{path}/subjective_symptoms.json", "r") as file:
            data = file.read()
            data = json_util.loads(data)
            self.db.subjective_symptoms.insert_many(data)
        with open(f"{path}/assoicated_symptoms.json", "r") as file:
            data = file.read()
            data = json_util.loads(data)
            self.db.assoicated_symptoms.insert_many(data)

        # for collection in existing_collections:
        #     self.db[collection].drop()

    def downgrade(self):
        if self.db.assoicated_symptoms is not None:
            self.db.assoicated_symptoms.drop()
        if self.db.subjective_symptoms is not None:
            self.db.subjective_symptoms.drop()
