from django.core.management.base import BaseCommand
import pika

class Command(BaseCommand):
    help = 'Runs the RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        credentials = pika.PlainCredentials('user', 'password')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', credentials=credentials)
        )
        channel = connection.channel()

        # Declare the queue to listen to
        channel.queue_declare(queue='book_queue')

        # Set up the listener
        channel.basic_consume(queue='book_queue', on_message_callback=self.callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        response = f"Processed: {body.decode()}"
        print(response)
