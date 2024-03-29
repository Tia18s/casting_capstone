# Prompt the user to enter the PostgreSQL username and password
$username = Read-Host -Prompt "Enter PostgreSQL username"
$password = Read-Host -Prompt "Enter PostgreSQL password" -AsSecureString

# Convert the secure string to plain text
$passwordPlainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Set the PostgreSQL username and password as environment variables
$env:PGUSER = $username
$env:PGPASSWORD = $passwordPlainText

# Drop the database if it exists
psql -c "DROP DATABASE IF EXISTS casting_db"

# Create the database
psql -c "CREATE DATABASE casting_db"

# Restore the database from the SQL file
psql -d casting_db -f .\casting_capstone.psql

# Clear the environment variables
$env:PGUSER = $null
$env:PGPASSWORD = $null