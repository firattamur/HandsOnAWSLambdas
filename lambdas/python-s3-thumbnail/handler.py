from typing_extensions import TypeAlias
import boto3
import logging
from botocore.exceptions import ClientError
from io import BytesIO
from PIL import Image, ImageOps
import os

s3 = boto3.client("s3")
size = int(os.environ["THUMBNAIL_SIZE"])
format = "PNG"

PILImage: TypeAlias = "PIL.JpegImagePlugin.JpegImageFile"

def handler(event, context):
    
    # get bucket name and image key 
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    region = event["Records"][0]["awsRegion"]

    if "thumbnail.png" in key:
        return "This is a thumbnail!"

    # retrieve image from s3
    image = get_image_from_s3(bucket, key)

    # create thumbnail
    thumbnail = create_thumbnail(image)

    # generate key for thumbnail
    thumbnail_key = create_thumbnail_key(key)

    # upload thumbnail to s3
    url = upload_thumbnail_to_s3(bucket, thumbnail_key, thumbnail, region)

    return url


def get_image_from_s3(bucket: str, key: str) -> PILImage:
    
    response = s3.get_object(Bucket=bucket, Key=key)

    imageContent = response["Body"].read()

    imageFile = BytesIO(imageContent)
    image = Image.open(imageFile)

    return image


def create_thumbnail(image: PILImage) -> PILImage:
    return ImageOps.fit(image, (size, size), Image.ANTIALIAS)


def create_thumbnail_key(key: str) -> str:
    return key.replace(".png", "_thumbnail.png")


def upload_thumbnail_to_s3(bucket: str, thumbnail_key: str, thumbnail: PILImage, region: str) -> str:
    # save image to stringio object instead of writing to the disk
    output = BytesIO()

    # save image
    thumbnail.save(output, format)

    # start of the stream
    thumbnailData = output.getvalue()

    response = s3.put_object(
        ACL='public-read',
        Body=thumbnailData,
        Bucket=bucket,
        ContentType='image/png',
        Key=thumbnail_key
    )
    
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{thumbnail_key}"
    
    return url


"""
    Example event: 

    {'Records': [
                    {
                    'eventVersion': '2.1', 
                    'eventSource': 'aws:s3', 
                    'awsRegion': 'us-east-2', 
                    'eventTime': '2021-07-25T22:25:40.571Z', 
                    'eventName': 'ObjectCreated:Put', 
                    'userIdentity': {'principalId': 'AZ09JJO23TJ23'}, 
                    'requestParameters': {'sourceIPAddress': '176.55.236.157'}, 
                    'responseElements': {
                                        'x-amz-request-id': 'A75HRNBAATJZMQ57', 
                                        'x-amz-id-2': '7g8DtYd0VWbp7Q+hQfWGpA3FRtufRU5/2gWlHp5sB8a95PThdyjZ4sIdOYJX9EJ77/5ISWHgxXlFVSYZ/2uludbE4GEJluJCJLI2Cqz0lKo='}, 
                    's3': {
                            's3SchemaVersion': '1.0', 
                            'configurationId': 'python-s3-thumbnail-dev-hello-fbff821515843392a274663548ccd733', 
                            'bucket': {
                                'name': 'firattamur-s3-thumbnail-bucket-2', 
                                'ownerIdentity': {'principalId': 'AZ09JJO23TJ23'}, 
                                'arn': 'arn:aws:s3:::firattamur-s3-thumbnail-bucket-2'}, 
                            'object': {
                                'key': 'rick_and_morty.png',
                                'size': 1339139, 
                                'eTag': '59605127dffb786ac6bcb369a44f4e09', 
                                'sequencer': '0060FDE4E9601307F5'}
                            }
                    }
                ]
    }

"""

"""
    Example s3.putObject response:

    response: 
        {
            'ResponseMetadata': 
                {
                    'RequestId': '9KC9GMN8Z08YGD0B', 
                    'HostId': 'eiC88JmdxDmKGgGSFHtAfPO1s2ZwtdtQy4iyNRapbtcGv1qxt8v9JE3FEoIf9YXbwowII243ASA=', 
                    'HTTPStatusCode': 200, 
                    'HTTPHeaders': 
                        {
                        'x-amz-id-2': 
                        'eiC88JmdxDmKGgGSFHtAfPO1s2ZwtdtQy4iyNRapbtcGv1qxt8v9JE3FEoIf9YXbwowII243ASA=', 
                        'x-amz-request-id': '9KC9GMN8Z08YGD0B', 
                        'date': 'Sun, 25 Jul 2021 23:11:56 GMT', 
                        'last-modified': 'Sun, 25 Jul 2021 23:11:55 GMT', 
                        'etag': '"59605127dffb786ac6bcb369a44f4e09"', 
                        'accept-ranges': 'bytes', 
                        'content-type': 'image/png', 
                        'server': 'AmazonS3', 
                        'content-length': '1339139'
                        }, 
                    'RetryAttempts': 0
                }, 
            'AcceptRanges': 'bytes', 
            'LastModified': datetime.datetime(2021, 7, 25, 23, 11, 55, tzinfo=tzutc()), 
            'ContentLength': 1339139, 
            'ETag': '"59605127dffb786ac6bcb369a44f4e09"', 
            'ContentType': 'image/png', 
            'Metadata': {}, 
            'Body': <botocore.response.StreamingBody object at 0x7f061bb70550>
        }

"""
