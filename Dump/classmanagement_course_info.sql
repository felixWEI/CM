-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: classmanagement
-- ------------------------------------------------------
-- Server version	5.7.20-log

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
  `class_name` varchar(45) NOT NULL,
  `semester` varchar(45) DEFAULT NULL,
  `course_hour` float NOT NULL,
  `course_degree` float NOT NULL,
  `course_type` varchar(45) DEFAULT NULL,
  `allow_teachers` int(11) DEFAULT NULL,
  `times_every_week` int(11) DEFAULT NULL,
  `suit_teacher` varchar(200) DEFAULT NULL,
  `insert_time` timestamp(6) NULL DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_info`
--

LOCK TABLES `course_info` WRITE;
/*!40000 ALTER TABLE `course_info` DISABLE KEYS */;
INSERT INTO `course_info` VALUES (3,'LAW830035','中国财产法史专题','博士','17','国际法学','二',36,1,'必选',1,1,'',NULL,'2018-01-30 22:21:07'),(4,'LAW830032','近代大陆法专题','博士','17','国际法学','二',36,3,'必选',1,1,'',NULL,'2018-01-30 22:23:47'),(5,'LAWS130004.01','中国法制史','本科','15','法学院本科','三',54,3,'必选',1,1,'',NULL,'2018-01-30 22:25:23'),(6,'LAWS130004.02','中国法制史','本科','15','法学院本科','三',54,3,'必选',1,1,'',NULL,'2018-01-30 22:25:47'),(7,'LAWS130013.01','专业英语I(法律)','本科','14','法学院本科','五',36,3,'必选',1,1,'',NULL,'2018-01-30 22:26:45'),(8,'LAWS130061.01','国际法','本科','14','法学院本科','五',54,3,'必选',1,2,'',NULL,'2018-01-30 22:27:45'),(9,'LAW620037','外国刑事诉讼法专题','法学硕士','16','诉讼法学','三',54,3,'本科',2,1,'WOODPECKER',NULL,'2018-01-30 22:32:57'),(10,'LAW620043','国际环境法专题','法学硕士','17','环境与资源保护法','二',54,3,'法学硕士',1,1,'',NULL,'2018-01-30 22:51:31');
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

-- Dump completed on 2018-03-13 21:38:24
