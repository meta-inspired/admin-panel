from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter


def get_churches(church_name="none"):
    db = firestore.client()
    churches = []
    if church_name == "none":
        docs = db.collection("churches").stream()
    else:
        docs = db.collection("churches").where(filter=FieldFilter("name", "==", church_name)).stream()
    for doc in docs:
        church = doc.to_dict()
        church["id"] = doc.id
        churches.append(church)

    return churches
