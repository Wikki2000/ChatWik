-- Create database if not exists
CREATE DATABASE IF NOT EXISTS chatwik_dev_db;

-- Create user if not exists
CREATE USER IF NOT EXISTS "chatwik_dev"@"localhost" IDENTIFIED BY "chatwik_dev_pwd";

-- Grant priviledges
GRANT ALL ON chatwik_dev_db.* TO "chatwik_dev"@"localhost";
