#!/bin/bash
set -e

echo ">>>>>>> trying to create database and users"
if [ -n "${MONGO_INITDB_ROOT_USERNAME:-}" ] && [ -n "${MONGO_INITDB_ROOT_PASSWORD:-}" ] && [ -n "${MONGODB_DATABASE_UESR_USERNAME:-}" ] && [ -n "${MONGODB_DATABASE_USER_PASSWORD:-}" ]; then
mongo -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD<<EOF
db=db.getSiblingDB('$MONGODB_DATABASE');
use $MONGODB_DATABASE;
db.createUser({
  user:  '$MONGODB_DATABASE_UESR_USERNAME',
  pwd: '$MONGODB_DATABASE_USER_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: '$MONGODB_DATABASE'
  }]
});
EOF
else
    echo "MONGO_INITDB_ROOT_USERNAME,MONGO_INITDB_ROOT_PASSWORD,MONGODB_DATABASE_UESR_USERNAME and MONGODB_DATABASE_USER_PASSWORD must be provided. Some of these are missing, hence exiting database and user creatioin"
    exit 403
fi