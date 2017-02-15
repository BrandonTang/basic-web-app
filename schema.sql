drop table if exists users;
create table users (
  user_id integer primary key autoincrement,
	username varchar(64) not null,
	password varchar(64) not null
);

drop table if exists posts;
create table posts (
  post_id integer primary key autoincrement,
  username varchar(64) not null,
  image varchar(256) not null,
  caption varchar(256) null,
  constraint fk_users
    foreign key (username)
    references users(username)
);