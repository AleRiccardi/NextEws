
/*************************************

Sql file that will be called for the
creation from the command:

$ flask init-db

@author:    Alericcardi
@version:   1.0.0
 */


CREATE TABLE `categories` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `slug` TEXT NOT NULL,
  `name` TEXT NOT NULL,
  `class_icon` TEXT NOT NULL,
  `class_color` TEXT NOT NULL
);

INSERT INTO `categories` (`id`, `slug`, `name`, `class_icon`, `class_color`) VALUES
(0, 'business', 'Business', 'fas fa-building', 'text-primary'),
(1, 'entertainment', 'Entertainment', 'fab fa-fort-awesome', 'text-danger'),
(2, 'politics', 'Politics', 'fas fa-briefcase', 'text-info'),
(3, 'sport', 'Sport', 'fas fa-basketball-ball', 'text-warning'),
(4, 'technology', 'Technology', 'fas fa-robot', 'text-success');


CREATE TABLE `authors` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `name` TEXT  NOT NULL
);


CREATE TABLE `news` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `title` TEXT NOT NULL,
  `description` TEXT DEFAULT NULL,
  `content` TEXT,
  `url` TEXT NOT NULL,
  `url_to_image` TEXT DEFAULT NULL,
  `published_at` DATETIME NOT NULL,
  `id_author` INTEGER DEFAULT NULL,
  `id_source` INTEGER NOT NULL,
  `id_category` INTEGER
);

CREATE TABLE `sources` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `slug` TEXT NOT NULL,
  `name` TEXT NOT NULL
);

--
-- Dump dei dati per la tabella `sources`
--

INSERT INTO `sources` (`id`, `slug`, `name`) VALUES
(1, 'techcrunch', 'TechCrunch'),
(2, 'cnn', 'CNN'),
(3, 'fox-news', 'Fox News'),
(4, 'nbc-news', 'NBC News'),
(5, 'independent', 'Independent'),
(6, 'vice-news', 'Vice News'),
(7, 'the-economist', 'The Economist');


