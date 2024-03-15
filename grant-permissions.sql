-- CREATE USER 'restsupplyadmin'@'localhost' IDENTIFIED BY 'adminpw';
-- CREATE USER 'restsupplyclient'@'localhost' IDENTIFIED BY 'clientpw';

-- CREATE USER IF NOT EXISTS 'restsupplyadmin'@'localhost' IDENTIFIED BY 'password';
-- CREATE USER IF NOT EXISTS 'restsupplyclient'@'localhost' IDENTIFIED BY 'password';

DROP USER IF EXISTS 'restsupplyadmin'@'localhost';
DROP USER IF EXISTS 'restsupplyclient'@'localhost';
CREATE USER 'restsupplyadmin'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'restsupplyclient'@'localhost' IDENTIFIED BY 'password';

-- Can add more users or refine permissions
GRANT ALL PRIVILEGES ON final.* TO 'restsupplyadmin'@'localhost';
GRANT SELECT ON final.* TO 'restsupplyclient'@'localhost';
FLUSH PRIVILEGES;
