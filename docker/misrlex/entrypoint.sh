#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."


echo "Running migrations..."
cd /app/models/db_schemas/misrlex/
alembic upgrade head

cd /app