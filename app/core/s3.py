import boto3
import uuid
import os
from fastapi import UploadFile

AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client("s3", region_name=AWS_REGION)


def upload_file_to_s3(file: UploadFile) -> str:
    """
    Uploads a file to S3 and returns the public URL
    """

    # Generate unique filename to avoid overwrite
    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    # Upload file
    s3.upload_fileobj(
        file.file,   # actual file stream
        BUCKET_NAME,
        unique_filename,
        ExtraArgs={
            "ContentType": file.content_type,
            # Optional (enable if bucket allows public access)
            # "ACL": "public-read"
        }
    )

    # Return file URL
    return f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
