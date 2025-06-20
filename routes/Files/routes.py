from flask import Blueprint, jsonify, request
import os
from datetime import datetime
from DB import db
from .models import fileModel
from utility.fileUpload_util import fileUpload
from utility.fileUpload_util import checkFileType

fileRoutes = Blueprint("files", __name__)
from ..User.models import userModel


@fileRoutes.route("/upload", methods=["POST"])
def uploadFile():
    file = request.files.get("file")
    email = request.form.get("email")

    user = userModel.getUserInfo(email=email)

    if user["userType"] != "ops":
        return (
            jsonify(
                {"msg": "client is not allowed to upload the files", "success": False}
            ),
            400,
        )

    if not file and checkFileType(file) == False:
        return (
            jsonify({"msg": f"{file} file not allowed", "success": False}),
            400,
        )

    url = fileUpload(file, file.filename)

    if not url:
        return jsonify({"msg": "upload failed", "success": False}), 500

    data = fileModel.fileSave(file, email, url)

    return (
        jsonify(
            {
                "msg": "File uploaded",
                "fileTOken": data["downloadFile"],
                "downloadURL": data["url"],
                "success": True,
            }
        ),
        201,
    )


@fileRoutes.route("/uploads", methods=["GET"])
def getFiles():
    email = request.form.get("email")

    user = userModel.getUserInfo(email=email)

    if not email:
        return jsonify({"msg": "no email provided", "success": False}), 404

    if user is None:
        return (
            jsonify(
                {
                    "msg": "User not found",
                    "success": False,
                }
            ),
            404,
        )

    files = fileModel.getAll()

    dataObject = []
    for each in files:
        dataObject.append(
            {
                "filename": each["filename"],
                "uploadedBy": each["uploadedBy"],
                "url": each["url"],
                "downloadId": each["downloadFile"],
            }
        )

    return (
        jsonify({"msg": "All files are here", "success": True, "files": dataObject}),
        200,
    )



@fileRoutes.route("/download", methods=["GET"])
def getFile():
    email = request.form.get("email")
    fileId = request.args.get("file")

    user = userModel.getUserInfo(email=email)

    if not email:
        return jsonify({"msg": "no email provided", "success": False}), 404

    if user is None:
        return (
            jsonify(
                {
                    "msg": "User not found",
                    "success": False,
                }
            ),
            404,
        )

    fileFound = fileModel.getFile(fileId)

    if fileFound is None:
        return (
            jsonify({"msg": "Invalid file id or file not found", "success": False}),
            404,
        )

    return (
        jsonify(
            {
                "msg": "File found",
                "success": True,
                "data": {
                    "filename": fileFound["filename"],
                    "downloadURL": fileFound["url"],
                    "Uploaded By": fileFound["uploadedBy"],
                },
            }
        ),
        200,
    )
