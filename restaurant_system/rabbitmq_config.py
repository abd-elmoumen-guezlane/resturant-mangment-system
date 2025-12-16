# restaurant_system/rabbitmq_config.py
import pika
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Configuration RabbitMQ
RABBITMQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'virtual_host': '/',
    'credentials': pika.PlainCredentials('guest', 'guest')
}

# Noms des queues
QUEUE_ORDER_NOTIFICATIONS = 'order_notifications'
##QUEUE_DELIVERY_ASSIGNMENTS = 'delivery_assignments'


class RabbitMQConnection:
    """Gestionnaire de connexion RabbitMQ"""
    
    @staticmethod
    def get_connection():
        """Crée et retourne une connexion RabbitMQ"""
        try:
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_CONFIG['host'],
                port=RABBITMQ_CONFIG['port'],
                virtual_host=RABBITMQ_CONFIG['virtual_host'],
                credentials=RABBITMQ_CONFIG['credentials'],
                heartbeat=600,
                blocked_connection_timeout=300
            )
            return pika.BlockingConnection(parameters)
        except Exception as e:
            logger.error(f"Erreur de connexion RabbitMQ: {e}")
            raise


class MessageProducer:
    """Producer pour envoyer des messages à RabbitMQ"""
    
    @staticmethod
    def send_message(queue_name, message_data):
        """
        Envoie un message à une queue RabbitMQ
        
        Args:
            queue_name: Nom de la queue
            message_data: Données à envoyer (dict)
        """
        connection = None
        try:
            connection = RabbitMQConnection.get_connection()
            channel = connection.channel()
            
            # Déclarer la queue (idempotent)
            channel.queue_declare(
                queue=queue_name,
                durable=True,  # La queue survivra au redémarrage du broker
               ## arguments={'x-message-ttl': 86400000}  # TTL 24h
            )
            
            # Convertir en JSON
            message_json = json.dumps(message_data)
            
            # Publier le message
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message_json,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Message persistant
                    content_type='application/json'
                )
            )
            
            logger.info(f"Message envoyé à {queue_name}: {message_data}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi du message: {e}")
            return False
            
        finally:
            if connection and not connection.is_closed:
                connection.close()


class OrderNotificationProducer:
    """Producer spécifique pour les notifications de commandes"""
    
    @staticmethod
    def notify_new_order(order_id, customer_name, total_price, items_count):
        """
        Envoie une notification de nouvelle commande
        
        Args:
            order_id: ID de la commande
            customer_name: Nom du client
            total_price: Prix total
            items_count: Nombre d'articles
        """
        message_data = {
            'event': 'new_order',
            'order_id': order_id,
            'customer_name': customer_name,
            'total_price': str(total_price),
            'items_count': items_count,
            'timestamp': str(timezone.now())
        }
        
        return MessageProducer.send_message(
            QUEUE_ORDER_NOTIFICATIONS,
            message_data
        )


from django.utils import timezone