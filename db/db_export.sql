PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE question_category (
       question_category_id integeer primary key not null,
       question_id integer not null,
       category text not null,
       certification text,
       importance integer default 50 not null check (importance > 0 and importance <= 100),
       unique(category, certification),
       unique(question_id, certification),
       foreign key(question_id) references question(question_id)
);
CREATE TABLE question (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       question text not null,
       answer text not null,
       unique(question)
);
CREATE TABLE answer (
       answer_id integer primary key not null,
       question_id integer not null,
       date_added integer default current_timestamp not null,
       result text not null,
       foreign key(question_id) references question(question_id)
);
COMMIT;
