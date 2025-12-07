#!/bin/bash
echo "Construction de toutes les images..."
docker-compose build --no-cache
echo "Construction terminée !"
