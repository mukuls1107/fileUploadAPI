import os
import cloudinary
import cloudinary.uploader


possibleExtensions = {"docx", "ppt", "xlsx"}


cloudinary.config(
    cname=os.getenv("CLOUDINARY_CNAME"),
    apiKey=os.getenv("API_KEY"),
    apiSecret=os.getenv("API_SECRET"),
)


def fileUpload(file, filename):
    try:
        upload = cloudinary.uploader.upload(
            file,
            resource_type="raw",
            public_id=filename
        )
        
        return upload["secure_url"]

    except Exception as err:
        print("error in file upload:", err)
        return None
    
def checkFileType(filename):
    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    print( "File extension is",extension)
    if extension in possibleExtensions:
        return True

    return False
