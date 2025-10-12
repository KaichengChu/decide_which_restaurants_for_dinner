#!/bin/bash

set -e
# For test purposes only
echo "$(date): Script started" >> /Users/ckc/Desktop/Dinner/decide_which_restaurants_for_dinner/data.log

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SECRET_FILE="$SCRIPT_DIR/secrets.env"
LOG_FILE="$SCRIPT_DIR/results.log"
# Activate the conda environment
PYTHON=/opt/anaconda3/envs/dinner/bin/python3

# Load secret environment variables
set -a
if [ -f "$SECRET_FILE" ]; then
  source "$SECRET_FILE"
else
  echo "[Error] Secret file not found: $SECRET_FILE"
  exit 1
fi
set +a

cd "$SCRIPT_DIR"
$PYTHON -m main > "$LOG_FILE" 2>&1