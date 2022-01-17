import boto3
from decouple import config
import uuid

s3_client = boto3.client(
    's3',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
    )


def upload_image(file):
    try:
        file_name = str(uuid.uuid4()) + "." + str(file.name).split(".")[1]
        
        s3_client.upload_fileobj(
            file,
            config("BUCKET_NAME"),
            file_name,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )

        return config("S3_OBJECT_BASE_URL") + file_name
    
    except Exception as e:
        raise e


def delete_image(img_url):
    try:
        img_key = img_url.split(config('S3_OBJECT_BASE_URL'))[1]
        s3_client.delete_object(
            Bucket=config("BUCKET_NAME"),
            Key=img_key
        )

        return True
    
    except Exception as e:
        raise e
