PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE tag (
       tag_id integer primary key not null,
       tag text not null,
       notes text,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       unique(tag)
);
INSERT INTO tag VALUES(1,'AWS Associate Solutions Architect Exam','','A');
INSERT INTO tag VALUES(2,'AWS Professional Solutions Architect Exam','','A');
CREATE TABLE question_tag (
       question_id integer not null,
       tag_id integer not null,
       foreign key(question_id) references question(question_id),
       foreign key(tag_id) references tag(tag_id),
       primary key(question_id, tag_id)
);
INSERT INTO question_tag VALUES(1,1);
INSERT INTO question_tag VALUES(1,2);
INSERT INTO question_tag VALUES(2,1);
INSERT INTO question_tag VALUES(2,2);
INSERT INTO question_tag VALUES(3,1);
INSERT INTO question_tag VALUES(3,2);
INSERT INTO question_tag VALUES(4,1);
INSERT INTO question_tag VALUES(4,2);
CREATE TABLE question (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       question text not null,
       answer text not null,
       status text default 'A' not null check (status = 'A' or status = 'I'),
       unique(question)
);
INSERT INTO question VALUES(1,'2020-12-16 16:45:21','What is EC2?','Amazon''s virtual compute service.','I');
INSERT INTO question VALUES(2,'2020-12-16 16:46:21','What is RDS?','Amazon''s virtual relational database service.','I');
INSERT INTO question VALUES(3,'2020-12-19 12:19:04','What is Global Accelerator?','Uses Anycast IPs to speed up connections to edge locations. It also has healthchecks and DDoS protection','A');
INSERT INTO question VALUES(4,'2020-12-19 12:20:05','What is Unicast IP vs Anycast IP?','Unicast is normal IP, Anycast is multiple servers have an IP, and user routed to nearest one. It goes through the edge location.','A');
CREATE TABLE answer (
       answer_id integer primary key not null,
       question_id integer not null,
       date_answered integer default current_timestamp not null,
       result text not null check (result = 'R' or result = 'W'),
       foreign key(question_id) references question(question_id)
);
INSERT INTO answer VALUES(1,1,'2020-12-19 11:45:08','R');
INSERT INTO answer VALUES(2,2,'2020-12-19 11:45:13','R');
INSERT INTO answer VALUES(3,1,'2020-12-19 11:46:03','R');
INSERT INTO answer VALUES(4,2,'2020-12-19 11:46:06','R');
INSERT INTO answer VALUES(5,1,'2020-12-19 11:48:58','R');
INSERT INTO answer VALUES(6,2,'2020-12-19 11:49:06','R');
INSERT INTO answer VALUES(7,1,'2020-12-19 12:07:56','W');
INSERT INTO answer VALUES(8,2,'2020-12-19 12:08:00','W');
COMMIT;
