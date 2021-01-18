from pymongo import MongoClient
from os import getenv
from sentry_sdk import capture_exception, capture_message

class DatabaseManager:
    def __init__(self):
        # Connection made with mongoDb database
        connection = MongoClient(
            getenv('MONGODB_URI'),
            tls=True,
            tlsCertificateKeyFile=getenv('MONGODB_CON_CERT_FILE'))
        db = connection['State']
        self.collection = db['OHIO']

    # record will be verified to be unique before adding into database
    def ifIndexExists(self , number):
        return self.collection\
            .count_documents({"Crash Number":number}) != 0

    # Insert a single record in database
    def insert_record(self , record):
        self.collection\
            .insert_one(record)

    