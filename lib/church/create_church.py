from firebase_admin import firestore


def create_church_in_database(title, website, address, bio, contact):
    db = firestore.client()
    church = {"title": title, "website": website, "address": address, "bio": bio, "contact": contact}
    update_time, church_ref = db.collection("churches").add(church)
    return
