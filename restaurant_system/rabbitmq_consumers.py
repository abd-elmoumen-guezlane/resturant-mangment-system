# restaurant_system/rabbitmq_consumers.py
import pika
import json
import logging
import sys
import os
import django
import threading
from django.utils import timezone

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_system.settings')
django.setup()

from rabbitmq_config import (
    RabbitMQConnection,
    QUEUE_ORDER_NOTIFICATIONS,
    ##QUEUE_DELIVERY_ASSIGNMENTS
)
from orders.models import Order
## from delivery.models import Delivery, DeliveryProfile

# ---------------------------
# Logging setup
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Suppress verbose pika logs
logging.getLogger("pika").setLevel(logging.WARNING)

# Separate loggers for each consumer
orders_logger = logging.getLogger("orders_consumer")
delivery_logger = logging.getLogger("delivery_consumer")

# ---------------------------
# Order Notification Consumer
# ---------------------------
class OrderNotificationConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body.decode())
            orders_logger.info(f"📦 Nouvelle commande reçue: {message}")

            order_id = message.get('order_id')
            customer_name = message.get('customer_name')
            total_price = message.get('total_price')
            items_count = message.get('items_count')

            self.process_order_notification(order_id, customer_name, total_price, items_count)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            orders_logger.info(f"✅ Notification traitée pour commande #{order_id}")

        except Exception as e:
            orders_logger.error(f"❌ Erreur traitement notification: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def process_order_notification(self, order_id, customer_name, total_price, items_count):
        try:
            order = Order.objects.get(id=order_id)
            notification_message = f"""
🎉 Nouvelle commande confirmée!

Commande #{order_id}
Client: {customer_name}
Montant: {total_price} DA
Articles: {items_count}

Votre commande est en cours de préparation!
"""
            orders_logger.info(f"📧 Notification envoyée: {notification_message}")

            if order.status == 'pending':
                order.status = 'preparing'
                order.save()
                orders_logger.info(f"📝 Statut commande #{order_id} -> En préparation")
        except Order.DoesNotExist:
            orders_logger.error(f"Commande #{order_id} introuvable")
        except Exception as e:
            orders_logger.error(f"Erreur process_order_notification: {e}")

    def start_consuming(self):
        try:
            self.connection = RabbitMQConnection.get_connection()
            self.channel = self.connection.channel()

            self.channel.queue_declare(
                queue=QUEUE_ORDER_NOTIFICATIONS,
                durable=True
            )

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=QUEUE_ORDER_NOTIFICATIONS,
                on_message_callback=self.callback,
                auto_ack=False
            )

            orders_logger.info("🚀 [OrderNotificationConsumer] En attente de messages...")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            orders_logger.info("🛑 Arrêt du consumer orders...")
            self.stop_consuming()
        except Exception as e:
            orders_logger.error(f"❌ Erreur consumer orders: {e}")
            self.stop_consuming()

    def stop_consuming(self):
        if self.channel:
            self.channel.stop_consuming()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        orders_logger.info("✅ Orders consumer arrêté")

# ---------------------------
# Delivery Assignment Consumer
# ---------------------------
"""

class DeliveryAssignmentConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body.decode())
            delivery_logger.info(f"🚚 Assignation de livraison reçue: {message}")

            delivery_id = message.get('delivery_id')
            order_id = message.get('order_id')
            delivery_person_id = message.get('delivery_person_id')
            address = message.get('address')

            self.process_delivery_assignment(delivery_id, order_id, delivery_person_id, address)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            delivery_logger.info(f"✅ Assignation traitée pour livraison #{delivery_id}")

        except Exception as e:
            delivery_logger.error(f"❌ Erreur traitement assignation: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def process_delivery_assignment(self, delivery_id, order_id, delivery_person_id, address):
        try:
            delivery = Delivery.objects.get(id=delivery_id)
            delivery_person = DeliveryProfile.objects.get(id=delivery_person_id)
            order = Order.objects.get(id=order_id)

            notification_message = f"""
#🚚 Nouvelle livraison assignée! `

#Livraison #{delivery_id}
#Commande #{order_id}
#Client: {order.customer_name}
#Adresse: {address}

#Préparez-vous à livrer!
"""
            delivery_logger.info(f"📱 Notification livreur envoyée: {notification_message}")

            if order.status == 'preparing':
                order.status = 'delivering'
                order.save()
                delivery_logger.info(f"📝 Statut commande #{order_id} -> En livraison")

            if delivery.status == 'pending':
                delivery.status = 'on_the_way'
                delivery.save()
                delivery_logger.info(f"📝 Statut livraison #{delivery_id} -> En route")

        except (Delivery.DoesNotExist, DeliveryProfile.DoesNotExist, Order.DoesNotExist) as e:
            delivery_logger.error(f"Entité introuvable: {e}")
        except Exception as e:
            delivery_logger.error(f"Erreur process_delivery_assignment: {e}")

    def start_consuming(self):
        try:
            self.connection = RabbitMQConnection.get_connection()
            self.channel = self.connection.channel()

            self.channel.queue_declare(
                queue=QUEUE_DELIVERY_ASSIGNMENTS,
                durable=True
            )

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=QUEUE_DELIVERY_ASSIGNMENTS,
                on_message_callback=self.callback,
                auto_ack=False
            )

            delivery_logger.info("🚀 [DeliveryAssignmentConsumer] En attente de messages...")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            delivery_logger.info("🛑 Arrêt du consumer deliveries...")
            self.stop_consuming()
        except Exception as e:
            delivery_logger.error(f"❌ Erreur consumer deliveries: {e}")
            self.stop_consuming()

    def stop_consuming(self):
        if self.channel:
            self.channel.stop_consuming()
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        delivery_logger.info("✅ Delivery consumer arrêté")
"""
# ---------------------------
# Main entry
# ---------------------------
def main():
    import argparse

    parser = argparse.ArgumentParser(description='RabbitMQ Consumers')
    parser.add_argument(
        '--consumer',
        choices=['orders', 'deliveries', 'all'],
        default='all',
        help='Quel consumer lancer'
    )
    args = parser.parse_args()

    consumers = []

    if args.consumer in ['orders', 'all']:
        order_consumer = OrderNotificationConsumer()
        t_orders = threading.Thread(target=order_consumer.start_consuming, daemon=True)
        consumers.append(t_orders)
        t_orders.start()
## the consue
    try:
        while True:
            for t in consumers:
                t.join(0.5)  # Keep main alive
    except KeyboardInterrupt:
        orders_logger.info("🛑 Arrêt global des consumers...")
        delivery_logger.info("🛑 Arrêt global des consumers...")

if __name__ == '__main__':
    main()
