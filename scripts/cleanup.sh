#!/bin/bash

# Detener y eliminar contenedores
docker-compose down

# Eliminar volúmenes no utilizados
docker volume prune -f