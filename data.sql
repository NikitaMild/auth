CREATE DATABASE  if not exists users_data DEFAULT CHARACTER SET 'utf8';

use users_data;
create table if not exists user_atributes
	( user_login   VARCHAR(64)
	, home_dir     VARCHAR(128)
	, token        VARCHAR(128)
	, PRIMARY KEY (user_login)
	)
;
