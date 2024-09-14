import pika

def send_to_rabbitmq(message):
    # Create credentials object with username and password
    credentials = pika.PlainCredentials('user', 'password')  # 'user' is both the username and the password
    
    # Set up connection parameters including credentials
    connection_params = pika.ConnectionParameters(
        host='localhost',     # RabbitMQ server address
        port=5672,            # Default port for RabbitMQ
        credentials=credentials  # Pass the credentials object for authentication
    )

    # Establish connection to RabbitMQ using the specified parameters
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    # Declare the queue (it will be created if it does not exist)
    channel.queue_declare(queue='nest_queue')

    # Send message to the queue
    channel.basic_publish(exchange='', routing_key='nest_queue', body=message)
    print(f" [x] Sent '{message}'")

    # Close the connection
    connection.close()
