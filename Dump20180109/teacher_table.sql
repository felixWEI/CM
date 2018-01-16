use classmanagement;
CREATE TABLE `teacher_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` int(11) NOT NULL,
  `teacher_name` varchar(45) DEFAULT NULL,
  `first_semester` float DEFAULT NULL,
  `second_semester` float DEFAULT NULL,
  `claiming_course` varchar(1000) DEFAULT NULL,
  `insert_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
SELECT * FROM classmanagement.teacher_info;