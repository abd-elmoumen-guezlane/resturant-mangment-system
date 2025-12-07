.PHONY: help build up down logs migrate test clean

help:
@echo "Commandes disponibles:"
@echo "  make build       - Construire les images Docker"
@echo "  make up          - Démarrer tous les services"
@echo "  make down        - Arrêter tous les services"
@echo "  make logs        - Voir les logs"
@echo "  make migrate     - Appliquer les migrations"
@echo "  make test        - Lancer les tests"
@echo "  make clean       - Nettoyer les containers/images"

build:
docker-compose build

up:
docker-compose up -d

down:
docker-compose down

logs:
docker-compose logs -f

migrate:
docker-compose exec auth-service python manage.py migrate
docker-compose exec order-service python manage.py migrate
docker-compose exec menu-service python manage.py migrate
docker-compose exec delivery-service python manage.py migrate

test:
docker-compose exec auth-service python manage.py test
docker-compose exec order-service python manage.py test

clean:
docker-compose down -v
docker system prune -f

# Déploiement multi-serveurs
deploy-server1:
@echo "Déploiement sur le serveur 1..."
@echo "docker-compose up -d postgres-auth rabbitmq consul traefik auth-service"

deploy-server2:
@echo "Déploiement sur le serveur 2..."
@echo "docker-compose up -d postgres-orders order-service menu-service"

deploy-server3:
@echo "Déploiement sur le serveur 3..."
@echo "docker-compose up -d frontend delivery-service notification-worker"
