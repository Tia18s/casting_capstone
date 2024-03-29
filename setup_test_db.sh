#!/bin/bash

# Prompt the user to enter the PostgreSQL username and password
read -p "Enter PostgreSQL username: " username
read -sp "Enter PostgreSQL password: " password

# Set the PostgreSQL username and password as environment variables
export PGUSER="$username"
export PGPASSWORD="$password"

# Drop the database if it exists
psql -c "DROP DATABASE IF EXISTS casting_test"

# Create the database
psql -c "CREATE DATABASE casting_test"

# Restore the database from the SQL file
psql -d casting_test -f ./casting_capstone.psql

# Clear the environment variables
unset PGUSER
unset PGPASSWORD
