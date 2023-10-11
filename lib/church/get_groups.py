from firebase_admin import firestore


def get_groups():
    db = firestore.client()
    church_docs = db.collection("churches").stream()
    churches = {}
    for doc in church_docs:
        church = doc.to_dict()
        churches[doc.id] = church["title"]

    group_docs = db.collection("groups").stream()
    groups = []
    for doc in group_docs:
        group_members = ""
        group = {}
        group_document = doc.to_dict()
        group["name"] = group_document["name"]
        if "church_id" in group_document:
            group["church_Name"] = churches[group_document["church_id"]]
        if "group_id" in group_document:
            group["group_id"] = group_document["group_id"]
        group["bio"] = group_document["bio"]
        for member in group_document["members"]:
            member_ref = db.collection("users").document(member)
            member_document = member_ref.get()
            user = member_document.to_dict()
            if "fullName" in user:
                group_members = group_members + user["fullName"] + " : " + group_document["members"][member] + " <br> "
            else:
                group_members = group_members + member + " : " + group_document["members"][member] + " <br> "

        group["members"] = group_members

        groups.append(group)

    return groups
