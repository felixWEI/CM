-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: classmanagement
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `course_history_info`
--

DROP TABLE IF EXISTS `course_history_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_history_info` (
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
  `course_parallel` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=553 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_history_info`
--

LOCK TABLES `course_history_info` WRITE;
/*!40000 ALTER TABLE `course_history_info` DISABLE KEYS */;
INSERT INTO `course_history_info` VALUES (1,'HIST119003','文艺复兴史','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'赵立行','赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:06',''),(2,'LAWS130022','物权法','本科','2018-2019','本科-17_法学专业教育','二',54,9,'选修',1,1,'李世刚,蒋云蔚','李世刚,蒋云蔚','李世刚','李世刚','','','','',0,'2018-04-25 00:00:06',''),(3,'LAWS130021','毕业论文','本科','2018-2019','本科-15_法学专业教育','二',72,10,'必修',1,1,'教学院长','教学院长','教学院长','教学院长','','','','',0,'2018-04-25 00:00:06',''),(4,'LAWS130020','毕业实习','本科','2018-2019','本科-15_法学专业教育','二',72,10,'必修',1,1,'教学院长','教学院长','教学院长','教学院长','','','','',0,'2018-04-25 00:00:06',''),(5,'LAWS130027','婚姻家庭法','本科','2018-2019','本科-16_法学专业教育','一',54,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','','','','',0,'2018-04-25 00:00:06',''),(6,'LAWS130026','自然资源和环境保护法','本科','2018-2019','本科-17_法学专业教育','二',36,10,'必修',2,1,'陶蕾,张梓太','陶蕾,张梓太','陶蕾,张梓太','陶蕾,张梓太','','','','',0,'2018-04-25 00:00:06',''),(7,'LAWS130025','公司法','本科','2018-2019','本科-17_法学专业教育','二',36,9,'选修',1,1,'白国栋,李小宁,张建伟','白国栋,李小宁,张建伟','李小宁','李小宁','','','','',0,'2018-04-25 00:00:06',''),(8,'LAWS130024','金融法','本科','2018-2019','本科-17_法学专业教育','二',36,9,'选修',1,1,'待定老师2','','待定老师2','许凌艳','','','','',0,'2018-04-27 22:13:59',''),(9,'LAWS119004.01','法治理念与实践','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'张光杰','张光杰','张光杰','张光杰','','','','',0,'2018-04-25 00:00:06',''),(10,'LAWS130029','国际金融法','本科','2018-2019','本科-16_法学专业教育','二',54,9,'选修',1,1,'待定老师2','','待定老师2','待定老师2','','','','',0,'2018-04-27 22:14:14',''),(11,'LAWS130061.02','国际法（全英文）','本科','2018-2019','本科-17_法学专业教育','一',54,9,'必修',1,1,'陆志安,王伟,马忠法','陆志安,王伟','陆志安','陆志安','','','','',0,'2018-04-28 09:18:46',''),(12,'LAWS130061.01','国际法','本科','2018-2019','本科-17_法学专业教育','一',54,10,'必修',1,1,'龚柏华,陆志安,王伟,朱丹','龚柏华,陆志安,王伟,朱丹','王伟','朱丹','','','','',0,'2018-04-25 00:00:06',''),(13,'LAWS130002.01','民法I','本科','2018-2019','本科-18_法学专业教育','二',54,9,'必修',2,1,'班天可,刘士国','班天可,刘士国,李世刚','刘士国,班天可','刘士国,班天可','','','','',0,'2018-04-28 09:05:56',''),(14,'SOSC120015.02','宪法','本科','2018-2019','本科-18_基础教育','一',54,10,'必修',2,1,'潘伟杰,涂云新,王蔚','潘伟杰,涂云新,王蔚','潘伟杰,王蔚','潘伟杰,王蔚','','','','',0,'2018-04-25 00:00:06',''),(15,'LAWS119004.02','法治理念与实践','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'张光杰','张光杰','张光杰','张光杰','','','','',0,'2018-04-25 00:00:06',''),(16,'LAW620041','环境法原理','法学硕士','2018-2019','法学硕士-18_环境与资源保护法学','一',54,4,'必修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','','','','',0,'2018-04-25 00:00:06',''),(17,'LAW620043','国际环境法专题','法学硕士','2018-2019','法学硕士-18_环境与资源保护法学','二',36,5,'选修',3,1,'陆志安,李传轩,马忠法','陆志安,马忠法,李传轩','李传轩,陆志安,马忠法','李传轩,陆志安,马忠法','','','','',0,'2018-04-28 09:35:07',''),(18,'JM630014.02','法律诊所与模拟法庭训练','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','二',72,8,'必修',2,1,'实务导师1,实务导师2','实务导师1,实务导师2','实务导师1,实务导师2','实务导师1,实务导师2','','','','',0,'2018-04-25 00:00:06',''),(19,'927.011.1','刑法I','本科','2018-2019','本科-18_第二专业教学','二',72,10,'必修',1,1,'王越,袁国何','王越,袁国何','袁国何','袁国何','','','','',0,'2018-04-25 00:00:06',''),(20,'JM630014.01','法律诊所与模拟法庭训练','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','二',72,8,'必修',2,1,'章武生,季立刚','章武生,季立刚','章武生,季立刚','章武生,季立刚','','','','',0,'2018-04-25 00:00:06',''),(22,'LAW630022.02','银行法专题','法学硕士','2018-2019','法学硕士-18_经济法学 法学硕士-17_经济法学','二',36,5,'选修',1,1,'季立刚','季立刚','季立刚','季立刚','','','','',0,'2018-05-02 17:27:01',''),(23,'LAW630057','国际海关法专题','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'何力','何力','何力','何力','','','','',0,'2018-04-25 00:00:06',''),(24,'JM620017.01','行政法与行政诉讼法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',36,7,'必修',1,1,'刘志刚','刘志刚','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:06',''),(25,'JM620017.02','行政法与行政诉讼法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',36,7,'必修',1,1,'刘志刚','刘志刚','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:06',''),(26,'927.013.1','行政法','本科','2018-2019','本科-18_第二专业教学','二',54,10,'必修',1,1,'待定老师2','','待定老师2','待定老师2','','','','',0,'2018-04-27 22:05:41',''),(27,'LAW620077','市场规制法专题','法学硕士','2018-2019','法学硕士-18_经济法学','一',54,4,'必修',1,1,'胡鸿高,张建伟','待定老师','张建伟','张建伟','','','','',0,'2018-04-26 12:28:45',''),(28,'927.005.1','民法II','本科','2018-2019','本科-17_第二专业教学','一',72,8,'必修',1,1,'施鸿鹏','施鸿鹏','施鸿鹏','施鸿鹏','','','','',0,'2018-04-25 00:00:06',''),(29,'LAWS119010.01','法律与社会','本科','2018-2019','本科-_通识教育','二',36,9,'选修',2,1,'侯健,孟烨,潘伟杰','侯健,孟烨,潘伟杰','侯健,孟烨','侯健,孟烨','','','','',0,'2018-04-25 00:00:06',''),(30,'LAWS119010.04','法律与社会','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'孟烨,潘伟杰','孟烨,潘伟杰','潘伟杰,孟烨','潘伟杰','','','','',0,'2018-05-03 16:10:53',''),(31,'LAWS130008','民法II','本科','2018-2019','本科-17_法学专业教育','一',72,10,'必修',1,1,'施鸿鹏,班天可','施鸿鹏,班天可','班天可','班天可','','','','',0,'2018-04-25 00:00:06',''),(32,'LAWS130052','国际商法','本科','2018-2019','本科-16_法学专业教育','二',54,9,'选修',1,1,'高凌云','高凌云','高凌云','高凌云','','','','',0,'2018-04-25 00:00:06',''),(34,'927.004.1','国际私法','本科','2018-2019','本科-17_第二专业教学','二',54,10,'必修',1,1,'陈力','陈力','陈力','陈力','','','','',0,'2018-04-25 00:00:06',''),(35,'JM620022.01','知识产权法','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','二',36,7,'必修',1,1,'王俊','王俊','王俊','王俊','','','','',0,'2018-04-25 00:00:07',''),(36,'JM620022.02','知识产权法','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','二',36,7,'必修',1,1,'丁文杰,王俊','丁文杰,王俊','丁文杰','丁文杰','','','','',0,'2018-04-25 00:00:07',''),(37,'927.014.1','中国法制史','本科','2018-2019','本科-18_第二专业教学','一',54,10,'必修',1,1,'赖骏楠,孟烨','赖骏楠,孟烨','赖骏楠','赖骏楠','','','','',0,'2018-04-25 00:00:07',''),(38,'LAWS130031','侵权行为法','本科','2018-2019','本科-16_法学专业教育','一',36,9,'选修',1,1,'丁文杰,施鸿鹏','丁文杰,施鸿鹏','施鸿鹏','施鸿鹏','','','','',0,'2018-04-25 00:00:07',''),(39,'MAST612116.01','专业英语(写作)','法学硕士','2018-2019','法学硕士-17_国际法学','一',18,3,'必修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 00:00:07',''),(40,'LAWS110022','环境与资源保护法律政策','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','','','','',0,'2018-04-25 00:00:07',''),(41,'LAWS110025','日本战后法律事件的解读','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','','','','',0,'2018-04-25 00:00:07',''),(42,'LAW620059','规制与竞争法专题研究','法学硕士','2018-2019','法学硕士-17_经济法学','一',54,4,'必修',1,1,'张建伟,胡鸿高','张建伟,胡鸿高','胡鸿高','张建伟','','','','',0,'2018-04-25 00:00:07',''),(43,'LAWS115001','法科大学生的创新与创业','本科','2018-2019','本科-_通识教育','二',18,9,'选修',1,1,'熊浩','熊浩','熊浩','熊浩','','','','',0,'2018-04-25 00:00:07',''),(44,'LAW620053','中国当代社会法理学问题','法学硕士','2018-2019','法学硕士-18_法学理论','一',54,4,'必修',1,1,'孙笑侠','孙笑侠','孙笑侠','孙笑侠','','','','',0,'2018-04-25 00:00:07',''),(45,'JM620018.02','经济法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',54,7,'必修',1,1,'王俊,陈立','王俊,陈立','陈立','陈立','','','','',0,'2018-04-25 00:00:07',''),(46,'LAW620078','民事诉讼法专题','法学硕士','2018-2019','法学硕士-18_诉讼法学','一',54,4,'必修',1,1,'段厚省','段厚省','段厚省','章武生','','','','',0,'2018-04-25 00:00:07',''),(47,'LAW630034','司法制度专题','法学硕士','2018-2019','法学硕士-18_诉讼法学','二',36,5,'选修',1,1,'章武生,徐美君','章武生,徐美君','徐美君','徐美君','','','','',0,'2018-04-25 00:00:07',''),(48,'JM620030','经济法专题','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'必修',1,1,'王俊','王俊','王俊','王俊','','','','',0,'2018-04-25 00:00:07',''),(49,'JM620031','法律职业规范与伦理','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',54,6,'必修',1,1,'杨晓畅','杨晓畅','杨晓畅','杨晓畅','','','','',0,'2018-04-25 00:00:07',''),(50,'LAWS130004.01','中国法制史','本科','2018-2019','本科-17_法学专业教育','一',54,10,'必修',2,1,'赖骏楠,郭建,孟烨','赖骏楠,郭建,孟烨','郭建,孟烨','郭建,孟烨','','','','',0,'2018-04-25 00:00:07',''),(51,'LAWS130045','西方法律思想史','本科','2018-2019','本科-15_法学专业教育','一',36,9,'选修',1,1,'杨晓畅','杨晓畅','杨晓畅','杨晓畅','','','','',0,'2018-04-25 00:00:07',''),(52,'LAWS130044','中国法律思想史','本科','2018-2019','本科-15_法学专业教育','一',36,9,'选修',1,1,'郭建,王志强,赖骏楠','郭建,王志强,赖骏楠','王志强','王志强','','','','',0,'2018-04-25 00:00:07',''),(53,'LAWS130041','国际商事仲裁法','本科','2018-2019','本科-16_法学专业教育','二',36,9,'选修',1,1,'陈力','陈力','陈力','陈力','','','','',0,'2018-04-25 00:00:07',''),(55,'LAWS130043','刑事政策','本科','2018-2019','本科-17_法学专业教育','二',36,9,'选修',1,1,'汪明亮','汪明亮','汪明亮','汪明亮','','','','',0,'2018-04-25 00:00:07',''),(56,'LAWS119007.01','法律与科技文明','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','','','','',0,'2018-04-25 00:00:07',''),(57,'LAW620083','国际私法研究','法学硕士','2018-2019','法学硕士-18_国际法学','一',54,4,'必修',1,1,'陈力,孙南申','陈力,孙南申','陈力','陈力','','','','',0,'2018-04-25 00:00:07',''),(58,'LAW620073','行政法学专题','法学硕士','2018-2019','法学硕士-18_宪法学与行政法学','一',54,4,'必修',1,1,'刘志刚','刘志刚','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:07',''),(59,'LAW620080','环境热点问题研究','法学硕士','2018-2019','法学硕士-18_环境与资源保护法学','一',54,4,'必修',1,1,'张梓太','张梓太','张梓太','张梓太','','','','',0,'2018-04-25 00:00:07',''),(60,'LAW630114','家事法专题','法学硕士','2018-2019','法学硕士-18_民商法学','二',36,5,'选修',1,1,'孙晓屏,施鸿鹏','孙晓屏,施鸿鹏','孙晓屏','孙晓屏','','','','',0,'2018-04-25 00:00:07',''),(61,'JM620012.02','国际经济法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',36,7,'必修',1,1,'何力,马忠法','何力,马忠法','何力','何力','','','','',0,'2018-04-25 00:00:07',''),(62,'JM620012.01','国际经济法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',36,7,'必修',1,1,'何力,马忠法','何力,马忠法','马忠法','马忠法','','','','',0,'2018-04-25 00:00:07',''),(63,'LAWS130062.01','刑法I','本科','2018-2019','本科-18_法学专业教育','二',54,10,'必修',2,1,'杜宇,袁国何,王越','杜宇,袁国何,王越','王越,杜宇','王越,杜宇','','','','',0,'2018-04-25 00:00:07',''),(64,'JM620020.02','商法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',54,7,'必修',1,1,'李小宁,季立刚,胡鸿高','李小宁,季立刚,胡鸿高','胡鸿高','胡鸿高','','','','',0,'2018-04-25 00:00:07',''),(65,'LAWS110016','交易法律制度','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'姚军','姚军','姚军','姚军','','','','',0,'2018-04-25 00:00:07',''),(66,'JM620020.01','商法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',54,7,'必修',1,1,'李小宁,季立刚,胡鸿高','李小宁,季立刚,胡鸿高','季立刚','季立刚','','','','',0,'2018-04-25 00:00:07',''),(68,'LAW620055.01','法律方法论专题','法学硕士','2018-2019','法学硕士-18_法学理论 法学硕士-17_法学理论','二',36,5,'选修',1,1,'孙笑侠','孙笑侠','孙笑侠','孙笑侠','','','','',0,'2018-04-25 15:44:42',''),(70,'LAW620064','中国环境法','法学硕士','2018-2019','法学硕士-17_环境与资源保护法学','一',54,4,'必修',1,1,'张梓太','张梓太','张梓太','张梓太','','','','',0,'2018-04-25 00:00:07',''),(71,'LAWS160004','债法(合同法)','本科','2018-2019','本科-17_跨校辅修教学','二',54,10,'必修',1,1,'班天可','班天可','班天可','班天可','','','','',0,'2018-04-25 00:00:07',''),(72,'LAWS160005','商法','本科','2018-2019','本科-16_跨校辅修教学','一',54,10,'必修',1,1,'待定老师','待定老师','待定老师','白江','','','','',0,'2018-04-25 00:00:07',''),(73,'LAWS160006','民事诉讼法','本科','2018-2019','本科-17_跨校辅修教学','二',54,10,'必修',1,1,'杨严炎','杨严炎','杨严炎','杨严炎','','','','',0,'2018-04-25 00:00:07',''),(74,'LAW630043','环境科学','法学硕士','2018-2019','法学硕士-17_环境与资源保护法学','一',54,3,'选修',2,1,'张梓太,李传轩','张梓太,李传轩','李传轩,张梓太','李传轩,张梓太','','','','',0,'2018-04-25 00:00:07',''),(75,'LAWS160001','宪法学','本科','2018-2019','本科-17_跨校辅修教学','一',54,10,'必修',1,1,'涂云新','涂云新','涂云新','涂云新','','','','',0,'2018-04-25 00:00:07',''),(76,'LAWS160002','民法总论','本科','2018-2019','本科-17_跨校辅修教学','一',54,10,'必修',1,1,'班天可','班天可','班天可','班天可','','','','',0,'2018-04-25 00:00:07',''),(77,'LAWS160003','刑法','本科','2018-2019','本科-17_跨校辅修教学','一',54,10,'必修',1,1,'杜宇','杜宇','杜宇','杜宇','','','','',0,'2018-04-25 00:00:07',''),(78,'LAWS110017.01','法治社会的公民权利','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'姚军','姚军','姚军','姚军','','','','',0,'2018-04-25 00:00:07',''),(79,'LAWS110017.02','法治社会的公民权利','本科','2018-2019','本科-_通识教育','一',36,8,'选修',1,1,'姚军','姚军','姚军','姚军','','','','',0,'2018-04-25 00:00:07',''),(80,'SOSC120015.01','宪法','本科','2018-2019','本科-_基础教育','二',54,10,'必修',1,1,'潘伟杰,涂云新,王蔚','潘伟杰,涂云新,王蔚','潘伟杰','王蔚','','','','',0,'2018-04-25 00:00:07',''),(81,'LAWS119002.01','人权与法','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'侯健','侯健','侯健','侯健','','','','',0,'2018-04-25 00:00:07',''),(82,'MAST612116.02','专业英语','法学硕士','2018-2019','法学硕士-17_国际法学 法学硕士-17_法律史 法学硕士-17_宪法学与行政法学 法学硕士-17_刑法学 法学硕士-17_民商法学 法学硕士-17_诉讼法学 法学硕士-17_经济法学 法学硕士-17_环境与资源保护法学','二',18,5,'必修',1,1,'陈力','陈力,涂云新','陈力','葛江虬','','','','',0,'2018-04-28 14:14:12',''),(83,'927.008.1','商法','本科','2018-2019','本科-17_第二专业教学','二',54,10,'必修',1,1,'许凌艳','许凌艳','许凌艳','许凌艳','','','','',0,'2018-04-25 00:00:07',''),(84,'927.010.1','刑法II','本科','2018-2019','本科-17_第二专业教学','一',36,10,'必修',1,1,'王越','王越','王越','王越','','','','',0,'2018-04-25 00:00:07',''),(85,'LAWS130049.01','外国法律制度','本科','2018-2019','本科-17_法学专业教育','二',54,9,'必修',2,1,'赵立行,赖骏楠','赵立行,赖骏楠','赵立行,赖骏楠','赵立行,赖骏楠','','','','',0,'2018-04-25 00:00:07',''),(86,'LAW630038','国际投资法研究','法学硕士','2018-2019','法学硕士-18_国际法学','二',36,5,'选修',1,1,'孙南申','孙南申','孙南申','孙南申','','','','',0,'2018-04-25 00:00:07',''),(87,'JM620028','模拟法庭训练','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'必修',1,1,'涂云新','涂云新','涂云新','涂云新','','','','',0,'2018-04-25 00:00:07',''),(88,'JM620024','法理学专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学） 法律硕士-18_法律硕士（法学）国际班','一',36,7,'必修',1,1,'张光杰','张光杰','张光杰','张光杰','','','','',0,'2018-04-25 00:00:07',''),(89,'927.006.1','民法I','本科','2018-2019','本科-18_第二专业教学','二',54,10,'必修',1,1,'施鸿鹏','施鸿鹏','施鸿鹏','施鸿鹏','','','','',0,'2018-04-25 00:00:07',''),(90,'LAW630035','律师制度专题','法学硕士','2018-2019','法学硕士-17_诉讼法学','二',36,3,'选修',1,1,'待定老师2','','待定老师2','待定老师2','','','','',0,'2018-04-27 22:12:49',''),(91,'927.012.1','刑事诉讼法','本科','2018-2019','本科-17_第二专业教学','一',54,10,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:07',''),(92,'JM620023','环境资源法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','二',36,8,'必修',1,1,'陶蕾,李传轩,张梓太','陶蕾,李传轩,张梓太','张梓太','张梓太','','','','',0,'2018-04-25 00:00:07',''),(93,'JM620022','知识产权法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','二',36,8,'必修',1,1,'王俊','王俊','王俊','王俊','','','','',0,'2018-04-25 00:00:07',''),(94,'LAW620074','民法专题研究','法学硕士','2018-2019','法学硕士-18_民商法学','一',54,4,'必修',1,1,'刘士国,孙晓屏,李世刚,蒋云蔚','刘士国,孙晓屏,李世刚,蒋云蔚','刘士国','刘士国','','','','',0,'2018-04-25 00:00:07',''),(95,'LAW620076','金融法专题','法学硕士','2018-2019','法学硕士-18_经济法学','一',54,4,'必修',1,1,'季立刚,许凌艳','季立刚,许凌艳','许凌艳','季立刚','','','','',0,'2018-04-25 00:00:07',''),(97,'LAWS130037','国际税法','本科','2018-2019','本科-16_法学专业教育','二',54,9,'选修',1,1,'陆志安','陆志安','陆志安','陆志安','','','','',0,'2018-04-25 00:00:07',''),(98,'LAWS119002.02','人权与法','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'侯健','侯健','侯健','侯健','','','','',0,'2018-04-25 00:00:07',''),(99,'927.024.1','法理学导论','本科','2018-2019','本科-18_第二专业教学','一',54,10,'必修',1,1,'史大晓','史大晓','史大晓','史大晓','','','','',0,'2018-04-25 00:00:07',''),(100,'927.007.1','民事诉讼法','本科','2018-2019','本科-17_第二专业教学','一',54,8,'必修',1,1,'杨严炎','杨严炎','杨严炎','杨严炎','','','','',0,'2018-04-25 00:00:07',''),(101,'LAWS110003','婚姻家庭法','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','','','','',0,'2018-04-25 00:00:07',''),(102,'LAW630115','债法专题','法学硕士','2018-2019','法学硕士-18_民商法学','二',36,5,'选修',1,1,'孙晓屏,施鸿鹏','孙晓屏,施鸿鹏','施鸿鹏','施鸿鹏','','','','',0,'2018-04-25 00:00:07',''),(103,'LAWS110014','知识经济与知识产权管理','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','','','','',0,'2018-04-25 00:00:07',''),(104,'LAW620030','宪法学专题','法学硕士','2018-2019','法学硕士-18_宪法学与行政法学','一',54,4,'必修',1,1,'待定老师','待定老师','待定老师','董茂云','','','','',0,'2018-04-25 00:00:07',''),(105,'LAW630112','物权法专题','法学硕士','2018-2019','法学硕士-18_民商法学','二',36,5,'选修',1,1,'李世刚,蒋云蔚','李世刚,蒋云蔚','蒋云蔚','蒋云蔚','','','','',0,'2018-04-25 00:00:07',''),(107,'LAW620075','商法专题研究','法学硕士','2018-2019','法学硕士-18_民商法学','一',54,4,'必修',1,1,'季立刚,胡鸿高','季立刚,胡鸿高','季立刚','胡鸿高','','','','',0,'2018-04-25 00:00:07',''),(108,'LAWS110004','知识产权法','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'王俊','王俊','王俊','王俊','','','','',0,'2018-04-25 00:00:07',''),(109,'LAWS160010','刑事诉讼法','本科','2018-2019','本科-17_跨校辅修教学','二',54,10,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:07',''),(110,'LAW630011.01','人权研究','法学硕士','2018-2019','法学硕士-18_宪法学与行政法学 法学硕士-17_宪法学与行政法学','二',54,5,'选修',1,1,'潘伟杰,涂云新','潘伟杰,涂云新','潘伟杰','潘伟杰','','','','',0,'2018-05-02 17:23:33',''),(111,'LAW620081','国际公法研究','法学硕士','2018-2019','法学硕士-18_国际法学','一',54,4,'必修',1,1,'龚柏华,张乃根','龚柏华,张乃根','龚柏华','张乃根','','','','',0,'2018-04-25 20:40:23',''),(112,'JM620016.02','民法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','一',72,8,'必修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','施鸿鹏','施鸿鹏','','','','',0,'2018-04-28 14:36:34',''),(113,'JM620016.01','民法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）国际班','一',72,8,'必修',1,1,'班天可,施鸿鹏','班天可,施鸿鹏','班天可','班天可','','','','',0,'2018-04-28 14:36:00',''),(114,'LAWS130033','票据法','本科','2018-2019','本科-16_法学专业教育','一',36,9,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','','','','',0,'2018-04-25 00:00:07',''),(115,'LAWS130009.01','民事诉讼法','本科','2018-2019','本科-17_法学专业教育','二',54,9,'必修',3,1,'杨严炎,章武生,段厚省','杨严炎,章武生,段厚省','杨严炎,段厚省,章武生','杨严炎,段厚省,章武生','','','','',0,'2018-04-25 00:00:07',''),(116,'LAWS130023','税法','本科','2018-2019','本科-17_法学专业教育','二',36,9,'选修',1,1,'陈立','陈立','陈立','陈立','','','','',0,'2018-04-25 00:00:07',''),(117,'LAWS130032','证券法','本科','2018-2019','本科-16_法学专业教育','一',36,9,'选修',1,1,'张建伟,许凌艳','张建伟,许凌艳','张建伟','张建伟','','','','',0,'2018-04-25 00:00:07',''),(118,'JM620004.01','刑法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）国际班','一',72,8,'必修',1,1,'袁国何,王越','袁国何,王越','袁国何','袁国何','','','','',0,'2018-04-25 00:00:07',''),(119,'JM620004.02','刑法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','一',72,8,'必修',1,1,'袁国何,王越','袁国何,王越','王越','王越','','','','',0,'2018-04-25 00:00:07',''),(120,'JM620041','法律与商业','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'郭建,陈立','郭建,陈立','郭建','郭建','','','','',0,'2018-04-25 00:00:07',''),(121,'JM620045','法律伦理与法律方法','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'待定老师','待定老师','待定老师','实务导师1','','','','',0,'2018-04-25 00:00:07',''),(122,'JM620035','法律英语（一）','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）','二',36,8,'必修',1,1,'王俊,熊浩','王俊,熊浩','熊浩','熊浩','','','','',0,'2018-04-25 00:00:07',''),(123,'JM620040','法律与人文','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','一',36,8,'必修',1,1,'郭建,赵立行','郭建,赵立行','郭建','郭建','','','','',0,'2018-04-25 00:00:07',''),(124,'JM620056','国际法*','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',36,6,'必修',1,1,'陆志安,马忠法,朱丹,陈立,张乃根','陆志安,马忠法,朱丹,陈立,张乃根','张乃根','朱丹','','','','',0,'2018-04-25 00:00:07',''),(125,'JM620034','法律检索与学术写作*','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',18,6,'必修',1,1,'待定老师','待定老师','待定老师','刘丽君','','','','',0,'2018-04-25 00:00:07',''),(126,'JM620053','比较法*','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）国际班 法律硕士-18_法律硕士（法学）国际班','二',36,6,'必修',1,1,'涂云新,陈立,赵立行','涂云新,陈立,赵立行','涂云新','涂云新','','','','',0,'2018-04-25 00:00:07',''),(127,'JM620052','刑法专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'袁国何,王越','袁国何,王越','袁国何','袁国何','','','','',0,'2018-04-25 00:00:07',''),(128,'JM620038','民法专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'李世刚,孙晓屏,蒋云蔚','李世刚,孙晓屏,刘士国,蒋云蔚','蒋云蔚','蒋云蔚','','','','',0,'2018-04-25 21:56:13',''),(129,'LAW630027','欧盟法专题','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'陆志安','陆志安','陆志安','陆志安','','','','',0,'2018-04-25 00:00:07',''),(131,'LAW630020.02','证券法研究','法学硕士','2018-2019','法学硕士-17_经济法学 法学硕士-18_经济法学','二',36,5,'选修',1,1,'许凌艳,张建伟','许凌艳,张建伟','张建伟','许凌艳','','','','',0,'2018-05-02 16:11:29',''),(133,'LAW630096','国际可持续发展法','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'陆志安,马忠法','陆志安,马忠法','陆志安','陆志安','','','','',0,'2018-04-25 00:00:07',''),(134,'LAW620003','宪法学研究','法学硕士','2018-2019','法学硕士-17_宪法学与行政法学','一',54,4,'必修',1,1,'刘志刚,潘伟杰,涂云新','刘志刚,潘伟杰,涂云新','潘伟杰','潘伟杰','','','','',0,'2018-04-25 00:00:07',''),(135,'LAW620002','比较法研究','法学硕士','2018-2019','法学硕士-17_法律史 法学硕士-17_诉讼法学','一',54,4,'必修',1,1,'赵立行','赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:07',''),(136,'SOSC120003.01','法理学导论','本科','2018-2019','本科-_基础教育','二',54,10,'必修',3,1,'侯健,史大晓,杨晓畅,孙笑侠','侯健,史大晓,杨晓畅,孙笑侠','史大晓,孙笑侠,杨晓畅','史大晓,孙笑侠,杨晓畅','','','','',0,'2018-04-25 00:00:07',''),(137,'LAW620007','刑事政策研究','法学硕士','2018-2019','法学硕士-18_刑法学','二',36,5,'选修',1,1,'汪明亮','汪明亮','汪明亮','汪明亮','','','','',0,'2018-04-25 00:00:07',''),(138,'927.009.1','宪法','本科','2018-2019','本科-18_第二专业教学','一',54,10,'必修',1,1,'涂云新','涂云新','涂云新','涂云新','','','','',0,'2018-04-25 00:00:07',''),(139,'LAWS130042','海商法','本科','2018-2019','本科-16_法学专业教育','二',36,9,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 00:00:07',''),(140,'JM620010.01','中国法制史','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','一',36,7,'必修',1,1,'郭建,孟烨,赖骏楠','郭建,孟烨,赖骏楠','孟烨','孟烨','','','','',0,'2018-04-25 00:00:07',''),(141,'JM620058','诉讼法专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:07',''),(142,'JM620055','国际法专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'马忠法,王伟,朱丹,张乃根','马忠法,王伟,朱丹,张乃根','朱丹','张乃根','','','','',0,'2018-04-25 20:43:29',''),(143,'JM620010.02','中国法制史','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','一',36,7,'必修',1,1,'郭建,孟烨,赖骏楠','郭建,孟烨,赖骏楠','赖骏楠','赖骏楠','','','','',0,'2018-04-25 00:00:07',''),(144,'JM620006.02','刑事诉讼法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'马贵翔,徐美君','马贵翔,徐美君','徐美君','徐美君','','','','',0,'2018-04-28 14:38:41',''),(145,'JM620006.01','刑事诉讼法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'马贵翔,徐美君','马贵翔,徐美君','徐美君','徐美君','','','','',0,'2018-04-28 14:38:01',''),(146,'JM620051','宪法与行政法专题','法律硕士','2018-2019','法律硕士-18_法律硕士（法学）','一',36,6,'必修',1,1,'刘志刚,涂云新','刘志刚,涂云新','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:07',''),(147,'LAW630038.01','国际投资法研究','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'选修',1,1,'孙南申','孙南申','孙南申','孙南申','','','','',0,'2018-04-25 00:00:07',''),(148,'LAW630014','经济行政法','法学硕士','2018-2019','法学硕士-17_宪法学与行政法学','二',54,3,'选修',1,1,'朱淑娣','朱淑娣','朱淑娣','朱淑娣','','','','',0,'2018-04-25 00:00:07',''),(149,'LAW630013','外国行政法','法学硕士','2018-2019','法学硕士-17_宪法学与行政法学','二',54,3,'选修',1,1,'朱淑娣','朱淑娣','朱淑娣','朱淑娣','','','','',0,'2018-04-25 00:00:07',''),(150,'LAWS130018','法理学','本科','2018-2019','本科-15_法学专业教育','一',36,10,'必修',1,1,'孙笑侠','孙笑侠','孙笑侠','孙笑侠','','','','',0,'2018-04-25 00:00:07',''),(151,'LAWS130019','法律实务','本科','2018-2019','本科-15_法学专业教育','一',54,10,'必修',1,1,'章武生,待定老师2','章武生','章武生','章武生','','','','',0,'2018-04-28 12:52:44',''),(152,'LAWS130015.01','知识产权法','本科','2018-2019','本科-16_法学专业教育','二',54,9,'必修',2,1,'丁文杰,王俊','丁文杰,王俊','王俊,丁文杰','王俊,丁文杰','','','','',0,'2018-04-25 00:00:07',''),(153,'927.002.1','国际法','本科','2018-2019','本科-18_第二专业教学','二',54,10,'必修',1,1,'朱丹','朱丹','朱丹','朱丹','','','','',0,'2018-04-25 00:00:07',''),(154,'LAWS130012','商法','本科','2018-2019','本科-16_法学专业教育','一',54,10,'必修',1,1,'李小宁','李小宁','李小宁','李小宁','','','','',0,'2018-04-25 00:00:07',''),(155,'LAWS130013','专业英语I(法律)','本科','2018-2019','本科-16_法学专业教育','一',36,10,'必修',1,1,'高凌云','高凌云','高凌云','高凌云','','','','',0,'2018-04-25 00:00:07',''),(156,'JM620057.02','国际法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','二',54,7,'必修',1,1,'何力,陆志安,王伟','何力,陆志安,王伟','王伟','王伟','','','','',0,'2018-04-25 22:22:38',''),(157,'LAW630018','侵权法研究','法学硕士','2018-2019','法学硕士-17_民商法学','一',54,3,'选修',1,1,'刘士国,班天可,蒋云蔚','班天可,蒋云蔚,刘士国','蒋云蔚','蒋云蔚','','','','',0,'2018-04-25 21:57:18',''),(158,'LAWS130016','专业英语II(法律)','本科','2018-2019','本科-16_法学专业教育','二',54,10,'必修',1,1,'高凌云','高凌云','高凌云','高凌云','','','','',0,'2018-04-25 00:00:07',''),(159,'JM620001.02','法理学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','一',54,7,'必修',1,1,'孙笑侠','孙笑侠','孙笑侠','孙笑侠','','','','',0,'2018-04-25 00:00:07',''),(160,'JM620001.01','法理学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','一',54,7,'必修',1,1,'侯健,孙笑侠','侯健,孙笑侠','侯健','侯健','','','','',0,'2018-04-25 00:00:07',''),(161,'LAW630107','法治与文化','法学硕士','2018-2019','法学硕士-18_法律史','二',36,5,'选修',1,1,'赵立行','赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:07',''),(162,'LAW630088','比较司法制度','法学硕士','2018-2019','法学硕士-17_法律史','二',36,3,'选修',1,1,'王志强,赖骏楠','王志强,赖骏楠','王志强','王志强','','','','',0,'2018-04-25 00:00:07',''),(163,'LAWS130007','刑事诉讼法','本科','2018-2019','本科-17_法学专业教育','二',54,10,'必修',1,1,'待定老师2','','待定老师2','徐美君','','','','',0,'2018-04-27 22:13:27',''),(164,'SOSC120016.02','经济法','本科','2018-2019','本科-17_基础教育','二',54,10,'必修',2,1,'施鸿鹏,李传轩,葛江虬','施鸿鹏,李传轩,葛江虬','李传轩,葛江虬','李传轩,葛江虬','','','','',0,'2018-04-25 00:00:07',''),(165,'JM630015.01','法律谈判课','法律硕士','2018-2019','法律硕士-16_法律硕士（非法学）1班','一',36,7,'必修',1,1,'熊浩','熊浩','熊浩','熊浩','','','','',0,'2018-04-25 00:00:07',''),(166,'JM630015.02','法律谈判课','法律硕士','2018-2019','法律硕士-16_法律硕士（非法学）2班','一',36,7,'必修',1,1,'熊浩','熊浩','熊浩','熊浩','','','','',0,'2018-04-25 00:00:07',''),(167,'SOSC120016.01','经济法','本科','2018-2019','本科-17_基础教育','一',54,10,'必修',1,1,'施鸿鹏,陈立','施鸿鹏,陈立','陈立','陈立','','','','',0,'2018-04-25 00:00:07',''),(168,'LAW630087','中世纪法专题','法学硕士','2018-2019','法学硕士-17_法律史','二',36,3,'选修',1,1,'赵立行','赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:07',''),(170,'LAW620010','立法学研究','法学硕士','2018-2019','法学硕士-18_宪法学与行政法学','二',36,5,'选修',1,1,'刘志刚,涂云新','刘志刚,涂云新','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:07',''),(171,'LAW620014','中国法制史专题','法学硕士','2018-2019','法学硕士-18_法律史','一',54,4,'必修',1,1,'郭建,赖骏楠','郭建','郭建','郭建','','','','',0,'2018-04-26 14:05:23',''),(172,'LAW630031.01','证据法','法学硕士','2018-2019','法学硕士-17_刑法学 法学硕士-17_诉讼法学 法学硕士-18_诉讼法学','二',36,5,'选修',1,1,'段厚省,马贵翔','段厚省,马贵翔','段厚省','段厚省','','','','',0,'2018-05-03 15:49:19',''),(174,'LAW620082','国际经济法研究','法学硕士','2018-2019','法学硕士-18_国际法学','一',54,4,'必修',1,1,'龚柏华,何力,马忠法','龚柏华,何力,马忠法','龚柏华','龚柏华','','','','',0,'2018-04-25 22:21:31',''),(175,'LAW630000','行政诉讼法学','法学硕士','2018-2019','法学硕士-17_宪法学与行政法学 法学硕士-17_诉讼法学','一',36,4,'选修',1,1,'待定老师2','','待定老师2','朱淑娣','','','','',0,'2018-04-27 22:06:33',''),(176,'JM630007','合同法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','一',36,7,'选修',1,1,'葛江虬,孙晓屏,蒋云蔚','葛江虬,孙晓屏,蒋云蔚','葛江虬','葛江虬','','','','',0,'2018-04-25 00:00:07',''),(177,'LAW630002','法学名著精读','法学硕士','2018-2019','法学硕士-18_法学理论','二',36,5,'选修',1,1,'王伟,赵立行','王伟,赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:07',''),(178,'LAW620060','马克思主义法学思想','法学硕士','2018-2019','法学硕士-17_法学理论','一',36,3,'必修',1,1,'史大晓,侯健','','史大晓','史大晓','','','','',0,'2018-04-26 14:09:54',''),(179,'LAWS130050.01','刑法II','本科','2018-2019','本科-17_法学专业教育','一',54,10,'必修',2,1,'袁国何,王越','袁国何,王越','袁国何,王越','袁国何,王越','','','','',0,'2018-04-25 00:00:07',''),(180,'LAW630007','比较刑法','法学硕士','2018-2019','法学硕士-18_刑法学','二',36,5,'选修',1,1,'待定老师2','','待定老师2','王越','','','','',0,'2018-04-27 22:09:51',''),(181,'LAW630009','西方法律思想史','法学硕士','2018-2019','法学硕士-17_法律史 法学硕士-17_法学理论','二',36,3,'选修',1,1,'赖骏楠,杨晓畅','赖骏楠,杨晓畅','杨晓畅','杨晓畅','','','','',0,'2018-04-25 15:13:19',''),(182,'LAWS160008','国际法','本科','2018-2019','本科-16_跨校辅修教学','二',54,10,'必修',1,1,'马忠法','马忠法','马忠法','马忠法','','','','',0,'2018-04-25 00:00:07',''),(183,'JM630008','专利法','法律硕士','2018-2019','法律硕士-16_法律硕士（非法学）1班 法律硕士-16_法律硕士（非法学）2班','一',36,7,'选修',1,1,'丁文杰','丁文杰','丁文杰','丁文杰','','','','',0,'2018-04-25 00:00:07',''),(184,'JM630009','物权法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','一',36,7,'选修',1,1,'李世刚,蒋云蔚','李世刚,蒋云蔚','李世刚','李世刚','','','','',0,'2018-04-25 00:00:07',''),(185,'JM630013.02','法律文书课','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',54,7,'必修',1,1,'姚军','姚军','姚军','姚军','','','','',0,'2018-04-25 00:00:07',''),(186,'JM630013.01','法律文书课','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',54,7,'必修',1,1,'姚军','姚军','姚军','姚军','','','','',0,'2018-04-25 00:00:07',''),(187,'JM620017','行政法与行政诉讼法','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'必修',1,1,'刘志刚,朱淑娣','刘志刚,朱淑娣','朱淑娣','朱淑娣','','','','',0,'2018-04-25 00:00:07',''),(188,'JM620023.02','环境资源法','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','二',36,7,'必修',1,1,'陶蕾,李传轩','陶蕾,李传轩','李传轩','李传轩','','','','',0,'2018-04-25 00:00:07',''),(189,'JM620023.01','环境资源法','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','二',36,7,'必修',1,1,'陶蕾,李传轩','陶蕾,李传轩','李传轩','李传轩','','','','',0,'2018-04-25 00:00:07',''),(190,'LAWS110013','合同法的理论与实践','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'孙晓屏','孙晓屏','孙晓屏','孙晓屏','','','','',0,'2018-04-25 00:00:07',''),(191,'LAWS130005','行政诉讼法','本科','2018-2019','本科-17_法学专业教育','一',36,10,'必修',1,1,'朱淑娣,刘志刚','朱淑娣,刘志刚','朱淑娣','朱淑娣','','','','',0,'2018-04-25 00:00:07',''),(192,'LAWS119003.01','宪政文明史','本科','2018-2019','本科-_通识教育','二',36,9,'选修',1,1,'王蔚','王蔚','王蔚','王蔚','','','','',0,'2018-04-25 00:00:07',''),(193,'LAWS119003.02','宪政文明史','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'王蔚','王蔚','王蔚','王蔚','','','','',0,'2018-04-25 00:00:07',''),(194,'LAWS160007','知识产权法','本科','2018-2019','本科-16_跨校辅修教学','一',54,10,'必修',1,1,'王俊','王俊','王俊','王俊','','','','',0,'2018-04-25 00:00:07',''),(195,'JM620005.03','民事诉讼法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',36,7,'必修',1,1,'杨严炎,章武生,段厚省','杨严炎,章武生,段厚省','杨严炎','杨严炎','','','','',0,'2018-04-27 22:22:13',''),(196,'JM620005.02','民事诉讼法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'杨严炎,章武生,段厚省','杨严炎,章武生,段厚省','章武生','章武生','','','','',0,'2018-04-27 22:21:19',''),(197,'JM620005.01','民事诉讼法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班 法律硕士-18_法律硕士（非法学）国际班','二',36,8,'必修',1,1,'章武生,段厚省','章武生,段厚省','段厚省','段厚省','','','','',0,'2018-04-27 22:20:52',''),(198,'JM630006.01','国际贸易法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','二',36,7,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 00:00:07',''),(199,'JM630006.02','国际贸易法','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 00:00:07',''),(200,'LAW620027','国际金融法专题','法学硕士','2018-2019','法学硕士-18_国际法学','二',36,5,'选修',1,1,'龚柏华,马忠法','龚柏华,马忠法','龚柏华','龚柏华','','','','',0,'2018-04-26 13:59:10',''),(201,'LAW620024','知识产权法研究','法学硕士','2018-2019','法学硕士-17_民商法学','二',54,4,'必修',1,1,'马忠法,王俊,丁文杰','丁文杰,马忠法','丁文杰','丁文杰','','','','',0,'2018-04-26 14:06:43',''),(202,'JM630011','证据法学','法律硕士','2018-2019','法律硕士-16_法律硕士（非法学）1班 法律硕士-16_法律硕士（非法学）2班','一',36,7,'选修',1,1,'段厚省','段厚省','段厚省','段厚省','','','','',0,'2018-04-25 14:14:55',''),(203,'JM630010','金融法','法律硕士','2018-2019','法律硕士-16_法律硕士（非法学）1班 法律硕士-16_法律硕士（非法学）2班','一',36,7,'选修',1,1,'待定老师2','','待定老师2','许凌艳','','','','',0,'2018-04-27 22:05:59',''),(204,'JM630012','票据法','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班 法律硕士-17_法律硕士（非法学）2班','一',36,7,'选修',1,1,'白国栋','白国栋','白国栋','白国栋','','','','',0,'2018-04-25 00:00:07',''),(205,'LAW620066','西方法理学研究','法学硕士','2018-2019','法学硕士-18_法学理论','一',54,4,'必修',1,1,'张光杰','张光杰','张光杰','张光杰','','','','',0,'2018-04-25 00:00:07',''),(206,'LAW630077','国际贸易法专题','法学硕士','2018-2019','法学硕士-18_国际法学','二',36,5,'选修',1,1,'何力','何力','何力','何力','','','','',0,'2018-04-25 22:18:42',''),(207,'LAW630073','票据法与保险法研究','法学硕士','2018-2019','法学硕士-17_民商法学 法学硕士-17_经济法学','二',36,4,'选修',1,1,'白国栋,季立刚,施鸿鹏','白国栋,季立刚,施鸿鹏','白国栋','白国栋','','','','',0,'2018-04-25 00:00:07',''),(208,'JM620057.01','国际法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','二',54,7,'必修',1,1,'何力,陆志安,王伟,朱丹','何力,陆志安,王伟,朱丹','王伟','王伟','','','','',0,'2018-04-25 22:22:10',''),(209,'JM620018.01','经济法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）1班','一',54,7,'必修',1,1,'陈立','陈立','陈立','陈立','','','','',0,'2018-04-25 00:00:07',''),(210,'JM620005.04','民事诉讼法学','法律硕士','2018-2019','法律硕士-17_法律硕士（非法学）2班','一',36,7,'必修',1,1,'章武生,段厚省','章武生,段厚省','段厚省','段厚省','','','','',0,'2018-04-27 22:22:41',''),(211,'JM620006','刑事诉讼法学','法律硕士','2018-2019','法律硕士-17_法律硕士（法学）','一',36,6,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:07',''),(212,'LAWS119007.02','法律与科技文明','本科','2018-2019','本科-_通识教育','一',36,9,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','','','','',0,'2018-04-25 00:00:07',''),(213,'927.003.1','国际经济法导论','本科','2018-2019','本科-17_第二专业教学','二',54,10,'必修',1,1,'何力','何力','何力','何力','','','','',0,'2018-04-25 00:00:07',''),(214,'LAWS130038','国际经济合同','本科','2018-2019','本科-16_法学专业教育','二',54,9,'选修',1,1,'龚柏华','龚柏华','龚柏华','龚柏华','','','','',0,'2018-04-25 00:00:07',''),(215,'LAWS130039','台港澳法','本科','2018-2019','本科-16_法学专业教育','二',36,9,'选修',1,1,'郭建','郭建','郭建','郭建','','','','',0,'2018-04-25 00:00:07',''),(216,'LAWS130034','证据学','本科','2018-2019','本科-16_法学专业教育','一',36,9,'选修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:07',''),(217,'LAWS130035','比较宪法','本科','2018-2019','本科-17_法学专业教育','二',36,9,'选修',1,1,'涂云新,王蔚','涂云新,王蔚','涂云新','涂云新','','','','',0,'2018-04-25 00:00:07',''),(218,'LAWS130036','国际投资法','本科','2018-2019','本科-16_法学专业教育','二',54,9,'选修',1,1,'陆志安,孙南申','陆志安,孙南申','陆志安','陆志安','','','','',0,'2018-04-25 00:00:07',''),(219,'LAWS130011','国际私法','本科','2018-2019','本科-17_法学专业教育','二',54,10,'必修',1,1,'陈力,孙南申','陈力,孙南申','孙南申','孙南申','','','','',0,'2018-04-25 00:00:07',''),(220,'LAWS130030','国际贸易法','本科','2018-2019','本科-16_法学专业教育','一',54,9,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 00:00:07',''),(222,'LAW620065','西方法律史专题','法学硕士','2018-2019','法学硕士-18_法律史','一',54,4,'必修',1,1,'赵立行','赵立行','赵立行','赵立行','','','','',0,'2018-04-25 00:00:07',''),(223,'LAWS130017','专业英语III(法律)','本科','2018-2019','本科-15_法学专业教育','一',54,10,'必修',1,1,'待定老师2','','待定老师2','王俊','','','','',0,'2018-04-27 22:13:43',''),(224,'LAWS160009','国际经济法','本科','2018-2019','本科-16_跨校辅修教学','二',54,10,'必修',1,1,'何力','何力','何力','何力','','','','',0,'2018-04-25 00:00:08',''),(225,'LAW630101','经济犯罪','法学硕士','2018-2019','法学硕士-17_刑法学','一',36,3,'选修',1,1,'汪明亮,王越','汪明亮,王越','汪明亮','汪明亮','','','','',0,'2018-04-25 00:00:08',''),(226,'LAW620079','刑事诉讼法专题','法学硕士','2018-2019','法学硕士-18_诉讼法学','一',54,4,'必修',1,1,'马贵翔','马贵翔','马贵翔','马贵翔','','','','',0,'2018-04-25 00:00:08',''),(227,'LAW620031','中国刑法','法学硕士','2018-2019','法学硕士-18_刑法学','一',54,4,'必修',1,1,'杜宇,王越','杜宇,王越','杜宇','杜宇','','','','',0,'2018-04-25 00:00:08',''),(228,'LAW620032','犯罪学','法学硕士','2018-2019','法学硕士-18_刑法学','一',54,4,'必修',1,1,'汪明亮','汪明亮','汪明亮','汪明亮','','','','',0,'2018-04-25 00:00:08',''),(229,'LAW620035','外国民事诉讼法专题','法学硕士','2018-2019','法学硕士-17_诉讼法学','一',54,4,'必修',1,1,'杨严炎,段厚省','杨严炎,段厚省','杨严炎','杨严炎','','','','',0,'2018-04-25 00:00:08',''),(230,'LAW630125','自然资源保护法专题','法学硕士','2018-2019','法学硕士-18_环境与资源保护法学','二',36,5,'选修',1,1,'张梓太,待定老师2','张梓太','张梓太','张梓太','','','','',0,'2018-04-28 14:27:16',''),(231,'LAW620037','外国刑事诉讼法专题','法学硕士','2018-2019','法学硕士-17_诉讼法学','一',54,4,'必修',1,1,'徐美君','徐美君','徐美君','徐美君','','','','',0,'2018-04-25 00:00:08',''),(232,'LAWS130001.01','行政法','本科','2018-2019','本科-18_法学专业教育','二',54,10,'必修',1,1,'刘志刚','刘志刚','刘志刚','刘志刚','','','','',0,'2018-04-25 00:00:08',''),(233,'LAW630019.01','公司法与破产法研究','法学硕士','2018-2019','法学硕士-17_民商法学','一',36,3,'选修',1,1,'白国栋,季立刚,李小宁','白国栋,季立刚,李小宁','李小宁','李小宁','','','','',0,'2018-04-25 00:00:08',''),(234,'SOSC120003.04','法理学导论','本科','2018-2019','本科-18_基础教育','一',54,10,'必修',3,1,'史大晓,杨晓畅,待定老师2','史大晓,杨晓畅','史大晓,杨晓畅,待定老师2','史大晓,杨晓畅,侯健','','','','',0,'2018-04-27 23:03:38',''),(235,'LAW630058.01','中国法律思想史专题','法学硕士','2018-2019','法学硕士-17_法学理论 法学硕士-17_法律史','二',36,4,'选修',1,1,'郭建,赖骏楠','郭建,赖骏楠','赖骏楠','赖骏楠','','','','',0,'2018-05-02 16:00:14',''),(236,'LAWS130014.01','国际经济法导论','本科','2018-2019','本科-16_法学专业教育','一',54,9,'必修',2,1,'张乃根,何力','张乃根,何力','何力,张乃根','何力,张乃根','','','','',0,'2018-04-25 09:51:30',''),(237,'LAW630061','民法原理与环境法','法学硕士','2018-2019','法学硕士-17_环境与资源保护法学','二',54,3,'选修',1,1,'陶蕾','陶蕾','陶蕾','陶蕾','','','','',0,'2018-04-25 00:00:08',''),(238,'JM620011.02','宪法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）2班','一',36,7,'必修',1,1,'潘伟杰,涂云新','潘伟杰,涂云新','潘伟杰','潘伟杰','','','','',0,'2018-04-25 00:00:08',''),(239,'JM620011.01','宪法学','法律硕士','2018-2019','法律硕士-18_法律硕士（非法学）1班','一',36,7,'必修',1,1,'潘伟杰,涂云新','潘伟杰,涂云新','潘伟杰','潘伟杰','','','','',0,'2018-04-25 00:00:08',''),(240,'LAW630068','国际金融信托法','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'高凌云','高凌云','高凌云','高凌云','','','','',0,'2018-04-25 00:00:08',''),(242,'LAW630058.02','中国法律思想史专题','法学硕士','2018-2019','法学硕士-18_法律史','二',36,5,'选修',1,1,'郭建,赖骏楠','郭建,赖骏楠','赖骏楠','赖骏楠','','','','',0,'2018-04-25 14:31:26',''),(243,'LAW630076','国际贸易的知识产权法','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'马忠法','马忠法','马忠法','马忠法','','','','',0,'2018-04-25 15:09:29',''),(244,'LAW630070','海商法研究','法学硕士','2018-2019','法学硕士-17_国际法学','一',36,3,'选修',1,1,'陈梁','陈梁','陈梁','陈梁','','','','',0,'2018-04-25 15:10:28',''),(248,'LAW630005','中国经济立法史','法学硕士','2018-2019','法学硕士-17_法律史','二',36,3,'选修',1,1,'郭建,赖骏楠','','赖骏楠','郭建','','','','',0,'2018-04-26 15:00:11',''),(249,'LAW630059','大陆法专题','法学硕士','2018-2019','法学硕士-17_法律史 法学硕士-17_刑法学','一',36,3,'选修',1,1,'史大晓,赵立行','','史大晓','史大晓','','','','',0,'2018-04-26 15:37:48',''),(250,'LAW630029','国际刑法','法学硕士','2018-2019','法学硕士-17_刑法学','二',36,3,'选修',1,1,'陆志安,朱丹','','朱丹','朱丹','','','','',0,'2018-04-26 15:40:48',''),(251,'SOSC120016','经济法','本科','2018-2019','本科-17_基础教育','',54,10,'必修',3,1,'施鸿鹏,李传轩,葛江虬','施鸿鹏,李传轩,葛江虬','李传轩,葛江虬,陈立','李传轩,葛江虬,陈立','','','','',0,'2018-04-25 00:00:07',''),(252,'MAST612116','专业英语(写作)','法学硕士','2018-2019','法学硕士-17_国际法学','',18,3,'必修',1,1,'陈梁','陈梁','陈梁','葛江虬','','','','',0,'2018-04-25 00:00:07','');
/*!40000 ALTER TABLE `course_history_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-18 15:29:56
