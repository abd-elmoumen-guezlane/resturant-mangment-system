# Système de Gestion de Restaurant - Microservices

## Architecture
- Frontend (Django): http://localhost:8000
- Auth Service: http://localhost:8001
- Order Service: http://localhost:8002
- Menu Service: http://localhost:8003
- Delivery Service: http://localhost:8004
- RabbitMQ Management: http://localhost:15672
- Consul UI: http://localhost:8500
- Traefik Dashboard: http://localhost:8080

## Commandes utiles

\\\ash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Appliquer les migrations
docker-compose exec auth-service python manage.py migrate

# Arrêter tous les services
docker-compose down

# Nettoyer
docker-compose down -v
docker system prune -f
\\\

## Déploiement Multi-Serveurs

1. **Serveur 1** (Infrastructure):
\\\ash
docker-compose up -d postgres-auth rabbitmq consul traefik auth-service
\\\

2. **Serveur 2** (Services métier):
\\\ash
docker-compose up -d postgres-orders order-service menu-service
\\\

3. **Serveur 3** (Interface + Notifications):
\\\ash
docker-compose up -d frontend delivery-service notification-worker
\\\

## Auteurs
- Projet WAMS 2025
- ING 4ème année Informatique
- UMB Béjaïa
