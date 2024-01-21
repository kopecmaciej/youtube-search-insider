import pika

def send_url_to_queue(url):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='transcription_processing')

    channel.basic_publish(exchange='',
                          routing_key='transcription_processing',
                          body=url)

    print(f"Sent URL to 'transcription_processing' queue: {url}")

    connection.close()

