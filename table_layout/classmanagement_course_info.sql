-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: classmanagement
-- ------------------------------------------------------
-- Server version	5.7.12-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course_info`
--

DROP TABLE IF EXISTS `course_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` varchar(45) NOT NULL,
  `course_name` varchar(45) NOT NULL,
  `student_type` varchar(45) NOT NULL,
  `year` varchar(45) DEFAULT NULL,
  `class_name` varchar(2000) NOT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `course_hour` float NOT NULL,
  `course_degree` float NOT NULL,
  `course_type` varchar(45) DEFAULT NULL,
  `allow_teachers` int(11) DEFAULT NULL,
  `times_every_week` int(11) DEFAULT NULL,
  `suit_teacher` varchar(200) DEFAULT NULL,
  `teacher_ordered` varchar(200) DEFAULT NULL,
  `teacher_auto_pick` varchar(200) DEFAULT NULL,
  `teacher_final_pick` varchar(200) DEFAULT NULL,
  `notes` varchar(200) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `language` varchar(45) DEFAULT '中文',
  `course_relate` varchar(45) DEFAULT NULL,
  `lock_state` tinyint(4) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_info`
--

LOCK TABLES `course_info` WRITE;
/*!40000 ALTER TABLE `course_info` DISABLE KEYS */;
INSERT INTO `course_info` VALUES (1,'HIST119003','文艺复兴史','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'赵立行','赵立行','赵立行','赵立行','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(2,'LAWS130023','税法','本科','2019-2020','本科-18_法学专业教育','二',36,9,'选修',1,1,'陈立','陈立','陈立','陈立','非精品课程','经济法学','中文','JM630041',0,'2019-04-05 20:51:09'),(3,'LAWS130021','毕业实习','本科','2019-2020','本科-16_法学专业教育','二',72,10,'必修',1,1,'孙南申','教学院长','孙南申','孙南申','非精品课程','综合','中文','',0,'2019-04-06 20:52:11'),(4,'LAWS130020','毕业论文','本科','2019-2020','本科-16_法学专业教育','二',72,10,'必修',1,1,'孙南申','教学院长','孙南申','孙南申','非精品课程','综合','中文','',0,'2019-04-06 20:51:30'),(5,'LAWS130027','婚姻家庭法','本科','2019-2020','本科-17_法学专业教育','一',54,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','非精品课程','民商法学','中文','JM630033',0,'2019-04-05 20:51:09'),(6,'LAWS130026','自然资源和环境保护法','本科','2019-2020','本科-18_法学专业教育','二',36,10,'必修',2,1,'陶蕾,张梓太','陶蕾,张梓太','张梓太,陶蕾','张梓太,陶蕾','非精品课程','环境与资源保护法学','中文','',0,'2019-04-05 20:51:09'),(7,'LAWS130025','公司法','本科','2019-2020','本科-18_法学专业教育','二',36,9,'选修',1,1,'白国栋,李小宁,张建伟','白国栋,李小宁,张建伟','李小宁,张建伟','李小宁,张建伟','非精品课程','民商法学','中文','JM630039',0,'2019-04-05 20:51:09'),(8,'LAWS130024','金融法','本科','2019-2020','本科-18_法学专业教育','二',36,9,'选修',1,1,'章武生,陈立','章武生,陈立','陈立,章武生','陈立,章武生','非精品课程','经济法学','中文','JM620015,JM630010',0,'2019-04-05 20:51:09'),(9,'927.008.1','商法','本科','2019-2020','本科-18_第二专业教学','二',54,10,'必修',1,1,'许凌艳','许凌艳','许凌艳','许凌艳','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(10,'LAWS130029','国际金融法','本科','2019-2020','本科-17_法学专业教育','一',54,9,'选修',1,1,'章武生,陈立','章武生,陈立','陈立,章武生','陈立,章武生','非精品课程','国际法学','英文','JM630028',0,'2019-04-05 20:51:09'),(11,'LAWS130028','劳动法','本科','2019-2020','本科-17_法学专业教育','一',36,8,'选修',1,1,'','许多奇,李小宁,白国栋,蒋云蔚',NULL,NULL,'非精品课程','民商法学','中文','JM630037',1,'2019-04-05 20:52:26'),(12,'SOSC120015.02','宪法','本科','2019-2020','本科-19_基础教育','二',54,10,'必修',1,1,'潘伟杰,涂云新,王蔚','潘伟杰,涂云新,王蔚','潘伟杰,潘伟杰','潘伟杰,潘伟杰','精品课程','宪法学与行政法学','中文','',0,'2019-04-05 20:51:09'),(13,'927.010.1','刑法Ⅱ','本科','2019-2020','本科-18_第二专业教学','一',36,10,'必修',1,1,'蒋云蔚','蒋云蔚','蒋云蔚','蒋云蔚','非精品课程','刑法学','中文','',0,'2019-04-05 20:51:09'),(14,'LAW620041','环境法原理','法学硕士','2019-2020','法学硕士-19_环境与资源保护法学','一',54,4,'必修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','非精品课程','环境与资源保护法学','','',0,'2019-04-05 20:51:09'),(15,'927.011.1','刑法Ⅰ','本科','2019-2020','本科-19_第二专业教学','二',72,0,'必修',0,0,'','',NULL,NULL,'非精品课程','刑法学','中文','',1,'2019-04-05 20:51:09'),(16,'927.013.1','行政法','本科','2019-2020','本科-19_第二专业教学','二',54,10,'必修',1,1,'杨晓畅','杨晓畅','杨晓畅','杨晓畅','非精品课程','宪法学与行政法学','中文','',0,'2019-04-06 21:02:22'),(17,'927.005.1','民法Ⅱ','本科','2019-2020','本科-18_第二专业教学','一',54,10,'必修',1,1,'施鸿鹏','施鸿鹏','施鸿鹏','施鸿鹏','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(18,'LAWS119005.02','犯罪与文明','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(19,'LAWS119005.01','犯罪与文明','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(20,'LAW630114','家事法专题','法学硕士','2019-2020','法学硕士-19_民商法学','二',36,4,'选修',1,1,'刘士国,李世刚,孙晓屏,王俊','刘士国,李世刚,孙晓屏,王俊','李世刚','李世刚','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(21,'LAW630115','债法专题','法学硕士','2019-2020','法学硕士-19_民商法学','二',36,4,'选修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','施鸿鹏','施鸿鹏','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(22,'LAWS130054','比较法','本科','2019-2020','本科-17_法学专业教育','一',54,0,'选修',0,0,'','',NULL,NULL,'非精品课程','法学理论','英文','JM620053',1,'2019-04-05 20:51:09'),(23,'LAWS130055','卓越法务前沿讲座','本科','2019-2020','本科-17_法学专业教育','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(24,'LAWS130052','国际商法','本科','2019-2020','本科-17_法学专业教育','二',54,9,'选修',1,1,'高凌云','高凌云','高凌云','高凌云','非精品课程','国际法学','英文','JM630030',0,'2019-04-05 20:51:09'),(25,'LAWS130051','外国民事诉讼法','本科','2019-2020','本科-17_法学专业教育','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','诉讼法学','中文','',1,'2019-04-05 20:51:09'),(26,'927.004.1','国际私法','本科','2019-2020','本科-18_第二专业教学','二',54,10,'必修',1,1,'陈力','陈力','陈力','陈力','非精品课程','国际法学','中文','',0,'2019-04-05 20:51:09'),(27,'927.014.1','中国法制史','本科','2019-2020','本科-19_第二专业教学','一',54,10,'必修',1,1,'赖骏楠,孟烨','赖骏楠,孟烨','孟烨,赖骏楠','孟烨,赖骏楠','非精品课程','法律史','中文','',0,'2019-04-05 20:51:09'),(28,'LAW620053','中国当代社会法理学问题','法学硕士','2019-2020','法学硕士-19_法学理论','一',54,4,'必修',1,1,'孙笑侠','孙笑侠','孙笑侠','孙笑侠','非精品课程','法学理论','','',0,'2019-04-05 20:51:09'),(29,'LAWS110013.01','合同法的理论和实践','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(30,'LAWS110013.02','合同法的理论和实践','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(31,'LAW630034','司法制度专题','法学硕士','2019-2020','法学硕士-19_诉讼法学 法律硕士-18_法律硕士（法学）','二',36,5,'选修',1,1,'章武生,徐美君','章武生,徐美君','徐美君','徐美君','非精品课程','诉讼法学','','',0,'2019-04-05 20:51:09'),(32,'JM620038','民法专题','法律硕士','2019-2020','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'胡鸿高,季立刚,张建伟','胡鸿高,季立刚,张建伟','胡鸿高','胡鸿高','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(33,'LAW630125','自然资源保护法专题','法学硕士','2019-2020','法学硕士-19_环境与资源保护法学','二',36,5,'选修',1,1,'张梓太','张梓太','张梓太','张梓太','非精品课程','环境与资源保护法学','','',0,'2019-04-05 20:51:09'),(34,'LAW630122','知识产权法','法学硕士','2019-2020','法学硕士-19_民商法学','二',36,4,'选修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','班天可','班天可','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(35,'LAWS130045','西方法律思想史','本科','2019-2020','本科-16_法学专业教育','一',36,9,'选修',1,1,'杨晓畅','杨晓畅','杨晓畅','杨晓畅','非精品课程','法律史','中文','',0,'2019-04-05 20:51:09'),(36,'LAWS130044','中国法律思想史','本科','2019-2020','本科-16_法学专业教育','一',36,9,'选修',1,1,'郭建,王志强,赖骏楠','郭建,王志强,赖骏楠','郭建,郭建','郭建,郭建','非精品课程','法律史','中文','',0,'2019-04-05 20:51:09'),(37,'LAWS130046','外国刑事诉讼法','本科','2019-2020','本科-16_法学专业教育','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','诉讼法学','中文','',1,'2019-04-05 20:51:09'),(38,'LAWS130041','国际商事仲裁法','本科','2019-2020','本科-17_法学专业教育','二',36,9,'选修',1,1,'陈力','陈力','陈力','陈力','非精品课程','国际法学','英文','JM630042',0,'2019-04-05 20:51:09'),(39,'LAWS130043','刑事政策','本科','2019-2020','本科-18_法学专业教育','二',36,9,'选修',1,1,'汪明亮','汪明亮','汪明亮','汪明亮','非精品课程','刑法学','中文','JM630044',0,'2019-04-05 20:51:09'),(40,'LAWS130042','海商法','本科','2019-2020','本科-17_法学专业教育 本科-17_法学专业教育','二',36,9,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','非精品课程','民商法学','中文','JM630043',0,'2019-04-05 20:51:09'),(41,'JM620053','比较法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（法学）国际班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'涂云新,陈立,赵立行','涂云新,陈立,赵立行','赵立行,涂云新','赵立行,涂云新','非精品课程','综合','','LAWS130074',0,'2019-04-05 20:51:09'),(42,'ICES110002.02','留学生高级汉语Ⅱ','本科','2019-2020','本科-18_','二',72,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(43,'LAWS110017','法治社会的公民权利','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(44,'LAWS160008','国际法','本科','2019-2020','本科-17_跨校辅修教学','二',54,10,'必修',1,1,'马忠法','马忠法','马忠法','马忠法','非精品课程','国际法学','中文','',0,'2019-04-05 20:51:09'),(45,'LAWS160009','国际经济法','本科','2019-2020','本科-17_跨校辅修教学','二',54,10,'必修',1,1,'何力','何力','何力','何力','非精品课程','国际法学','中文','',0,'2019-04-05 20:51:09'),(46,'LAW620065','西方法律史专题','法学硕士','2019-2020','法学硕士-19_法律史','一',54,4,'必修',1,1,'赵立行','赵立行','赵立行','赵立行','非精品课程','法律史','','',0,'2019-04-05 20:51:09'),(47,'LAWS160004','债法（合同法）','本科','2019-2020','本科-18_跨校辅修教学','二',54,10,'必修',1,1,'班天可','班天可','班天可','班天可','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(48,'LAWS160005','商法','本科','2019-2020','本科-17_跨校辅修教学','一',54,10,'必修',1,1,'陈立','陈立','陈立','陈立','非精品课程','民商法学','中文','',0,'2019-04-06 21:12:32'),(49,'LAWS160006','民事诉讼法','本科','2019-2020','本科-18_跨校辅修教学','二',54,10,'必修',1,1,'杨严炎','杨严炎','杨严炎','杨严炎','非精品课程','诉讼法学','中文','',0,'2019-04-05 20:51:09'),(50,'LAWS160007','知识产权法','本科','2019-2020','本科-17_跨校辅修教学','一',54,10,'必修',1,1,'王俊','王俊','王俊','王俊','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(51,'LAWS160001','宪法学','本科','2019-2020','本科-18_跨校辅修教学','一',54,10,'必修',1,1,'涂云新','涂云新','涂云新','涂云新','非精品课程','宪法学与行政法学','中文','',0,'2019-04-05 20:51:09'),(52,'LAWS160002','民法总论','本科','2019-2020','本科-18_跨校辅修教学','一',54,10,'必修',1,1,'班天可','班天可','班天可','班天可','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(53,'LAWS130039','台港澳法','本科','2019-2020','本科-17_法学专业教育','二',36,9,'选修',1,1,'郭建','郭建','郭建','郭建','非精品课程','法律史','中文','JM630038',0,'2019-04-05 20:51:09'),(54,'LAWS110017.01','法治社会的公民权利（邯郸）','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'姚军','姚军','姚军','姚军','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(55,'LAWS110017.02','法治社会的公民权利（张江）','本科','2019-2020','本科-_通识教育','一',36,8,'选修',1,1,'姚军','姚军','姚军','姚军','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(56,'SOSC120015.01','宪法','本科','2019-2020','本科-19_基础教育','一',54,10,'必修',2,1,'潘伟杰,涂云新,王蔚','潘伟杰,涂云新,王蔚','王蔚,王蔚,潘伟杰,潘伟杰','王蔚,王蔚,潘伟杰,潘伟杰','精品课程','宪法学与行政法学','中文','',0,'2019-04-05 20:51:09'),(57,'927.024.1','法理学导论','本科','2019-2020','本科-19_第二专业教学','一',54,10,'必修',1,1,'史大晓','史大晓','史大晓','史大晓','非精品课程','法学理论','中文','',0,'2019-04-05 20:51:09'),(58,'LAWS119004.01','法治理念与实践','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'张光杰','张光杰','张光杰','张光杰','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(59,'LAWS119004.02','法治理念与实践','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'张光杰','张光杰','张光杰','张光杰','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(60,'LAW630038','国际投资法研究 ','法律硕士','2019-2020','法律硕士-18_法律硕士（法学）','一',36,5,'选修',1,1,'孙南申','孙南申','孙南申','孙南申','非精品课程','国际法学','','',0,'2019-04-05 20:51:09'),(61,'LAWS110025.01','日本战后法律事件的解读','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(62,'JM620024','法理学专题','法律硕士','2019-2020','法律硕士-18_法律硕士（法学）','一',36,7,'必修',1,1,'张光杰','张光杰','张光杰','张光杰','非精品课程','法学理论','','',0,'2019-04-05 20:51:09'),(63,'927.006.1','民法Ⅰ','本科','2019-2020','本科-19_第二专业教学','二',54,10,'必修',1,1,'施鸿鹏','施鸿鹏','施鸿鹏','施鸿鹏','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(64,'LAWS110025.02','日本战后法律事件的解读','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(65,'927.012.1','刑事诉讼法','本科','2019-2020','本科-18_第二专业教学','一',54,10,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','非精品课程','诉讼法学','中文','',0,'2019-04-05 20:51:09'),(66,'JM620023','环境资源法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学）','二',36,8,'必修',1,1,'陶蕾,李传轩,张梓太','陶蕾,李传轩,张梓太','张梓太,李传轩','张梓太,李传轩','非精品课程','环境与资源保护法学','','',0,'2019-04-05 20:51:09'),(67,'JM620022','知识产权法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学）','二',36,8,'必修',1,1,'丁文杰,王俊','丁文杰,王俊','丁文杰,王俊','丁文杰,王俊','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(68,'LAWS119002.02','人权与法','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'侯健','侯健','侯健','侯健','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(69,'LAWS119002.01','人权与法','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'侯健','侯健','侯健','侯健','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(70,'927.007.1','民事诉讼法','本科','2019-2020','本科-18_第二专业教学','一',54,8,'必修',1,1,'杨严炎','杨严炎','杨严炎','杨严炎','非精品课程','诉讼法学','中文','',0,'2019-04-05 20:51:09'),(71,'LAWS110009.02','国际经济合同','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(72,'LAWS110009.01','国际经济合同','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(73,'LAW620074','民法专题研究','法学硕士','2019-2020','法学硕士-19_民商法学','一',54,4,'必修',1,1,'胡鸿高,季立刚,张建伟','胡鸿高,季立刚,张建伟','季立刚','季立刚','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(74,'LAW620075','商法专题研究','法学硕士','2019-2020','法学硕士-19_民商法学','一',54,4,'必修',1,1,'许多奇,李小宁,白国栋,蒋云蔚','许多奇,李小宁,白国栋,蒋云蔚','许多奇','许多奇','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(75,'LAWS160010','刑事诉讼法','本科','2019-2020','本科-18_跨校辅修教学','二',54,10,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','非精品课程','诉讼法学','中文','',0,'2019-04-05 20:51:09'),(76,'LAWS119006.02','现代金融与法律','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(77,'LAWS119006.01','现代金融与法律','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(78,'LAW620079','刑事诉讼法专题','法学硕士','2019-2020','法学硕士-19_诉讼法学','一',54,4,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','非精品课程','诉讼法学','','',0,'2019-04-05 20:51:09'),(79,'LAWS130064','民法Ⅱ','本科','2019-2020','本科-18_法学专业教育','一',54,8,'必修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','施鸿鹏,施鸿鹏','施鸿鹏,施鸿鹏','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:09'),(80,'ICES110001.01','留学生高级汉语I','本科','2019-2020','本科-19_','一',72,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','','',1,'2019-04-05 20:51:09'),(81,'JM630026','医事法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',36,6,'选修',1,1,'刘士国,李世刚,孙晓屏,王俊','刘士国,李世刚,孙晓屏,王俊','李世刚','李世刚','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(82,'JM630009','物权法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',36,7,'选修',1,1,'李世刚,蒋云蔚','李世刚,蒋云蔚','李世刚','李世刚','非精品课程','民商法学','','LAW630112',0,'2019-04-05 20:51:09'),(83,'LAW830060','国际经济法研究','博士','2019-2020','博士-18_博士','二',36,3,'选修',1,1,'龚柏华,何力,马忠法','龚柏华,何力,马忠法','龚柏华','龚柏华','非精品课程','国际法学','','',0,'2019-04-05 20:51:09'),(84,'LAW630027','欧盟法专题','法学硕士','2019-2020','法学硕士-19_国际法学','二',36,3,'选修',1,1,'陆志安','陆志安','陆志安','陆志安','非精品课程','国际法学','','',0,'2019-04-05 20:51:09'),(85,'LAWS119008.01','全球化时代的法律冲突和对话','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(86,'LAWS119008.02','全球化时代的法律冲突和对话','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(87,'LAWS110014.01','知识经济与知识产权管理','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:09'),(88,'LAWS110014.02','知识经济与知识产权管理','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','非精品课程','综合','中文','',0,'2019-04-05 20:51:09'),(89,'JM620006','刑事诉讼法学','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班','二',36,6,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','非精品课程','诉讼法学','','',0,'2019-04-05 20:51:09'),(90,'SOSC120003.01','法理学导论','本科','2019-2020','本科-19_基础教育','一',54,10,'必修',3,1,'侯健,史大晓,杨晓畅,孙笑侠','侯健,史大晓,杨晓畅,孙笑侠','杨晓畅,杨晓畅,史大晓,孙笑侠,侯健,侯健','杨晓畅,杨晓畅,史大晓,孙笑侠,侯健,侯健','精品课程','法学理论','中文','',0,'2019-04-05 20:51:09'),(91,'927.009.1','宪法','本科','2019-2020','本科-19_第二专业教学','一',54,10,'必修',1,1,'涂云新','涂云新','涂云新','涂云新','非精品课程','宪法学与行政法学','中文','',0,'2019-04-05 20:51:09'),(92,'JM630033','婚姻家庭法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','一',36,6,'选修',1,1,'胡鸿高,季立刚,张建伟','胡鸿高,季立刚,张建伟','胡鸿高','胡鸿高','非精品课程','民商法学','','LAWS130027',0,'2019-04-05 20:51:09'),(93,'JM630037','劳动法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','一',36,6,'选修',1,1,'许多奇,李小宁,白国栋,蒋云蔚','许多奇,李小宁,白国栋,蒋云蔚','白国栋','白国栋','非精品课程','民商法学','','LAWS130028',0,'2019-04-05 20:51:09'),(94,'JM630034','侵权责任法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','一',36,6,'选修',1,1,'胡鸿高,季立刚,张建伟','胡鸿高,季立刚,张建伟','张建伟','张建伟','非精品课程','民商法学','','',0,'2019-04-05 20:51:09'),(95,'LAW620080','环境法热点问题研究','法学硕士','2019-2020','法学硕士-19_环境与资源保护法学','一',54,6,'必修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','非精品课程','环境与资源保护法学','','',0,'2019-04-05 20:51:10'),(96,'SOSC120016.01','经济法','本科','2019-2020','本科-18_基础教育','二',54,10,'必修',2,1,'施鸿鹏,陈立','施鸿鹏,陈立','陈立,施鸿鹏','陈立,施鸿鹏','非精品课程','经济法学','中文','',0,'2019-04-05 20:51:10'),(97,'LAW620082','国际经济法研究','法学硕士','2019-2020','法学硕士-19_国际法学','一',54,4,'必修',1,1,'龚柏华,何力,马忠法','龚柏华,何力,马忠法','何力','何力','非精品课程','国际法学','','',0,'2019-04-05 20:51:10'),(98,'LAWS130074','比较法','本科','2019-2020','本科-18_法学专业教育','二',36,9,'选修',1,1,'涂云新,陈立,赵立行','涂云新,陈立,赵立行','赵立行,涂云新','赵立行,涂云新','非精品课程','法学理论','英文','JM620053',0,'2019-04-05 20:51:10'),(99,'LAWS130019','法律实务','本科','2019-2020','本科-16_法学专业教育','一',54,10,'必修',1,1,'章武生,陈立','章武生,陈立','章武生,章武生','章武生,章武生','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(100,'927.002.1','国际法','本科','2019-2020','本科-19_第二专业教学','二',54,10,'必修',1,1,'朱丹,王志强','朱丹','朱丹,朱丹','朱丹,朱丹','非精品课程','国际法学','中文','',0,'2019-04-06 21:08:12'),(101,'LAWS130012','商法','本科','2019-2020','本科-17_法学专业教育','一',54,10,'必修',1,1,'李小宁','李小宁','李小宁','李小宁','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:10'),(102,'LAWS130013','专业英语I(法律)','本科','2019-2020','本科-17_法学专业教育','一',36,10,'必修',1,1,'高凌云','高凌云','高凌云','高凌云','非精品课程','综合','英文','',0,'2019-04-05 20:51:10'),(103,'LAWS130016','专业英语Ⅱ（法律）','本科','2019-2020','本科-17_法学专业教育','二',54,10,'必修',1,1,'高凌云','高凌云','高凌云','高凌云','精品课程','民商法学','英文','',0,'2019-04-05 20:51:10'),(104,'LAWS130017','专业英语Ⅲ（法律)','本科','2019-2020','本科-16_法学专业教育','一',54,10,'必修',1,1,'王志强','王志强','王志强','王志强','非精品课程','综合','英文','',0,'2019-04-06 21:05:35'),(105,'LAWS130015','知识产权法','本科','2019-2020','本科-17_法学专业教育','二',54,8,'必修',1,1,'刘士国,李世刚,孙晓屏,王俊','刘士国,李世刚,孙晓屏,王俊','刘士国,刘士国','刘士国,刘士国','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:10'),(106,'LAW630112','物权法专题','法学硕士','2019-2020','法学硕士-19_民商法学','二',36,4,'选修',1,1,'葛江虬,施鸿鹏,丁文杰','葛江虬,施鸿鹏,丁文杰','葛江虬','葛江虬','非精品课程','民商法学','','JM630009',0,'2019-04-05 20:51:10'),(107,'LAWS130007','刑事诉讼法','本科','2019-2020','本科-18_法学专业教育','二',54,10,'必修',1,1,'刘天娇','刘天娇','刘天娇','刘天娇','精品课程','诉讼法学','中文','',0,'2019-04-06 21:04:21'),(108,'SOSC120016.02','经济法','本科','2019-2020','本科-_基础教育','一',54,10,'必修',1,1,'施鸿鹏,李传轩,葛江虬','施鸿鹏,李传轩,葛江虬','李传轩,葛江虬','李传轩,葛江虬','非精品课程','经济法学','中文','',0,'2019-04-05 20:51:10'),(109,'JM620057','国际法学','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学）','二',54,7,'必修',1,1,'何力,陆志安,王伟,朱丹','何力,陆志安,王伟,朱丹','王伟','王伟','非精品课程','国际法学','','',0,'2019-04-05 20:51:10'),(110,'LAW620014','中国法制史专题','法学硕士','2019-2020','法学硕士-19_法律史','一',54,4,'必修',1,1,'郭建,赖骏楠','郭建,赖骏楠','赖骏楠','赖骏楠','非精品课程','法律史','','',0,'2019-04-05 20:51:10'),(111,'LAWS119010','法律与社会','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(112,'LAW620060','马克思主义法学思想','法学硕士','2019-2020','法学硕士-19_法学理论','二',36,3,'必修',1,1,'史大晓,侯健','史大晓,侯健','史大晓','史大晓','非精品课程','法学理论','','',0,'2019-04-05 20:51:10'),(113,'LAW630007','比较刑法','法学硕士','2019-2020','法学硕士-19_刑法学','二',36,5,'选修',1,1,'杨晓畅','杨晓畅','杨晓畅','杨晓畅','非精品课程','刑法学','','',0,'2019-04-06 21:00:27'),(114,'LAWS110010.01','外国行政法','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(115,'LAW630009','西方法律思想史','法学硕士','2019-2020','法学硕士-19_法学理论','二',36,3,'选修',1,1,'赖骏楠,杨晓畅','赖骏楠,杨晓畅','赖骏楠','赖骏楠','非精品课程','法学理论','','',0,'2019-04-05 20:51:10'),(116,'LAWS110010.02','外国行政法','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(117,'JM630008','专利法','法律硕士','2019-2020','法律硕士-17_法律硕士（非法学）','一',36,7,'选修',1,1,'丁文杰','丁文杰','丁文杰','丁文杰','非精品课程','民商法学','','',0,'2019-04-05 20:51:10'),(118,'LAWS130060','非诉讼纠纷解决','本科','2019-2020','本科-16_法学专业教育','一',54,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','英文','JM620036',1,'2019-04-05 20:51:10'),(119,'JM620016','民法学','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班','一',72,8,'必修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','班天可,班天可','班天可,班天可','非精品课程','民商法学','','',0,'2019-04-05 20:51:10'),(120,'JM620017','行政法与行政诉讼法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学）','一',36,7,'必修',1,1,'刘志刚,朱淑娣','刘志刚,朱淑娣','刘志刚','刘志刚','非精品课程','宪法学与行政法学','','',0,'2019-04-05 20:51:10'),(121,'LAWS130002','民法I','本科','2019-2020','本科-19_法学专业教育','二',54,8,'必修',1,1,'葛江虬,施鸿鹏,丁文杰','葛江虬,施鸿鹏,丁文杰','葛江虬,葛江虬','葛江虬,葛江虬','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:10'),(122,'LAWS130005','行政诉讼法','本科','2019-2020','本科-18_法学专业教育','一',36,10,'必修',1,1,'朱淑娣,刘志刚','朱淑娣,刘志刚','朱淑娣,刘志刚','朱淑娣,刘志刚','非精品课程','诉讼法学','中文','',0,'2019-04-05 20:51:10'),(123,'LAWS119003.01','宪政文明史','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'王蔚','王蔚','王蔚','王蔚','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(124,'LAWS119003.02','宪政文明史','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'王蔚','王蔚','王蔚','王蔚','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(125,'LAWS110003.01','婚姻家庭法','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(126,'LAWS110003.02','婚姻家庭法','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(127,'JM630012','票据法','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学） 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',36,7,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','非精品课程','经济法学','','LAWS130033',0,'2019-04-05 20:51:10'),(128,'LAW620066','西方法理学研究','法学硕士','2019-2020','法学硕士-19_法学理论','一',54,4,'必修',1,1,'张光杰','张光杰','张光杰','张光杰','非精品课程','法学理论','','',0,'2019-04-05 20:51:10'),(129,'LAW630077','国际贸易法专题','法学硕士','2019-2020','法学硕士-19_国际法学','二',36,5,'选修',1,1,'何力','何力','何力','何力','非精品课程','国际法学','','',0,'2019-04-05 20:51:10'),(130,'LAW630076','国际贸易的知识产权法','法学硕士','2019-2020','法学硕士-19_国际法学','二',36,3,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','非精品课程','国际法学','','',0,'2019-04-05 20:51:10'),(131,'LAWS110016.02','交易法律制度','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(132,'LAWS110016.01','交易法律制度','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'姚军','姚军','姚军','姚军','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(133,'LAWS160003','刑法','本科','2019-2020','本科-18_跨校辅修教学','一',54,10,'必修',1,1,'杜宇','杜宇','杜宇','杜宇','非精品课程','刑法学','中文','',0,'2019-04-05 20:51:10'),(134,'LAWS119007.01','法律与科技文明','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(135,'LAWS119007.02','法律与科技文明','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(136,'927.003.1','国际经济法导论','本科','2019-2020','本科-18_第二专业教学','二',54,10,'必修',1,1,'何力','何力','何力','何力','非精品课程','国际法学','中文','',0,'2019-04-05 20:51:10'),(137,'LAWS130038','国际经济合同','本科','2019-2020','本科-17_法学专业教育','二',54,9,'选修',1,1,'龚柏华','龚柏华','龚柏华','龚柏华','非精品课程','国际法学','中文','JM630029',0,'2019-04-05 20:51:10'),(138,'LAWS110004.01','知识产权法','本科','2019-2020','本科-_通识教育','一',36,9,'选修',1,1,'王俊','王俊','王俊','王俊','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(139,'LAWS110004.02','知识产权法','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(140,'LAWS130034','证据学','本科','2019-2020','本科-17_法学专业教育','一',36,9,'选修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','非精品课程','诉讼法学','中文','JM630011',0,'2019-04-05 20:51:10'),(141,'LAWS130036','国际投资法','本科','2019-2020','本科-17_法学专业教育','二',54,9,'选修',1,1,'陆志安,孙南申','陆志安,孙南申','孙南申,陆志安','孙南申,陆志安','精品课程','国际法学','英文','JM630032',0,'2019-04-05 20:51:10'),(142,'LAWS130037','国际税法','本科','2019-2020','本科-17_法学专业教育','二',54,9,'选修',1,1,'陆志安','陆志安','陆志安','陆志安','非精品课程','国际法学','中文','JM630031',0,'2019-04-05 20:51:10'),(143,'LAWS130030','国际贸易法','本科','2019-2020','本科-17_法学专业教育','一',54,9,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','非精品课程','国际法学','中文','JM630006',0,'2019-04-05 20:51:10'),(144,'LAWS130031','侵权行为法','本科','2019-2020','本科-17_法学专业教育','一',36,9,'选修',1,1,'丁文杰,施鸿鹏','丁文杰,施鸿鹏','丁文杰,丁文杰','丁文杰,丁文杰','非精品课程','民商法学','中文','JM630034',0,'2019-04-05 20:51:10'),(145,'LAWS130032','证券法','本科','2019-2020','本科-17_法学专业教育','一',36,9,'选修',1,1,'张建伟,许凌艳','张建伟,许凌艳','张建伟,许凌艳','张建伟,许凌艳','非精品课程','民商法学','中文','',0,'2019-04-05 20:51:10'),(146,'LAWS130033','票据法','本科','2019-2020','本科-17_法学专业教育','一',36,9,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','非精品课程','民商法学','中文','JM630012',0,'2019-04-05 20:51:10'),(147,'LAW620031','中国刑法','法学硕士','2019-2020','法学硕士-19_刑法学','一',54,4,'必修',1,1,'杜宇,蒋云蔚','杜宇,蒋云蔚','蒋云蔚','蒋云蔚','非精品课程','LLM','','',0,'2019-04-05 20:51:10'),(148,'LAW620032','犯罪学','法学硕士','2019-2020','法学硕士-19_刑法学','一',54,4,'必修',1,1,'汪明亮','汪明亮','汪明亮','汪明亮','非精品课程','刑法学','','',0,'2019-04-05 20:51:10'),(149,'LAWS110022.01','环境与资源保护法律政策','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(150,'LAWS110022.02','环境与资源保护法律政策','本科','2019-2020','本科-_通识教育','二',36,9,'选修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','非精品课程','综合','中文','',0,'2019-04-05 20:51:10'),(151,'LAWS119001.02','法律与跨文化交往','本科','2019-2020','本科-_','二',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(152,'LAWS119001.01','法律与跨文化交往','本科','2019-2020','本科-_','一',36,0,'选修',0,0,'','',NULL,NULL,'非精品课程','综合','中文','',1,'2019-04-05 20:51:10'),(153,'LAW630101','经济犯罪','法学硕士','2019-2020','法学硕士-19_刑法学','二',36,3,'选修',1,1,'汪明亮,蒋云蔚','汪明亮,蒋云蔚','汪明亮','汪明亮','非精品课程','刑法学','','',0,'2019-04-05 20:51:10'),(154,'LAW630107','法治与文化','法律硕士','2019-2020','法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）','二',36,5,'选修',1,1,'赵立行','赵立行','赵立行','赵立行','非精品课程','综合','','',0,'2019-04-05 20:51:10'),(155,'LAW630106','比较法原理','法学硕士','2019-2020','法学硕士-19_法律史','二',36,4,'选修',1,1,'涂云新,陈立,赵立行','涂云新,陈立,赵立行','涂云新','涂云新','非精品课程','法律史','','',0,'2019-04-05 20:51:10');
/*!40000 ALTER TABLE `course_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-07 21:41:22
