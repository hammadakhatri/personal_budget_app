#!/bin/bash

# Configuration
# Replace with your actual bucket name after you create it in GCP
BUCKET_NAME="gs://budget-app-backups-hammad"
DB_PATH="budget.db"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="budget_backup_$TIMESTAMP.db"

echo "Starting backup of $DB_PATH to $BUCKET_NAME..."

# Check if gsutil is installed (it is by default on GCP VMs)
if ! command -v gsutil &> /dev/null
then
    echo "gsutil could not be found. Please ensure Google Cloud SDK is installed."
    exit 1
fi

# Perform upload
gsutil cp $DB_PATH $BUCKET_NAME/$BACKUP_NAME

if [ $? -eq 0 ]; then
    echo "✅ Backup successful: $BACKUP_NAME"
else
    echo "❌ Backup failed!"
fi
