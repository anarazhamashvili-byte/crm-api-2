#!/usr/bin/env bash
set -euo pipefail

APP_NAME="marketplacesoftwareapi"
APP_DIR="/opt/MarketPlaceSoftwareAPI"
PYTHON_BIN="python3"
SERVICE_NAME="marketplacesoftwareapi"
ENABLE_SYNC_TIMER="${ENABLE_SYNC_TIMER:-1}"

echo "==> Installing system packages..."
sudo apt-get update -y
sudo apt-get install -y "$PYTHON_BIN" python3-venv python3-pip nginx rsync

echo "==> Creating app directory..."
sudo mkdir -p "$APP_DIR"
sudo chown -R "$USER":"$USER" "$APP_DIR"

echo "==> Copying project files..."
rsync -av --delete --exclude ".venv" --exclude "__pycache__" ./ "$APP_DIR/"

echo "==> Creating virtual environment..."
cd "$APP_DIR"
$PYTHON_BIN -m venv .venv
. .venv/bin/activate

echo "==> Installing Python dependencies..."
pip install --upgrade pip
if file requirements.txt | grep -qi "utf-16"; then
  iconv -f utf-16 -t utf-8 requirements.txt -o /tmp/requirements_utf8.txt
  pip install -r /tmp/requirements_utf8.txt
else
  pip install -r requirements.txt
fi

echo "==> Creating systemd service..."
sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" >/dev/null <<EOF
[Unit]
Description=MarketPlaceSoftwareAPI Flask Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PYTHONUNBUFFERED=1
ExecStart=$APP_DIR/.venv/bin/python $APP_DIR/api.py
Environment=PORT=7000
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "==> Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

if [ "$ENABLE_SYNC_TIMER" = "1" ] && [ -f "$APP_DIR/install_systemd_timer.sh" ]; then
  echo "==> Enabling 5-minute sync timer..."
  chmod +x "$APP_DIR/install_systemd_timer.sh"
  "$APP_DIR/install_systemd_timer.sh"
fi

echo "==> Done. Service is running."
