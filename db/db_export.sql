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
INSERT INTO tag VALUES(3,'AWS Associate Developer Exam','','A');
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
INSERT INTO question_tag VALUES(5,1);
INSERT INTO question_tag VALUES(5,2);
INSERT INTO question_tag VALUES(6,1);
INSERT INTO question_tag VALUES(6,2);
INSERT INTO question_tag VALUES(7,1);
INSERT INTO question_tag VALUES(7,2);
INSERT INTO question_tag VALUES(8,1);
INSERT INTO question_tag VALUES(8,2);
INSERT INTO question_tag VALUES(9,1);
INSERT INTO question_tag VALUES(9,2);
INSERT INTO question_tag VALUES(10,1);
INSERT INTO question_tag VALUES(10,2);
INSERT INTO question_tag VALUES(11,3);
INSERT INTO question_tag VALUES(12,3);
INSERT INTO question_tag VALUES(13,3);
INSERT INTO question_tag VALUES(14,3);
INSERT INTO question_tag VALUES(15,3);
INSERT INTO question_tag VALUES(16,3);
INSERT INTO question_tag VALUES(17,3);
INSERT INTO question_tag VALUES(18,3);
INSERT INTO question_tag VALUES(19,3);
INSERT INTO question_tag VALUES(20,3);
CREATE TABLE question (
       question_id integer primary key not null,
       date_added integer default current_timestamp not null,
       question text not null,
       answer text not null,
       status text default 'A' not null check (status = 'A' or status = 'I'), ask_after integer,
       unique(question)
);
INSERT INTO question VALUES(1,'2020-12-16 16:45:21','What is EC2?','Amazon''s virtual compute service.','I',NULL);
INSERT INTO question VALUES(2,'2020-12-16 16:46:21','What is RDS?','Amazon''s virtual relational database service.','I',NULL);
INSERT INTO question VALUES(3,'2020-12-19 12:19:04','What is Global Accelerator?','Uses Anycast IPs to speed up connections to edge locations. It also has healthchecks and DDoS protection','A',NULL);
INSERT INTO question VALUES(4,'2020-12-19 12:20:05','What is Unicast IP vs Anycast IP?','Unicast is normal IP, Anycast is multiple servers have an IP, and user routed to nearest one. It goes through the edge location.','A',NULL);
INSERT INTO question VALUES(5,'2020-12-23 09:28:16.587','What is the difference between Global Accelerator vs CloudFront?','CloudFront content is served at the edge. Accelerator proxies packets, good fit for gaming (UDP etc).','A',NULL);
INSERT INTO question VALUES(6,'2020-12-19 13:01:20',replace('Is a new AMI available across all regions?\n','\n',char(10)),replace('No, but it can be copied to other regions and gets a new AMI id.\n','\n',char(10)),'A','2020-12-23');
INSERT INTO question VALUES(7,'2020-12-19 13:01:20',replace('What are the three parts to an AMI?\n','\n',char(10)),replace('They are: 1) Root volume 2) Launch perms 3) Volumes to attach on launch\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(8,'2020-12-19 13:01:20',replace('AMIs are public by default. True or False?\n','\n',char(10)),replace('False\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(9,'2020-12-19 13:01:20',replace('How can AMIs be shared?\n','\n',char(10)),replace('By adding the account number you want to share it with, or copy to another region. When share, you can specify that they can''t just copy it directly to someone else (tho they can spin up an EC2 and make an image from that).\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(10,'2020-12-19 13:01:20',replace('How do you copy a Billing Product AMI?\n','\n',char(10)),replace('EXAM TIP: You can''t if it''s a billing product. In that case you''d have to spin up an EC2 instance and snapshot that, and turn that into an AMI.\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(11,'2020-12-19 16:23:32',replace('What is Cloud Sight?\n','\n',char(10)),replace('Image recognition API\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(12,'2020-12-19 16:23:32',replace('What is Code Commit?\n','\n',char(10)),replace('AWS''s version of GitHub\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(13,'2020-12-19 16:23:32',replace('What is Code Deploy?\n','\n',char(10)),replace('Automates code deployment to Amazon instances\n','\n',char(10)),'I',NULL);
INSERT INTO question VALUES(14,'2020-12-19 16:23:32',replace('What is code pipeline?\n','\n',char(10)),replace('Builds test and deploys code on changes\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(15,'2020-12-19 16:23:32',replace('What is device farm?\n','\n',char(10)),replace('Device simulation\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(16,'2020-12-19 16:23:32',replace('What is workdocs?\n','\n',char(10)),replace('Document store for enterprises\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(17,'2020-12-19 16:23:32',replace('What is Work Mail?\n','\n',char(10)),replace('Exchange for AWS\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(18,'2020-12-19 16:23:32',replace('What is Workspaces?\n','\n',char(10)),replace('Virtual desktops in the cloud\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(19,'2020-12-19 16:23:32',replace('How often is the drive backed up? Which drive?\n','\n',char(10)),replace('D drive, every 12 hours\n','\n',char(10)),'A',NULL);
INSERT INTO question VALUES(20,'2020-12-19 16:23:32',replace('You will need an AWS account to log into a workspace instance. True or False?\n','\n',char(10)),replace('False\n','\n',char(10)),'A',NULL);
CREATE TABLE answer (
       answer_id integer primary key not null,
       question_id integer not null,
       date_answered integer default current_timestamp not null,
       result text not null check (result = 'R' or result = 'W'),
       foreign key(question_id) references question(question_id)
);
INSERT INTO answer VALUES(1,8,'2020-12-20 16:49:32','R');
INSERT INTO answer VALUES(2,4,'2020-12-20 16:49:37','R');
INSERT INTO answer VALUES(3,5,'2020-12-20 16:49:46','R');
INSERT INTO answer VALUES(4,9,'2020-12-20 16:49:55','W');
INSERT INTO answer VALUES(5,3,'2020-12-20 16:50:01','R');
INSERT INTO answer VALUES(6,6,'2020-12-20 16:50:04','R');
INSERT INTO answer VALUES(7,6,'2020-12-20 17:03:04','R');
INSERT INTO answer VALUES(8,5,'2020-12-20 17:03:11','W');
INSERT INTO answer VALUES(9,6,'2020-12-21 14:02:10','R');
INSERT INTO answer VALUES(10,7,'2020-12-21 14:06:37','R');
COMMIT;
