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
INSERT INTO question_tag VALUES(11,1);
INSERT INTO question_tag VALUES(11,2);
INSERT INTO question_tag VALUES(12,1);
INSERT INTO question_tag VALUES(12,2);
INSERT INTO question_tag VALUES(13,1);
INSERT INTO question_tag VALUES(13,2);
INSERT INTO question_tag VALUES(14,1);
INSERT INTO question_tag VALUES(14,2);
INSERT INTO question_tag VALUES(15,1);
INSERT INTO question_tag VALUES(15,2);
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
INSERT INTO question VALUES(5,'2020-12-19 12:22:50','What is the difference between Global Accelerator vs CloudFront?','CloudFront content is served at the edge. Accelerator proxies packets, good fit for gaming (UDP etc).','A');
INSERT INTO question VALUES(6,'2020-12-19 13:01:20',replace('Is a new AMI available across all regions?\n','\n',char(10)),replace('No, but it can be copied to other regions and gets a new AMI id.\n','\n',char(10)),'A');
INSERT INTO question VALUES(7,'2020-12-19 13:01:20',replace('What are the three parts to an AMI?\n','\n',char(10)),replace('They are:\n','\n',char(10)),'A');
INSERT INTO question VALUES(8,'2020-12-19 13:01:20',replace('AMIs are public by default. True or False?\n','\n',char(10)),replace('False\n','\n',char(10)),'A');
INSERT INTO question VALUES(9,'2020-12-19 13:01:20',replace('How can AMIs be shared?\n','\n',char(10)),replace('By adding the account number you want to share it with, or copy to another region. When share, you can specify that they can''t just copy it directly to someone else (tho they can spin up an EC2 and make an image from that).\n','\n',char(10)),'A');
INSERT INTO question VALUES(10,'2020-12-19 13:01:20',replace('How do you copy a Billing Product AMI?\n','\n',char(10)),replace('EXAM TIP: You can''t if it''s a billing product. In that case you''d have to spin up an EC2 instance and snapshot that, and turn that into an AMI.\n','\n',char(10)),'A');
INSERT INTO question VALUES(11,'2020-12-19 13:01:20',replace('How do you get rid of ssh keys for added security when creating an AMI?\n','\n',char(10)),replace('Use the shred command\n','\n',char(10)),'A');
INSERT INTO question VALUES(12,'2020-12-19 13:01:20',replace('How do you get rid of the bash history for added security when creating an AMI?\n','\n',char(10)),replace('history -c\n','\n',char(10)),'A');
INSERT INTO question VALUES(13,'2020-12-19 13:01:20',replace('What is the difference between INSTANCE STORE (EPHEMERAL STORAGE) and EBS store when starting AMIs?\n','\n',char(10)),replace('You can''t stop an instance store. You can''t therefore move an instance store. Instance store can''t be detached. This is at the AMI level. Both can be rebooted. EBS storage can be marked as kept on restart.\n','\n',char(10)),'A');
INSERT INTO question VALUES(14,'2020-12-19 13:01:20',replace('By default, EBS store instances do not delete on termination. True or False?\n','\n',char(10)),replace('False. They are deleted, but you can stop this.\n','\n',char(10)),'A');
INSERT INTO question VALUES(15,'2020-12-19 13:01:20',replace('What does copying an AMI not copy?\n','\n',char(10)),replace('Tags, launch permissions, bucket permissions\n','\n',char(10)),'A');
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
