use classmanagement;
CREATE TABLE `course_info` (
  `id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `course_name` varchar(45) DEFAULT NULL,
  `course_hour` float DEFAULT NULL,
  `course_degree` float DEFAULT NULL,
  `course_type` varchar(45) DEFAULT NULL,
  `class_name` varchar(45) DEFAULT NULL,
  `course_time` datetime DEFAULT NULL,
  `suit_teacher` varchar(200) DEFAULT NULL,
  `teacher_claiming` varchar(200) DEFAULT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `year` varchar(45) DEFAULT NULL,
  `insert_time` timestamp(6) NULL DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SELECT * FROM classmanagement.course_info;