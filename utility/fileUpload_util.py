import os
import cloudinary
import cloudinary.uploader
import uuid # Import uuid for unique IDs

possibleExtensions = {"png", "jpeg", "jpg",  "heif", "heic"} # Added jpg and pdf as common extensions

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CNAME"), # <-- CHANGED: 'cname' to 'cloud_name'
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    secure=True
)

def fileUpload(file, original_filename): # Accept original filename as argument
    try:
        # Generate a unique public_id to avoid overwriting files with same name
        # Combines a UUID with the original filename (without extension)
        unique_public_id = f"{uuid.uuid4()}-{os.path.splitext(original_filename)[0]}"

        upload = cloudinary.uploader.upload(
            file,
            resource_type="image", # 'raw' for documents, consider 'image' for images
            public_id=unique_public_id, # <-- CHANGED: Use unique ID
            type="private"
        )
        print(upload) # This print will show the Cloudinary response in your Flask console

        return upload

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