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

# Configurar sessão Boto3 com credenciais e região
session = boto3.session.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
    region_name=os.getenv('AWS_REGION')
)

polly_client = session.client('polly')
s3_client = session.client('s3')
dynamodb_client = session.client('dynamodb')


def extract_phrase_from_request(event):
    req = json.loads(event.get('body'))
    received_phrase = req.get('phrase', None)
    if received_phrase is None:
        return None
    return received_phrase

def generate_unique_id(phrase):
    # Gera um hash MD5 único com base na frase recebida
    return hashlib.md5(phrase.encode()).hexdigest()


def synthesize_speech(phrase):
    # Solicitação ao Polly para converter o texto em fala
    response = polly_client.synthesize_speech(
        LanguageCode='pt-BR',
        Engine='neural',
        Text=phrase,
        OutputFormat='mp3',
        VoiceId='Vitoria'
    )
    return response['AudioStream'].read()

def save_audio_to_s3(audio_data, unique_id):
    # Salva o áudio no S3
    object_key = f'audio-{unique_id}.mp3'
    s3_client.put_object(
        Body=audio_data,
        Bucket=bucket_name,
        Key=object_key,
        ContentType='audio/mpeg')
    return f'https://{bucket_name}.s3.amazonaws.com/{object_key}'


def save_reference_to_dynamodb(unique_id, received_phrase, audio_url):
    # Salva uma referência no DynamoDB
    dynamodb_client.put_item(
        TableName=table_name,
        Item={
            'unique_id': {'S': unique_id},
            'received_phrase': {'S': received_phrase},
            'audio_url': {'S': audio_url},
            'created_audio': {'S': datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
        }
    )

#verifica se o hash existe
def existing_hash(table_name,hash):
    # Verificar o hash
    responseHash = dynamodb_client.get_item(
        TableName = table_name,
        Key={'unique_id': {'S': str(hash)}}
    )
    if 'Item' in responseHash:
        return responseHash['Item']
    else:
        return None
    
    
    
def add_cors_headers(response):
    response['headers'] = {
        # Ou você pode definir apenas domínios específicos que podem acessar sua API
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
    }
    return response

    

def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_description(event, context):
    body = {
        "message": "TTS api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v2_description(event, context):
    body = {
        "message": "TTS api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response


def v1_tts(event, context):
 
    received_phrase = extract_phrase_from_request(event)
    if received_phrase is None:
        return {"statusCode": 400, "body": "Bad Request"}
 
    # Gera um ID único
    unique_id = generate_unique_id(received_phrase)
 
    # Solicitação ao Polly para converter o texto em fala
    audio_stream = synthesize_speech(received_phrase)
 
    # Salva o áudio no S3
    audio_url = save_audio_to_s3(audio_stream, unique_id)
 
    # Preparação do corpo da resposta incluindo a frase recebida, a URL do áudio e a data de criação
    response_body = {
        'received_phrase': received_phrase,
        'url_to_audio': audio_url,
        'created_audio': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    }
 
    # Retorno da resposta com status 200 e o corpo em formato JSON
    response = {"statusCode": 200,
                "body": json.dumps(response_body)}
    return add_cors_headers(response)


def v2_tts(event, context):
    
    received_phrase = extract_phrase_from_request(event)
    if received_phrase is None:
        return {"statusCode": 400, "body": "Bad Request"}

    # Gera um ID único
    unique_id = generate_unique_id(received_phrase)

    audio_stream = synthesize_speech(received_phrase)

    # Salva o áudio no S3
    audio_url = save_audio_to_s3(audio_stream, unique_id)

    # Salva uma referência no DynamoDB
    save_reference_to_dynamodb(unique_id, received_phrase, audio_url)

    # Constrói a resposta
    response_body = {
        "received_phrase": received_phrase,
        "url_to_audio": audio_url,
        "created_audio": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "unique_id": unique_id
    }

    response = {"statusCode": 200, "body": json.dumps(response_body)}
    return response


def v3_tts(event, context):

    received_phrase = extract_phrase_from_request(event)
    if received_phrase is None:
        return {"statusCode": 400, "body": "Bad Request"}

    # Gera um ID único
    unique_id = generate_unique_id(received_phrase)

    hash_info = existing_hash(table_name, unique_id)

    if (hash_info) is None:
        # se não existir uma referência no DynamoDB, criar um novo registro
        return v2_tts(event=event, context=context)
    else: 
        response_body = {
            "received_phrase": received_phrase,
            "url_to_audio": hash_info['audio_url']['S'],
            "created_audio": hash_info['created_audio']['S'],
            "unique_id": unique_id
        }
        response = {"statusCode": 200, "body": json.dumps(response_body)}
        return response
        
