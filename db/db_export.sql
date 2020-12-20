PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE certification (
       certification_id integer primary key not null,
       certification text not null,
       unique(certification)
);
CREATE TABLE category (
       category_id integer primary key not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       category text not null,
       unique(category)
);
CREATE TABLE question_category_certification (
       question_id integer not null,
       category_id integer not null,
       certification_id integer not null,
       foreign key(question_id) references question(question_id),
       foreign key(category_id) references category(category_id),
       foreign key(certification_id) references certification(certification_id),
       primary_key(question_id, category_id, certification_id)
);
CREATE TABLE question (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       question text not null,
       answer text not null,
       unique(question)
);
CREATE TABLE question_status (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       foreign key(question_id) references question(question_id)
);
CREATE TABLE answer (
       answer_id integer primary key not null,
       question_id integer not null,
       date_answered integer default current_timestamp not null,
       result text not null check (status = 'R' or status = 'W'),
       foreign key(question_id) references question(question_id)
);
COMMIT;
