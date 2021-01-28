CREATE USER 'zhique_service'@'%' IDENTIFIED BY "zhique_service";
CREATE DATABASE zhique_service DEFAULT CHARACTER SET utf8;
GRANT ALL PRIVILEGES ON zhique_service.* TO zhique_service@'%';
FLUSH PRIVILEGES;