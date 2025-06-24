from flask import Flask, jsonify
from bson.binary import Binary, UUID_SUBTYPE
from DB import db
import uuid




if db is not None:
    users = db.users
else:
    users = None


files = db.files
downloads = db.downloads

class FileSys():
    
    def fileSave(self, filename, uploadedBy, url):
        fileId = Binary(uuid.uuid4().bytes, UUID_SUBTYPE)
        
        data = {
            "id": fileId,
            "filename": filename.filename,
            "uploadedBy": uploadedBy,
            "url": url["secure_url"],
            "publicID": url["public_id"],
            "downloadFile": str(uuid.uuid4())
        }
        
        files.insert_one(data)
        return data
    
    def getAll(self):
        return list(files.find({}, {"_id": 0}))
    
    def getFile(self, id):
        print("Asking for file id", id)
        
        fileData = files.find_one({"downloadFile": id})
        return fileData
    
fileModel = FileSys() 
