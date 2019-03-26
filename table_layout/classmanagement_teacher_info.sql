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
-- Table structure for table `teacher_info`
--

DROP TABLE IF EXISTS `teacher_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacher_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `teacher_id` varchar(11) NOT NULL,
  `teacher_name` varchar(45) DEFAULT NULL,
  `first_semester_expect` float DEFAULT NULL,
  `second_semester_expect` float DEFAULT NULL,
  `first_semester_hours` float DEFAULT NULL,
  `second_semester_hours` float DEFAULT NULL,
  `first_semester_degree` float DEFAULT NULL,
  `second_semester_degree` float DEFAULT NULL,
  `teacher_apply_done` varchar(45) DEFAULT NULL,
  `notes` varchar(2000) DEFAULT NULL,
  `insert_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `teacher_title` varchar(45) DEFAULT NULL,
  `major` varchar(45) DEFAULT NULL,
  `teacher_type` varchar(45) DEFAULT NULL,
  `birthday` date NOT NULL,
  `sex` varchar(45) NOT NULL,
  `lock_state` tinyint(4) DEFAULT '0',
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `teacher_id_UNIQUE` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_info`
--

LOCK TABLES `teacher_info` WRITE;
/*!40000 ALTER TABLE `teacher_info` DISABLE KEYS */;
INSERT INTO `teacher_info` VALUES (1,'20572','胡鸿高',1,1,108,162,10,23,NULL,NULL,'2018-04-27 14:56:20.537150',NULL,NULL,NULL,'0000-00-00','',0,NULL),(2,'25152','孟庆',1,1,72,NULL,9,NULL,NULL,NULL,'2018-04-27 14:56:14.548329',NULL,NULL,NULL,'0000-00-00','',0,NULL),(3,'20558','郭建',1,1,162,72,25,13,NULL,NULL,'2018-04-27 14:56:21.189476',NULL,NULL,NULL,'0000-00-00','',0,NULL),(4,'20569','王俊',1,1,90,144,16,18,'申报结束',NULL,'2018-04-27 14:56:15.798556',NULL,NULL,NULL,'0000-00-00','',0,NULL),(5,'20605','唐海红',1,1,39,36,5.83333,9,NULL,NULL,'2018-04-27 14:56:19.932975',NULL,NULL,NULL,'0000-00-00','',0,NULL),(6,'20608','朱伟芳',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.166176',NULL,NULL,NULL,'0000-00-00','',0,NULL),(7,'20570','孙晓屏',1,1,126,144,25,17,'申报结束',NULL,'2018-04-27 14:56:20.699620',NULL,NULL,NULL,'0000-00-00','',0,NULL),(8,'20557','张乃根',1,1,90,108,18,15,'申报结束','《国际经济法导论》是我负责的上海市精品课程。','2018-04-27 14:56:20.622908',NULL,NULL,NULL,'0000-00-00','',0,NULL),(9,'02009','姚军',1,1,216,108,40,24,'申报结束',NULL,'2018-04-27 14:56:16.816683',NULL,NULL,NULL,'0000-00-00','',0,NULL),(10,'20588','龚柏华',1,1,90,108,16,14,'申报结束',NULL,'2018-04-27 14:56:22.412310',NULL,NULL,NULL,'0000-00-00','',0,NULL),(11,'20549','张光杰',1,1,126,54,25,5,'申报结束',NULL,'2018-04-27 14:56:16.490567',NULL,NULL,NULL,'0000-00-00','',0,NULL),(12,'20550','王蔚',1,1,144,72,17,17,'申报结束',NULL,'2018-04-27 14:56:20.812953',NULL,NULL,NULL,'0000-00-00','',0,NULL),(13,'20414','季立刚',1,1,72,144,12,17.5,NULL,NULL,'2018-04-27 14:56:20.959348',NULL,NULL,NULL,'0000-00-00','',0,NULL),(14,'01359','吴建超',1,1,12,NULL,2.33333,NULL,NULL,NULL,'2018-04-27 14:56:22.214169',NULL,NULL,NULL,'0000-00-00','',0,NULL),(15,'20591','陆志安',1,1,117,144,14.5,23,NULL,NULL,'2018-04-27 14:56:18.022894',NULL,NULL,NULL,'0000-00-00','',0,NULL),(16,'20589','陈力',1,1,90,162,12,27,'申报结束',NULL,'2018-04-27 14:56:22.506301',NULL,NULL,NULL,'0000-00-00','',0,NULL),(17,'02010','吕萍',1,1,90,90,17,13,NULL,NULL,'2018-04-27 14:56:21.950050',NULL,NULL,NULL,'0000-00-00','',0,NULL),(18,'07041','李小宁',1,1,90,126,14,21,'申报结束',NULL,'2018-04-27 14:56:15.092185',NULL,NULL,NULL,'0000-00-00','',0,NULL),(19,'60038','朱淑娣',1,1,126,144,17,12,'申报结束',NULL,'2018-04-27 14:56:16.418375',NULL,NULL,NULL,'0000-00-00','',0,NULL),(20,'90016','潘伟杰',1,1,144,126,25,25,'申报结束',NULL,'2018-04-27 14:56:20.072848',NULL,NULL,NULL,'0000-00-00','',0,NULL),(21,'90093','何力',1,1,144,144,18,19,'申报结束',NULL,'2018-04-27 14:56:19.141370',NULL,NULL,NULL,'0000-00-00','',0,NULL),(22,'00027','白国栋',1,1,108,72,21,12,'申报结束',NULL,'2018-04-27 14:56:22.268312',NULL,NULL,NULL,'0000-00-00','',0,NULL),(23,'00028','王志强',0.5,0.5,126,90,17,18,'申报结束','行政管理岗位','2018-04-27 14:56:21.618601',NULL,NULL,NULL,'0000-00-00','',0,NULL),(24,'00058','侯健',1,1,180,144,30,21,'申报结束',NULL,'2018-04-27 14:56:18.497657',NULL,NULL,NULL,'0000-00-00','',0,NULL),(25,'00143','章武生',1,1,198,117,24.5,17.5,'申报结束',NULL,'2018-04-27 14:56:19.853764',NULL,NULL,NULL,'0000-00-00','',0,NULL),(26,'04166','马贵翔',1,1,189,162,24.5,22,'申报结束',NULL,'2018-04-27 14:56:20.432303',NULL,NULL,NULL,'0000-00-00','',0,NULL),(27,'04310','陈梁',1,1,90,144,15,24,'申报结束',NULL,'2018-04-27 14:56:22.170074',NULL,NULL,NULL,'0000-00-00','',0,NULL),(28,'04208','徐美君',1,1,117,108,19.5,15,'申报结束',NULL,'2018-04-27 14:56:15.621555',NULL,NULL,NULL,'0000-00-00','',0,NULL),(29,'04375','杨玉芝',1,1,27,36,3.5,9,NULL,NULL,'2018-04-27 14:56:15.477992',NULL,NULL,NULL,'0000-00-00','',0,NULL),(30,'04445','孙南申',1,1,126,180,15,26,'申报结束',NULL,'2018-04-27 14:56:14.953298',NULL,NULL,NULL,'0000-00-00','',0,NULL),(31,'04641','张建伟',1,1,108,90,13,9,'申报结束',NULL,'2018-04-27 14:56:16.171780',NULL,NULL,NULL,'0000-00-00','',0,NULL),(32,'04466','许凌艳',1,1,72,126,16,18,'申报结束',NULL,'2018-04-27 14:56:15.310988',NULL,NULL,NULL,'0000-00-00','',0,NULL),(33,'04465','汪明亮',1,1,146,162,15,27,'申报结束','基于硕士博士课头太多','2018-04-27 14:56:15.401537',NULL,NULL,NULL,'0000-00-00','',0,NULL),(34,'04695','高凌云',1,0,72,54,14,9,'申报结束',NULL,'2018-04-27 14:56:22.655267',NULL,NULL,NULL,'0000-00-00','',0,NULL),(35,'04736','刘士国',1,1,108,126,15,17,NULL,NULL,'2018-04-27 14:56:19.737956',NULL,NULL,NULL,'0000-00-00','',0,NULL),(36,'04753','史大晓',1,1,180,90,28,13,'申报结束',NULL,'2018-04-27 14:56:16.336825',NULL,NULL,NULL,'0000-00-00','',0,NULL),(37,'04754','杜宇',1,1,144,162,23,19,'申报结束',NULL,'2018-04-27 14:56:17.370158',NULL,NULL,NULL,'0000-00-00','',0,NULL),(38,'04751','梁咏',1,1,90,162,17,29,NULL,NULL,'2018-04-27 14:56:16.016789',NULL,NULL,NULL,'0000-00-00','',0,NULL),(39,'04915','段厚省',1,1,180,162,31.5,21,'申报结束',NULL,'2018-04-27 14:56:16.582905',NULL,NULL,NULL,'0000-00-00','',0,NULL),(40,'04948','刘志刚',1,1,126,126,15,18,'申报结束','学校要求必须承担1门本科生课程，近五年一直承担行政法课程。目前，本专业本科生课程相较于以往明显减少。所以，选择一门本科生课程：《行政法》','2018-04-27 14:56:21.109763',NULL,NULL,NULL,'0000-00-00','',0,NULL),(41,'05410','马忠法',1,1,162,108,25,20,NULL,NULL,'2018-04-27 14:56:19.660751',NULL,NULL,NULL,'0000-00-00','',0,NULL),(42,'06120','蒋云蔚',1,1,90,90,14,16,NULL,NULL,'2018-04-27 14:56:16.094496',NULL,NULL,NULL,'0000-00-00','',0,NULL),(43,'06121','罗霄',1,1,90,108,17,24,NULL,NULL,'2018-04-27 14:56:19.494308',NULL,NULL,NULL,'0000-00-00','',0,NULL),(44,'06375','朱芹',1,1,126,NULL,17,NULL,NULL,NULL,'2018-04-27 14:56:17.104452',NULL,NULL,NULL,'0000-00-00','',0,NULL),(45,'07339','王伟',1,1,54,90,5,13,NULL,NULL,'2018-04-27 14:56:19.243642',NULL,NULL,NULL,'0000-00-00','',0,NULL),(46,'07330','杨严炎',1,1,216,117,38,18.5,'申报结束',NULL,'2018-04-27 14:56:15.889379',NULL,NULL,NULL,'0000-00-00','',0,NULL),(47,'07344','张梓太',1,1,135,153,12.5,28.5,'申报结束',NULL,'2018-04-27 14:56:21.290913',NULL,NULL,NULL,'0000-00-00','',0,NULL),(48,'08081','李传轩',1,1,117,180,14,24,'申报结束',NULL,'2018-04-27 14:56:15.691742',NULL,NULL,NULL,'0000-00-00','',0,NULL),(49,'08159','陆优优',1,1,99,54,18.5,10,NULL,NULL,'2018-04-27 14:56:18.935824',NULL,NULL,NULL,'0000-00-00','',0,NULL),(50,'09120','韩涛',1,1,162,NULL,23,NULL,NULL,NULL,'2018-04-27 14:56:18.350266',NULL,NULL,NULL,'0000-00-00','',0,NULL),(51,'20390','赵立行',1,1,180,198,25,23,'申报结束',NULL,'2018-04-27 14:56:16.253684',NULL,NULL,NULL,'0000-00-00','',0,NULL),(52,'31043','孙笑侠',1,1,162,90,19,13,'申报结束',NULL,'2018-04-27 14:56:17.191182',NULL,NULL,NULL,'0000-00-00','',0,NULL),(53,'31075','王琳',1,1,108,126,16,16,NULL,NULL,'2018-04-27 14:56:22.589536',NULL,NULL,NULL,'0000-00-00','',0,NULL),(54,'31087','李世刚',1,1,108,108,16,14,'申报结束',NULL,'2018-04-27 14:56:22.033957',NULL,NULL,NULL,'0000-00-00','',0,NULL),(55,'50128','胡华忠',1,1,18,90,6,19,NULL,NULL,'2018-04-27 14:56:20.265861',NULL,NULL,NULL,'0000-00-00','',0,NULL),(56,'33080','倪妮',1,1,27,36,4.5,4.5,NULL,NULL,'2018-04-27 14:56:14.818251',NULL,NULL,NULL,'0000-00-00','',0,NULL),(57,'33364','孙蕾',1,1,108,NULL,26,NULL,NULL,NULL,'2018-04-27 14:56:14.704409',NULL,NULL,NULL,'0000-00-00','',0,NULL),(58,'34004','杨晓畅',1,1,144,36,25,4,'申报结束',NULL,'2018-04-27 14:56:20.366127',NULL,NULL,NULL,'0000-00-00','',0,NULL),(59,'34075','陶蕾',1,1,126,135,19.5,15.5,'申报结束',NULL,'2018-04-27 14:56:16.671244',NULL,NULL,NULL,'0000-00-00','',0,NULL),(60,'34082','朱丹',1,1,135,90,15.5,18,'申报结束',NULL,'2018-04-27 14:56:21.538434',NULL,NULL,NULL,'0000-00-00','',0,NULL),(61,'34077','涂云新',1,1,90,108,18,19,'申报结束',NULL,'2018-04-27 14:56:21.795680',NULL,NULL,NULL,'0000-00-00','',0,NULL),(62,'34086','班天可',1,1,126,108,14,15,'申报结束',NULL,'2018-04-27 14:56:21.715462',NULL,NULL,NULL,'0000-00-00','',0,NULL),(63,'34161','熊浩',0.9,0.9,36,54,8,16,'申报结束',NULL,'2018-04-27 14:56:15.244097',NULL,NULL,NULL,'0000-00-00','',0,NULL),(64,'35001','杜仪方',1,1,90,108,20,14,NULL,NULL,'2018-04-27 14:56:22.100909',NULL,NULL,NULL,'0000-00-00','',0,NULL),(65,'36033','孟烨',1,1,162,72,23,5,'申报结束',NULL,'2018-04-27 14:56:22.338224',NULL,NULL,NULL,'0000-00-00','',0,NULL),(66,'36074','汪奕',1,1,12,NULL,2.33333,NULL,NULL,NULL,'2018-04-27 14:56:16.726461',NULL,NULL,NULL,'0000-00-00','',0,NULL),(67,'37036','丁文杰',0.4,0.6,36,54,9,9,'申报结束',NULL,'2018-04-27 14:56:21.054610',NULL,NULL,NULL,'0000-00-00','',0,NULL),(68,'37061','陈立',1,1,90,90,12,18,'申报结束',NULL,'2018-04-27 14:56:21.864893',NULL,NULL,NULL,'0000-00-00','',0,NULL),(69,'37158','袁国何',1,1,182,180,24,25,'申报结束',NULL,'2018-04-27 14:56:15.537255',NULL,NULL,NULL,'0000-00-00','',0,NULL),(70,'37228','葛江虬',1,1,126,126,20,18,'申报结束','按照《课程设置改革》计划，在改革完成之后，《合同法》课程将可以同时被本科生和法律硕士所选择，课程难度系数将上升到7（目前已经是7，而根据经验选课人数即便只有法硕也在150人左右）以上。','2018-04-27 14:56:18.836057',NULL,NULL,NULL,'0000-00-00','',0,NULL),(71,'L0824','李璐',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.462136',NULL,NULL,NULL,'0000-00-00','',0,NULL),(72,'L0400','邓双丽',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.465701',NULL,NULL,NULL,'0000-00-00','',0,NULL),(73,'N0001','赖俊楠',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.469629',NULL,NULL,NULL,'0000-00-00','',0,NULL),(74,'N0002','施鸿鹏',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.473656',NULL,NULL,NULL,'0000-00-00','',0,NULL),(75,'N0003','王越',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.478226',NULL,NULL,NULL,'0000-00-00','',0,NULL),(76,'T0001','实务导师1',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.481730',NULL,NULL,NULL,'0000-00-00','',0,NULL),(77,'T0002','实务导师2',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.486412',NULL,NULL,NULL,'0000-00-00','',0,NULL),(78,'T0003','待定老师',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.490117',NULL,NULL,NULL,'0000-00-00','',0,NULL),(79,'T0004','教学院长',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-24 16:00:29.494159',NULL,NULL,NULL,'0000-00-00','',0,NULL),(80,'T0005','待定老师2',1,1,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-27 14:04:38.730275',NULL,NULL,NULL,'0000-00-00','',0,NULL);
/*!40000 ALTER TABLE `teacher_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-23 14:41:44