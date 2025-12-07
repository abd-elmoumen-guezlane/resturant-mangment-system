#!/bin/bash
echo "Déploiement de tous les services..."
docker-compose up -d --build
echo "Attente du démarrage des services..."
sleep 10
echo "Application des migrations..."
docker-compose exec auth-service python manage.py migrate
docker-compose exec order-service python manage.py migrate
echo "Déploiement terminé !"
