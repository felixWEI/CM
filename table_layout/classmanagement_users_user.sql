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
-- Table structure for table `users_user`
--

DROP TABLE IF EXISTS `users_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  `nickname` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user`
--

LOCK TABLES `users_user` WRITE;
/*!40000 ALTER TABLE `users_user` DISABLE KEYS */;
INSERT INTO `users_user` VALUES (1,'pbkdf2_sha256$36000$dO0IejAaPMCk$Ag8/bdLPxhTf7U4/+YbFl0qWhM73PBg++x0MuIf/qF4=','2018-04-29 16:45:13',1,'9999','','','helloweifan@qq.com',1,1,'2018-03-15 12:40:57',''),(2,'pbkdf2_sha256$36000$fYxUkaOSaKUr$s1sQ2S346QnnUjzlFj9sgzUBhjBEjT54ydRQwBqckuU=','2018-03-15 12:48:00',0,'8000','','','helloweifan@qq.com',1,1,'2018-03-15 12:43:00',''),(3,'pbkdf2_sha256$36000$yM7ckNJp2pu3$i9NmAqEN9cDS3nsg723Y8g4dvr1+PY/YDNU28vK8bvQ=','2018-03-21 21:29:55',0,'33364','蕾','孙','545278672@qq.com',0,1,'2018-03-15 13:16:00',''),(4,'pbkdf2_sha256$36000$n2V7Q0QingmQ$3a2hri+iL2IeCqusaYeLqxwEZlRFwZVrtFgIYoDSZh0=','2019-04-07 21:37:48',0,'33080','妮','倪','545278672@qq.com',1,1,'2018-03-15 13:19:00',''),(5,'pbkdf2_sha256$36000$TGAVGiUL5pdr$oI0Yox+qBxFQOPVyjdvU+6+vWUWAooOUGVYMsoA+2mk=','2018-03-20 23:01:07',0,'20570','晓屏','孙','helloweifan@qq.com',0,1,'2018-03-19 11:20:57',''),(6,'pbkdf2_sha256$36000$ADlbVVfxtGOa$EDyemO9oFl4m2XvkD6kSr8CZVkRb07VfzYvGGiBw+KQ=','2018-03-21 21:29:39',0,'20390','立行','赵','helloweifan@qq.com',0,1,'2018-03-20 21:21:13',''),(8,'pbkdf2_sha256$36000$aZyKgyPDZlXc$qPUXyLQbF2V56jBvo1C5J4qhvyFtKGMQsC76+QtUjpU=','2018-03-21 21:29:46',0,'4465','明亮','汪','',0,1,'2018-03-20 22:18:43',''),(9,'pbkdf2_sha256$36000$ho5LnsVO24v3$Z6jCQqDCLSPOZxMvNFSVOm1dmSj3xweZuwCms/e2y2A=','2018-04-07 10:58:04',0,'26','武生','章','helloweifan@qq.com',0,1,'2018-04-06 22:24:33',''),(10,'pbkdf2_sha256$36000$aWUJu8IRB58k$KrRKnRJmiFFAmFDaCJ1ts5QILrrqqyRjosAxiTJvfMg=','2018-04-09 21:51:53',0,'58','健','侯','helloweifan@qq.com',0,1,'2018-04-09 21:51:40',''),(11,'pbkdf2_sha256$36000$g7ON6NKa4c2X$fCvmyGpZ8lk1S5C6rmJG6m1YX09KB3UgXoB4fCiZnUg=','2018-04-21 12:17:42',0,'04465','明亮','汪','helloweifan@qq.com',0,1,'2018-04-21 09:41:17',''),(12,'pbkdf2_sha256$36000$ChY8Go081tmj$0h+B4iWoCXCyM0slX9BazVOdjnoITMHHdQ9Xi1nf2Og=','2018-04-21 10:07:39',0,'L0824','璐','李','helloweifan@qq.com',0,1,'2018-04-21 10:07:26','');
/*!40000 ALTER TABLE `users_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-07 23:02:46
