-- CREATE USER 'restsupplyadmin'@'localhost' IDENTIFIED BY 'adminpw';
-- CREATE USER 'restsupplyclient'@'localhost' IDENTIFIED BY 'clientpw';

-- CREATE USER IF NOT EXISTS 'restsupplyadmin'@'localhost' IDENTIFIED BY 'password';
-- CREATE USER IF NOT EXISTS 'restsupplyclient'@'localhost' IDENTIFIED BY 'password';
DROP USER IF EXISTS 'restsupplyadmin'@'localhost';
DROP USER IF EXISTS 'restsupplyclient'@'localhost';

-- Recreate the users with their passwords
CREATE USER 'restsupplyadmin'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'restsupplyclient'@'localhost' IDENTIFIED BY 'password';

-- Grant full privileges to the admin user on the 'final' database
GRANT ALL PRIVILEGES ON final.* TO 'restsupplyadmin'@'localhost';

-- Grant SELECT and EXECUTE privileges to the client user on the 'final' database
GRANT SELECT, EXECUTE ON final.* TO 'restsupplyclient'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

