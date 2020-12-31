CREATE USER 'metmini'@metmini.localdomain identified by 'metmini';
CREATE USER 'grafanaReader' IDENTIFIED BY 'grafanasecret';
GRANT SELECT ON metminidb.actual TO 'grafanaReader';
GRANT ALL ON metminidb.* to 'metmini' identified by 'metmini';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'metmini'@metmini.localdomain;
