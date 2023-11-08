from firebase_admin import firestore


def create_group(name, bio, image, is_private, journey_id, meeting_link, church_id, group_code):
    db = firestore.client()
    church_ref = db.collection("churches").document(church_id)
    church = church_ref.get()
    church = church.to_dict()
    church_name = church["title"]
    group = {"name": name, "bio": bio, "image": image, "is_private": is_private, "journey_id": journey_id, "meeting_link": meeting_link, "church_id": church_id, "church_name": church_name, "members": {}, "group_code": group_code, "is_active": True}
    update_time, group_ref = db.collection("groups").add(group)
    return group_ref
