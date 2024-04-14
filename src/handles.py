import json
import boto3
from datetime import datetime
# from uuid import uuid4
import hashlib
import os
from dotenv import load_dotenv
# from aws_services import synthesize_speech, upload_audio_to_s3


load_dotenv()

bucket_name = os.getenv('S3_BUCKET')
table_name = os.getenv('DYNAMODB_TABLE')