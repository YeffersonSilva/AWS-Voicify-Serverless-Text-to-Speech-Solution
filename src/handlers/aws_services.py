# aws_services.py
import boto3
import os
from uuid import uuid4

def synthesize_speech(phrase):
    polly = boto3.client('polly',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = polly.synthesize_speech(
        LanguageCode='pt-BR',
        OutputFormat='mp3',
        Text=phrase,
        TextType='text',
        VoiceId='Vitoria'
    )
    return response['AudioStream'].read()

def upload_audio_to_s3(audio_stream, directory):
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    bucket_name = os.getenv('BUCKET_NAME')
    key = f'{directory}polly-{uuid4()}.mp3'
    s3.put_object(
        Body=audio_stream,
        Bucket=bucket_name,
        Key=key,
        ContentType='audio/mpeg',
        ACL='public-read'
    )
    return f'https://{bucket_name}.s3.amazonaws.com/{key}'
