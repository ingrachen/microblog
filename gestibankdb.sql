-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le :  ven. 23 août 2019 à 15:47
-- Version du serveur :  5.7.17
-- Version de PHP :  5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `gestiBankDB`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `login` varchar(20) PRIMARY KEY NOT NULL,
  `password` LONGTEXT DEFAULT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `type` ENUM('admin', 'conseiller', 'client')
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `employe`
--

INSERT INTO `utilisateur` (`login`,`password`,`nom`, `prenom`, `email`, `type`) VALUES
('admin', password('admin'), 'smith', 'jean', 'jean.smith@domain.com', 'admin');
INSERT INTO `utilisateur` (`login`,`password`,`nom`, `prenom`, `email`, `type`) VALUES
('ag1dupont', password('jeandupont$'), 'dupont', 'jean','jeand.@gmail.com', 'conseiller');
CREATE TABLE `agent` (
  `mle` int(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
   `login` varchar(20) ,
   `date_debut` datetime DEFAULT NULL,
   `date_fin` datetime DEFAULT NULL,
   FOREIGN KEY (login) REFERENCES utilisateur(login)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `agent` (`mle`,`login`,`date_debut`, `date_fin`) VALUES
(1, 'ag1dupont', '2000-12-04', NULL);

CREATE TABLE `client` (
    `num_client` int(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `login` varchar(20) ,
    `conseiller` int(20) NOT NULL,
    `adresse` varchar(50) DEFAULT NULL,
    `telephone` varchar(10) DEFAULT NULL,
    `revenu_mensuel` float DEFAULT NULL,
    FOREIGN KEY (login) REFERENCES utilisateur(login),
    FOREIGN KEY (conseiller) REFERENCES agent(mle)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `compte` (
    `rib` varchar(20) PRIMARY KEY NOT NULL,
    `proprietaire` int(20) NOT NULL,
    `date_creation` datetime DEFAULT NULL,
    `solde` int(10) DEFAULT 0,
    `type` varchar(20) DEFAULT NULL,
    FOREIGN KEY (proprietaire) REFERENCES client(num_client)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `compte_epargne` (
    `num_compte` int(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `rib` varchar(20) NOT NULL,
    `taux_remuneration` int(1) DEFAULT NULL,
    `seuil_remuneration` int(5) DEFAULT NULL,
    FOREIGN KEY (rib) REFERENCES compte(rib)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `compte_courant` (
    `num_compte` int(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `rib` varchar(20) NOT NULL,
    `autorisation_decouvert` tinyint(1) DEFAULT 0,
    `taux_decouvert` float(2.1) DEFAULT 0,
    `entree_moyenne` int(10) DEFAULT 0,
    FOREIGN KEY (rib) REFERENCES compte(rib)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `operation` (
    `num_operation` int(20) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `rib_compte` VARCHAR(20) NOT NULL,
    `type_opt` ENUM('debit', 'credit','virement'),
    `valeur` INT(20) DEFAULT NULL,
     FOREIGN KEY (rib_compte) REFERENCES compte(rib)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


