-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.0.17 - MySQL Community Server - GPL
-- Server OS:                    Win64
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for pipe_db
CREATE DATABASE IF NOT EXISTS `pipe_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pipe_db`;

-- Dumping structure for table pipe_db.bibliometrics
CREATE TABLE IF NOT EXISTS `bibliometrics` (
  `bibliometric_id` int(11) NOT NULL AUTO_INCREMENT,
  `times_cited` int(11) DEFAULT NULL,
  `recent_citations` int(11) DEFAULT NULL,
  `retrieved_date` date NOT NULL,
  `relative_citation_ratio` float DEFAULT NULL,
  `field_citation_ratio` float DEFAULT NULL,
  `doi` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`bibliometric_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.citation_store
CREATE TABLE IF NOT EXISTS `citation_store` (
  `author` mediumtext COLLATE utf8mb4_unicode_ci,
  `doi` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` mediumtext COLLATE utf8mb4_unicode_ci,
  `type` mediumtext COLLATE utf8mb4_unicode_ci,
  `issued_date` date DEFAULT NULL,
  `subject` mediumtext COLLATE utf8mb4_unicode_ci,
  `pub_title` mediumtext COLLATE utf8mb4_unicode_ci,
  `pub_publisher` mediumtext COLLATE utf8mb4_unicode_ci,
  `issn` varchar(9) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `isbn` varchar(14) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `issue` mediumtext COLLATE utf8mb4_unicode_ci,
  `volume` mediumtext COLLATE utf8mb4_unicode_ci,
  `page` mediumtext COLLATE utf8mb4_unicode_ci,
  `classification_id` int(11) DEFAULT NULL,
  `identified_date` date DEFAULT NULL,
  PRIMARY KEY (`doi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.labels
CREATE TABLE IF NOT EXISTS `labels` (
  `label_id` varchar(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label_name` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  UNIQUE KEY `labels_label_id_uindex` (`label_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.message_store
CREATE TABLE IF NOT EXISTS `message_store` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `email_id` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `title` mediumtext COLLATE utf8mb4_unicode_ci,
  `snippet` mediumtext COLLATE utf8mb4_unicode_ci,
  `m_author` mediumtext COLLATE utf8mb4_unicode_ci,
  `m_pub_title` mediumtext COLLATE utf8mb4_unicode_ci,
  `m_pub_year` int(11) DEFAULT NULL,
  `sent_date` date DEFAULT NULL,
  `harvested_date` date DEFAULT NULL,
  `source` varchar(2) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id_status` tinyint(1) DEFAULT NULL,
  `label_id` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `doi` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_crossref_run` date DEFAULT NULL,
  `snippet_match` tinyint(1) DEFAULT NULL,
  `highlight_length` int(11) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.names
CREATE TABLE IF NOT EXISTS `names` (
  `name_id` int(11) NOT NULL AUTO_INCREMENT,
  `doi` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `label` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usage_key` int(11) DEFAULT NULL,
  `rundate` date DEFAULT NULL,
  PRIMARY KEY (`name_id`),
  KEY `names_citation_store_doi_fk` (`doi`),
  CONSTRAINT `names_citation_store_doi_fk` FOREIGN KEY (`doi`) REFERENCES `citation_store` (`doi`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.nhm_pubs
CREATE TABLE IF NOT EXISTS `nhm_pubs` (
  `issn` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pub_title` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`issn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.open_access
CREATE TABLE IF NOT EXISTS `open_access` (
  `oa_id` int(11) NOT NULL AUTO_INCREMENT,
  `best_oa_url` mediumtext COLLATE utf8mb4_unicode_ci,
  `updated_date` date DEFAULT NULL,
  `retrieved_date` date NOT NULL,
  `pdf_url` mediumtext COLLATE utf8mb4_unicode_ci,
  `is_oa` tinyint(1) DEFAULT NULL,
  `doi` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `doi_url` varchar(70) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `host_type` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `version` varchar(25) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`oa_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for table pipe_db.taxonomy
CREATE TABLE IF NOT EXISTS `taxonomy` (
  `usageKey` int(11) NOT NULL,
  `scientificName` text COLLATE utf8mb4_unicode_ci,
  `canonicalName` text COLLATE utf8mb4_unicode_ci,
  `rank` text COLLATE utf8mb4_unicode_ci,
  `status` text COLLATE utf8mb4_unicode_ci,
  `kingdom` text COLLATE utf8mb4_unicode_ci,
  `phylum` text COLLATE utf8mb4_unicode_ci,
  `order` text COLLATE utf8mb4_unicode_ci,
  `family` text COLLATE utf8mb4_unicode_ci,
  `species` text COLLATE utf8mb4_unicode_ci,
  `genus` text COLLATE utf8mb4_unicode_ci,
  `kingdomKey` int(11) DEFAULT NULL,
  `phylumKey` int(11) DEFAULT NULL,
  `classKey` int(11) DEFAULT NULL,
  `orderKey` int(11) DEFAULT NULL,
  `familyKey` int(11) DEFAULT NULL,
  `genusKey` int(11) DEFAULT NULL,
  `speciesKey` int(11) DEFAULT NULL,
  `class_name` text COLLATE utf8mb4_unicode_ci,
  `rundate` date DEFAULT NULL,
  PRIMARY KEY (`usageKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.

-- Dumping structure for view pipe_db.vw_classifier
-- Creating temporary table to overcome VIEW dependency errors
CREATE TABLE `vw_classifier` (
	`doi` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`nhm_sub` INT(1) NOT NULL,
	`snippet_match` TINYINT(1) NULL,
	`highlight_length` INT(11) NULL,
	`label_id` VARCHAR(8) NULL COLLATE 'utf8mb4_unicode_ci'
) ENGINE=MyISAM;

-- Dumping structure for view pipe_db.vw_classifier
-- Removing temporary table and create final VIEW structure
DROP TABLE IF EXISTS `vw_classifier`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_classifier` AS select `c`.`doi` AS `doi`,if((`c`.`issn` in (select `p`.`issn` from `nhm_pubs` `p`) and (`c`.`issn` is not null)),true,false) AS `nhm_sub`,`m`.`snippet_match` AS `snippet_match`,`m`.`highlight_length` AS `highlight_length`,`m`.`label_id` AS `label_id` from (`citation_store` `c` join `message_store` `m`) where ((`c`.`doi` = `m`.`doi`) and (`c`.`classification_id` is null)) order by `c`.`doi`;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
