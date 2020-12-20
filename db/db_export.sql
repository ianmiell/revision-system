PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tag (
       tag_id integer primary key not null,
       tag text not null,
       notes text,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       unique(tag)
);
CREATE TABLE question_tag (
       question_id integer not null,
       tag_id integer not null,
       foreign key(question_id) references question(question_id),
       foreign key(tag_id) references tag(tag_id),
       primary key(question_id, tag_id)
);
CREATE TABLE question (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       question text not null,
       answer text not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       unique(question)
);
CREATE TABLE answer (
       answer_id integer primary key not null,
       question_id integer not null,
       date_answered integer default current_timestamp not null,
       result text not null check (result = 'R' or result = 'W'),
       foreign key(question_id) references question(question_id)
);
COMMIT;
