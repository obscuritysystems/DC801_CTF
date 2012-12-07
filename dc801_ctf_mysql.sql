CREATE TABLE teams(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
created DATETIME,
name VARCHAR(254),
salt VARCHAR(254),
UNIQUE KEY (name),
UNIQUE KEY (salt),
PRIMARY KEY(id)
) ENGINE=InnoDB;


CREATE TABLE flags(
id INT UNSIGNED AUTO_INCREMENT,
created DATETIME,
text TEXT,
points DOUBLE,
team_owner_id INT UNSIGNED,
FOREIGN KEY (`team_owner_id`) REFERENCES `teams` (`id`)
PRIMARY KEY(id)
)ENGINE=InnoDB;


CREATE TABLE flag_hashes(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
submission_team_id INT UNSIGNED,
flag_id INT UNSIGNED,
hash VARCHAR(254),
PRIMARY KEY (id),
FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`),
FOREIGN KEY (`flag_id`) REFERENCES `flags` (`id`)
ower_team_id INT UNSIGNED,
)ENGINE=InnoDB;

CREATE TABLE captures(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
team_id INT UNSIGNED,
flag_id INT UNSIGNED,
captured DATETIME,
hash_id INT UNSIGNED,
PRIMARY KEY (id),
FOREIGN KEY (`hash_id`) REFERENCES `flag_hashes` (`id`)
)ENGINE=InnoDB;

CREATE TABLE submission_log(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
handle varchar(254),
team_id INT UNSIGNED,
submited DATETIME,
valid TINYINT,
hash VARCHAR(254),
PRIMARY KEY (id),
FOREIGN KEY (`team_id`) REFERENCES `teams` (`id`)
)ENGINE=InnoDB;


