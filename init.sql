-- Step 1: Create the user with CREATEDB privilege
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'evotes_dev') THEN
        CREATE ROLE evotes_dev WITH LOGIN PASSWORD 'evotes_dev_pwd' CREATEDB;
    END IF;
END
$$;

-- Step 2: Create the database (MUST NOT be inside DO block)
-- Check if the database exists manually in bash if needed
-- For now, we assume it doesn't exist:
CREATE DATABASE evotes_dev_db OWNER evotes_dev;

-- Step 3: Connect to the newly created database
\connect evotes_dev_db

-- Step 4: Grant privileges on the public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO evotes_dev;

-- Step 5: Set default privileges
ALTER DEFAULT PRIVILEGES FOR ROLE evotes_dev IN SCHEMA public
GRANT ALL ON TABLES TO evotes_dev;

ALTER DEFAULT PRIVILEGES FOR ROLE evotes_dev IN SCHEMA public
GRANT ALL ON SEQUENCES TO evotes_dev;

ALTER DEFAULT PRIVILEGES FOR ROLE evotes_dev IN SCHEMA public
GRANT ALL ON FUNCTIONS TO evotes_dev;
