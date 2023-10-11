from firebase_admin import firestore
from firebase_admin import auth
from google.cloud.firestore_v1.base_query import FieldFilter


def create_user(display_name, email, password, group_id="", is_group_leader=False):
    db = firestore.client()
    user = auth.create_user(display_name=display_name, email=email, password=password)
    user_db = {"fullName": display_name, "currentQuest": {"chapter": 1, "journey": 1, "quest": 0}, "isCommunityMember": False, "isFirstLogin": False}
    db.collection("users").document(user.uid).set(user_db)
    if group_id != "":
        group_collection = db.collection("groups")
        groups_ref = group_collection.where(filter=FieldFilter("group_id", "==", group_id)).stream()
        for doc in groups_ref:
            group_members = doc.to_dict()["members"]
            group_members[user.uid] = "admin"
            group_ref = db.collection("groups").document(doc.id)
            group_ref.update({"members": group_members})
    return

