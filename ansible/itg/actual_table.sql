USE metminidb;
CREATE TABLE actual
(
id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
ts_local DATETIME NOT NULL,
ts_utc DATETIME NOT NULL,
julian INT NOT NULL,
hour_utc INT NOT NULL,
location VARCHAR(64) NOT NULL,
main VARCHAR(32) NOT NULL,
description VARCHAR(32) NOT NULL,
pressure INT NOT NULL,
wind_speed FLOAT NOT NULL,
wind_deg INT NOT NULL,
wind_quadrant VARCHAR(8) NOT NULL,
wind_strength INT NOT NULL,
wind_gust FLOAT NOT NULL,
temp FLOAT NOT NULL,
feels_like FLOAT NOT NULL,
dew_point FLOAT NOT NULL,
uvi FLOAT NOT NULL,
humidity INT NOT NULL,
visibility INT NOT NULL,
rain FLOAT NOT NULL,
snow FLOAT NOT NULL,
coverage INT NOT NULL,
source VARCHAR(32) NOT NULL,
lat VARCHAR(8) NOT NULL,
lon VARCHAR(8) NOT NULL,
tz VARCHAR(32) NOT NULL,
tz_offset INT NOT NULL,
ts_epoch INT NOT NULL,
sunrise_local TIMESTAMP NOT NULL,
sunset_local TIMESTAMP NOT NULL
);


