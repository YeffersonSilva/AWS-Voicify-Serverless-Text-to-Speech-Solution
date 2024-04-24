import json
import boto3
import os
import tempfile
import hashlib
from json.decoder import JSONDecodeError
from contextlib import closing
import unicodedata

AWS_BUCKET_S3 = os.environ['AWS_BUCKET_S3']
AWS_DYNAMODB_TABLE = os.environ['AWS_DYNAMODB_TABLE'] 


def v3_tts(event, context):
    try:
        request = json.loads(event.get('body'))
        received_phrase = request.get('phrase')



        if received_phrase == '':
            response = {"statusCode": 400, "body": "Frase vazia"}
            return response
        

        db_client = boto3.client('dynamodb')

        normalized_phrase = ''.join(c for c in unicodedata.normalize('NFD', received_phrase) if not unicodedata.combining(c))
        hash_obj = hashlib.sha256(normalized_phrase.encode())
        hash_hexa = hash_obj.hexdigest()
        id_db = hash_hexa

        responseDb = db_client.get_item(TableName = AWS_DYNAMODB_TABLE, Key={'id':{'S':id_db}})
        response = ''
        if 'Item' in responseDb:
            item = responseDb['Item']
            
            received_phrase = item.get('received_phrase', {}).get('S', None)
            url_to_audio = item.get('url_to_audio', {}).get('S', None)
            created_audio = item.get('created_audio', {}).get('S', None)
            unique_id = item.get('id', {}).get('S', None)
            
            body = {
                "received_phrase": received_phrase,
                "url_to_audio": url_to_audio,
                "created_audio": created_audio,
                "unique_id": unique_id
            }
            response = {"statusCode": 200, "body": json.dumps(body)}
        else:
            s3_client = boto3.client('s3')
            polly_client = boto3.client('polly')
            
            audio = polly_client.synthesize_speech(Engine='neural',
                                            Text=received_phrase, 
                                            OutputFormat='mp3',
                                            VoiceId='Vitoria')
            
            received_phrase = ''.join(c for c in unicodedata.normalize('NFD', received_phrase) if not unicodedata.combining(c))

            file_phrase_name = received_phrase.replace(" ", "_")
            Temporaryfile = os.path.join(tempfile.gettempdir(), f'{file_phrase_name}.mp3')

            with closing(audio['AudioStream']) as audioStream:
                with open(Temporaryfile,'wb') as file:
                    file.write(audioStream.read())

            s3_file = f'audios/{file_phrase_name}.mp3'
            s3_client.upload_file(Temporaryfile, AWS_BUCKET_S3, s3_file)

            s3_client.put_object_acl(ACL='public-read', Bucket=AWS_BUCKET_S3, Key=s3_file)

            url_to_audio = f'https://{AWS_BUCKET_S3}.s3.amazonaws.com/{s3_file}'

            metaData = s3_client.head_object(Bucket=AWS_BUCKET_S3, Key=s3_file)
            created_audio = metaData['LastModified']
            created_audio = created_audio.strftime("%d-%m-%Y %H:%M:%S")


            item = {
            'id': {'S': str(id_db)},
            'received_phrase': {'S': received_phrase},
            'url_to_audio': {'S': url_to_audio},
            "created_audio": {'S': created_audio}
            }

            db_client.put_item(TableName = AWS_DYNAMODB_TABLE, Item = item)
            
            body = {
                "received_phrase": received_phrase,
                "url_to_audio": url_to_audio,
                "created_audio": created_audio,
                "unique_id": str(id_db)
            }
            response = {"statusCode": 200, "body": json.dumps(body)}
           
    except(TypeError,JSONDecodeError):
        response = {"statusCode": 400, "body": "Requisição inválida "}
    
    return response