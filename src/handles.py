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

bucket_name = os.getenv('S3_BUCKET')
table_name = os.getenv('DYNAMODB_TABLE')

# Configurar sessão Boto3 com credenciais e região
session = boto3.session.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_REGION')
)
# Crear clientes de AWS para Polly, S3, y DynamoDB

polly_client = session.client('polly')
s3_client = session.client('s3')
dynamodb_client = session.client('dynamodb')

# Extraer frase de un evento HTTP

def extract_phrase_from_request(event):
    req = json.loads(event.get('body'))
    received_phrase = req.get('phrase', None)
    if received_phrase is None:
        return None
    return received_phrase


# Generar un identificador único usando hash MD5 de la frase

def generate_unique_id(phrase):
    # Gera um hash MD5 único com base na frase recebida
    return hashlib.md5(phrase.encode()).hexdigest()