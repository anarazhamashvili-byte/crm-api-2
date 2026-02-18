#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/MarketPlaceSoftwareAPI"

sudo mkdir -p "$APP_DIR"
sudo rsync -av --delete --exclude "__pycache__" ./ "$APP_DIR/"

sudo cp "$APP_DIR/crm_sync.service" /etc/systemd/system/crm_sync.service
sudo cp "$APP_DIR/crm_sync.timer" /etc/systemd/system/crm_sync.timer

sudo systemctl daemon-reload
sudo systemctl enable --now crm_sync.timer

echo "CRM sync timer enabled (runs every 5 minutes)."
