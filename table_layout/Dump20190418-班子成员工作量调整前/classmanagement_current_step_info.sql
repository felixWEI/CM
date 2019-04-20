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
-- Table structure for table `current_step_info`
--

DROP TABLE IF EXISTS `current_step_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `current_step_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `arrange_class_status` varchar(45) DEFAULT NULL,
  `s1_year_info` varchar(45) DEFAULT NULL,
  `s2_undergraduate` varchar(45) DEFAULT NULL,
  `s2_postgraduate_1` varchar(45) DEFAULT NULL,
  `s2_postgraduate_2` varchar(45) DEFAULT NULL,
  `s2_doctor` varchar(45) DEFAULT NULL,
  `s2_start_request` varchar(45) DEFAULT NULL,
  `s2_deadline` datetime DEFAULT NULL,
  `s2_teacher_confirm_u` varchar(45) DEFAULT NULL,
  `s2_teacher_confirm_p1` varchar(45) DEFAULT NULL,
  `s2_teacher_confirm_p2` varchar(45) DEFAULT NULL,
  `s2_teacher_confirm_d` varchar(45) DEFAULT NULL,
  `s3_status_flag` varchar(45) DEFAULT NULL,
  `s4_status_flag` varchar(45) DEFAULT NULL,
  `s4_teacher_confirm_u` varchar(45) DEFAULT '0',
  `s4_teacher_confirm_p1` varchar(45) DEFAULT '0',
  `s4_teacher_confirm_p2` varchar(45) DEFAULT '0',
  `s4_teacher_confirm_d` varchar(45) DEFAULT '0',
  `s5_status_flag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_step_info`
--

LOCK TABLES `current_step_info` WRITE;
/*!40000 ALTER TABLE `current_step_info` DISABLE KEYS */;
INSERT INTO `current_step_info` VALUES (1,'start','2019-2020','2','2','2','2','2','2019-04-17 16:01:00','2','2','2','2','start arrange',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `current_step_info` ENABLE KEYS */;
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
