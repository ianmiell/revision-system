

```
CREATE TABLE category (
       category_id integer primary key not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       category text not null,
       certification text,
       unique(category, certification)
);
CREATE TABLE question_category (
       question_category_id integer primary key not null,
       question_id integer not null,
       category_id integer not null,
       importance integer default 50 not null check (importance > 0 and importance <= 100),
       unique(question_id, category_id),
       foreign key(question_id) references question(question_id),
       foreign key(category_id) references question(category_id)
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
       result text not null,
       foreign key(question_id) references question(question_id)
);
```
