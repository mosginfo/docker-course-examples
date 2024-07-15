#!/usr/bin/env sh

BIN_DIR="$(dirname "$(readlink -f "$0")")"
SECRET_DIR="$(dirname $BIN_DIR)/secrets"

MONGO_ROOT_USERNAME="$SECRET_DIR/mongo_root_username"
MONGO_ROOT_PASSWORD="$SECRET_DIR/mongo_root_password"

if [ ! -f "$MONGO_ROOT_USERNAME" ]; then
  echo "Creating $(basename $MONGO_ROOT_USERNAME) secret"
  echo 'user' > "$MONGO_ROOT_USERNAME"
fi

if [ ! -f "$MONGO_ROOT_PASSWORD" ]; then
  echo "Creating $(basename $MONGO_ROOT_PASSWORD) secret"
  echo "$(command -v pwgen >/dev/null 2>&1 && pwgen -cn 16 1 || openssl rand -base64 32)" > "$MONGO_ROOT_PASSWORD"
fi

docker compose build
