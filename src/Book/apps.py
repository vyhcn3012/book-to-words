from django.apps import AppConfig
from threading import Thread
import pika
import json
import base64
import os
from io import BytesIO
from django.http import JsonResponse
from django.core.files.base import ContentFile
from Book.import_book import import_book


class BookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Book'

    def ready(self):
        consumer_thread = Thread(target=start_rabbitmq_consumer)
        consumer_thread.daemon = True 
        consumer_thread.start()

def start_rabbitmq_consumer():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='book_queue')
    channel.basic_consume(queue='book_queue', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def callback(ch, method, properties, body):

    try:
        # Decode the incoming message from JSON
        # print(f" [x] Received {body.decode()}")
        _data = json.loads(body.decode())
        data = _data['data']

        print(data)

        # Check if the expected keys are in the data
        if 'file' not in data or 'file_name' not in data:
            print(" [!] Missing 'file' or 'file_name' in the received data")
            return

        # Decode the file content from Base64
        file_content = base64.b64decode(data['file'])
        file_name = data['file_name']

        # Create a Django ContentFile object from the decoded content
        file = ContentFile(file_content, name=file_name)

        # Call the function to process the file
        import_book(file)

    except Exception as e:
        print(f" [!] Error processing message: {e}")