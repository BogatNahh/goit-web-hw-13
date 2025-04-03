import cloudinary.uploader
from fastapi import UploadFile

@app.post("/upload-avatar/")
async def upload_avatar(file: UploadFile):
    result = cloudinary.uploader.upload(file.file)
    return {"url": result["secure_url"]}
