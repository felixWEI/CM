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
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-03-15 12:42:13','1','教务员',1,'[{\"added\": {}}]',2,1),(2,'2018-03-15 12:51:20','2','8000',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(3,'2018-03-15 13:24:41','4','33080',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(4,'2018-03-15 13:31:23','4','33080',2,'[{\"changed\": {\"fields\": [\"last_login\", \"email\"]}}]',6,1),(5,'2018-03-15 13:31:33','3','33364',2,'[{\"changed\": {\"fields\": [\"last_login\", \"email\"]}}]',6,1),(6,'2018-04-19 23:26:54','6','20572',2,'[{\"changed\": {\"fields\": [\"last_login\", \"first_name\", \"last_name\", \"email\"]}}]',6,1),(7,'2018-04-19 23:33:48','7','20608',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(8,'2018-04-20 00:04:15','3','33364',2,'[{\"changed\": {\"fields\": [\"last_login\", \"email\"]}}]',6,1),(9,'2018-04-20 00:04:27','4','33080',2,'[{\"changed\": {\"fields\": [\"last_login\", \"email\"]}}]',6,1),(10,'2018-04-23 00:07:24','60','31075',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(11,'2018-04-23 00:07:39','36','L0824',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(12,'2018-04-23 00:07:51','35','L0400',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(13,'2018-04-24 20:00:54','61','31087',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(14,'2018-04-24 20:12:40','33','00028',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(15,'2018-04-25 00:19:42','33','00028',2,'[{\"changed\": {\"fields\": [\"last_login\"]}}]',6,1),(16,'2018-04-28 15:23:32','61','31087',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(17,'2018-04-28 15:23:47','60','31075',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(18,'2018-04-28 15:23:07','36','L0824',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(19,'2018-04-28 15:23:23','35','L0400',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(20,'2018-04-28 15:23:47','33','00028',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(21,'2018-04-28 15:23:59','4','33080',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(22,'2018-04-28 15:26:10','1','9999',2,'[{\"changed\": {\"fields\": [\"last_login\", \"first_name\", \"last_name\"]}}]',6,1),(23,'2018-04-28 15:36:35','7','20608',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(24,'2018-04-28 17:09:31','4','33080',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,1),(25,'2018-04-28 17:09:45','7','20608',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(26,'2018-04-28 17:10:16','35','L0400',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(27,'2018-04-28 17:10:29','36','L0824',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(28,'2018-04-28 17:11:02','60','31075',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(29,'2018-04-28 17:11:37','61','31087',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(30,'2018-04-28 17:12:02','33','00028',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',6,1),(31,'2019-04-12 12:34:19','34','00058',3,'',6,2),(32,'2019-04-12 12:43:13','10','04753',3,'',6,2),(33,'2019-04-12 12:47:52','63','34004',3,'',6,2),(34,'2019-04-12 13:00:55','14','20558',3,'',6,2),(35,'2019-04-12 13:26:45','33','00028',3,'',6,2),(36,'2019-04-12 13:31:13','70','36033',3,'',6,2),(37,'2019-04-12 13:31:41','77','N0001',3,'',6,2),(38,'2019-04-12 13:37:23','20','20588',3,'',6,2),(39,'2019-04-12 13:37:46','58','20390',3,'',6,2),(40,'2019-04-12 14:00:15','65','34082',3,'',6,2),(41,'2019-04-12 14:00:32','68','34161',3,'',6,2),(42,'2019-04-12 14:01:05','29','60038',3,'',6,2),(43,'2019-04-12 14:01:22','22','20550',3,'',6,2),(44,'2019-04-12 14:17:53','75','37228',3,'',6,2),(45,'2019-04-12 14:18:09','72','37036',3,'',6,2),(46,'2019-04-12 14:18:31','15','20569',3,'',6,2),(47,'2019-04-12 14:19:03','61','31087',3,'',6,2),(48,'2019-04-12 14:19:57','23','20414',3,'',6,2),(49,'2019-04-12 14:20:32','64','34075',3,'',6,2),(50,'2019-04-12 14:20:52','55','08081',3,'',6,2),(51,'2019-04-12 14:21:09','74','37158',3,'',6,2),(52,'2019-04-12 14:21:53','11','04754',3,'',6,2),(53,'2019-04-12 14:38:25','7','20608',3,'',6,2),(54,'2019-04-12 14:38:36','3','33364',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,2),(55,'2019-04-12 14:39:05','98','31087',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,2),(56,'2019-04-12 14:40:44','103','20608',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,2),(57,'2019-04-13 14:03:14','83','00028',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,2),(58,'2019-04-15 20:18:02','103','20608',3,'',6,2),(59,'2019-04-16 09:52:42','104','20608',2,'[{\"changed\": {\"fields\": [\"last_login\", \"is_staff\"]}}]',6,2);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-18 15:29:55
