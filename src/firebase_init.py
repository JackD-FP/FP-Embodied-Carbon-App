import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("creds/creds.json")
fp_app = firebase_admin.initialize_app(
    cred,
    {
        "storageBucket": "embodied-carbon.appspot.com",
    },
)
db = firestore.client()
bucket = storage.bucket(app=fp_app)
