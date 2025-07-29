from flask import Flask, jsonify
from bson.binary import Binary, UUID_SUBTYPE
from DB import db
import uuid

if db is not None:
    users = db.users # Ensure this is correct, but users collection is not used in FileSys class directly
    files = db.files
    downloads = db.downloads # If downloads collection is not used, consider removing it or adding logic for it
else:
    users = None
    files = None # Initialize to None if db is None
    downloads = None # Initialize to None if db is None

class FileSys():

    def fileSave(self, filename_str, uploadedBy, url_data): # Accept filename as string and url_data dict
        if files is None:
            return None # Handle case where db connection failed

        fileId = Binary(uuid.uuid4().bytes, UUID_SUBTYPE)

        data = {
            "id": fileId,
            "filename": filename_str, # Use the passed string filename
            "uploadedBy": uploadedBy,
            "url": url_data["secure_url"],
            "publicID": url_data["public_id"],
            "downloadFile": str(uuid.uuid4()) # Unique ID for download link
        }

        files.insert_one(data)
        return data

    def getAll(self):
        if files is None:
            return [] # Return empty list if db connection failed
        return list(files.find({}, {"_id": 0}))

    def getFile(self, id):
        if files is None:
            return None # Handle case where db connection failed

        print("Asking for file id", id)

        fileData = files.find_one({"downloadFile": id})
        return fileData

fileModel = FileSys()