#!/usr/bin/env sh

BIN_DIR="$(dirname "$(readlink -f "$0")")"
SECRET_DIR="$(dirname $BIN_DIR)/secrets"

MONGO_ROOT_USERNAME="$SECRET_DIR/mongo_root_username"
MONGO_ROOT_PASSWORD="$SECRET_DIR/mongo_root_password"

if [ ! -f "$MONGO_ROOT_USERNAME" ]; then
  username=''

  while [ -z "$username" ]; do
      read -p 'Enter Mongo superuser name: ' username
  done

  echo -n "$username" > "$MONGO_ROOT_USERNAME"
fi

if [ ! -f "$MONGO_ROOT_PASSWORD" ]; then
  read -p 'Enter Mongo superuser password: ' password

  if [ -z "$password" ]; then
      password="$(command -v pwgen >/dev/null 2>&1 && pwgen -cn 16 1 || openssl rand -base64 32)"
  fi

  echo -n "$password" > "$MONGO_ROOT_PASSWORD"
fi

docker compose build
