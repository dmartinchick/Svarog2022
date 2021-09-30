CREATE TABLE IF NOT EXISTS `users`(
    `user_id` INT NOT NULL UNIQUE,
    `team_subs` TEXT,
    `event_subs` TEXT,

    PRIMARY KEY (`user_id`)
);

CREATE TABLE IF NOT EXISTS `event`(
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `type` ENUM('Кубок туризма','Кубок спорта','Кубок культуры','Прочее') NOT NULL,
    `coefficient` FLOAT (2,1) DEFAULT NULL,
    `place` VARCHAR(255) DEFAULT NULL,
    `rule` TEXT DEFAULT NULL COMMENT 'Правила мероприятия',
    `composition` VARCHAR(255) DEFAULT NULL COMMENT 'Количество и состав участников',
    `address` VARCHAR (255) DEFAULT NULL COMMENT 'ссылка на картинку',

    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `team`(
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR (255) NOT  NULL,
    `holding` BIT NOT NULL COMMENT 'Входит ли команда в состав холдинга 0-False 1-True',
    `address` VARCHAR (255) DEFAULT NULL COMMENT 'ссылка на логотип команды',

    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `schedule`(
    `id` INT AUTO_INCREMENT,
    `event_name_id` INT NOT NULL,
    `time_start` DATETIME NOT NULL,
    `time_end` DATETIME  NOT NULL,

    PRIMARY KEY (`id`),

    CONSTRAINT FK_schedule_event FOREIGN KEY (`event_name_id`)
    REFERENCES `event` (`id`)
);

CREATE TABLE  IF NOT EXISTS `results`(
    `id` INT AUTO_INCREMENT,
    `event_id` INT NOT NULL,
    `team_id` INT NOT NULL,

    PRIMARY KEY (`id`),

    CONSTRAINT FK_result_event FOREIGN KEY (`event_id`)
    REFERENCES `event` (`id`),
    CONSTRAINT FK_result_team FOREIGN KEY (`team_id`)
    REFERENCES `team` (`id`)
);

INSERT INTO `event`
(id,name,type,coefficient,place,rule,composition) 
VALUES
(1,'Техника пешеходного туризма','Кубок туризма',2.0,NULL,X'd0a1d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d18f20d0bfd180d0bed0b2d0bed0b4d18fd182d181d18f20d0b220d181d182d180d0b0d185d0bed0b2d0bed187d0bdd18bd18520d181d0b8d181d182d0b5d0bcd0b0d18520d0bfd0be20d0bfd180d0b0d0b2d0b8d0bbd0b0d0bc20d181d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d0b93a20d0b2d0b8d0b420d181d0bfd0bed180d182d0b020c2abd0a2d183d180d0b8d0b7d0bc20d181d0bfd0bed180d182d0b8d0b2d0bdd18bd0b9c2bb20d181d0bfd0bed180d182d0b8d0b2d0bdd0b0d18f20d0b4d0b8d181d186d0b8d0bfd0bbd0b8d0bdd0b020c2abd0a2d183d180d0b8d181d182d181d0bad0be2dd0bfd180d0b8d0bad0bbd0b0d0b4d0bdd0bed0b520d0bcd0bdd0bed0b3d0bed0b1d0bed180d18cd0b52e20d0a2d0b5d185d0bdd0b8d0bad0b020d0bfd0b5d188d0b5d185d0bed0b4d0bdd0bed0b3d0be20d182d183d180d0b8d0b7d0bcd0b0c2bb2e','2 человека - 1м + 1ж'),
(2,'Заезд команд, разбивка лагеря','Прочее',NULL,'Лагерь команд',NULL,NULL),
(3,'Обед','Прочее',NULL,'Лагерь команд',NULL,NULL),
(4,'Заседание оргкомитета, судейской коллегии, совещание капитанов команд, жеребьевка','Прочее',NULL,'Судейский лагерь',NULL,'1 человек - Капитан команды Либо лицо его замещающее'),
(5,'Построение команд, торжественное открытие Фестиваля','Прочее',NULL,'Парковка Базы отдыха *Днепровские зори*',NULL,NULL),
(6,'Ловкость рук','Кубок спорта',1.5,'Футбольная площадка',X'd091d180d0bed181d0bed0ba20d0b820d0bbd0bed0b2d0bbd18f20d0bad183d180d0b8d0bdd18bd18520d18fd0b8d18620d0bdd0b020d0b4d0b0d0bbd18cd0bdd0bed181d182d18c2e20d09cd183d0b6d187d0b8d0bdd0b020d0bcd0b5d182d0b0d0b5d1822c20d0b4d0b5d0b2d183d188d0bad0b020d0bbd0bed0b2d0b8d1822e20d09dd0b020d0b2d181d19120d0bfd180d0be20d0b2d181d191203320d0bfd0bed0bfd18bd182d0bad0b82e20d0a3d187d0b0d181d182d0bdd0b8d0bad0b820d0bfd180d0bed0b4d0bed0bbd0b6d0b0d18ed18220d0bfd0bed0bfd18bd182d0bad18320d0bfd0bed0bad0b020d18fd0b9d186d0be20d0bdd0b520d0bed0bad0b0d0b6d0b5d182d181d18f20d0bdd0b020d0b7d0b5d0bcd0bbd0b520d0b8d0bbd0b820d0bdd0b520d0b1d183d0b4d0b5d18220d180d0b0d0b7d0b1d0b8d182d0be2e20d09fd0bed0b1d0b5d0b6d0b4d0b0d0b5d18220d0bfd0b0d180d0b02c20d0bad0bed182d0bed180d0b0d18f20d0bfd0bed0b9d0bcd0b0d0b5d18220d0a6d095d09bd09ed09520d18fd0b9d186d0be20d0bdd0b020d0bcd0b0d0bad181d0b8d0bcd0b0d0bbd18cd0bdd0bed0bc20d180d0b0d181d181d182d0bed18fd0bdd0b8d0b82e','2 человека - 1м + 1ж'),
(7,'Борьба за мужика','Кубок спорта',1.5,'Крытая площадка',X'd09fd180d0bed0b2d0bed0b4d0b8d182d181d18f20d181d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d0b520d0bfd0be20d0bfd180d0b0d0b2d0b8d0bbd0b0d0bc20d0bcd0b0d181d1812dd180d0b5d181d182d0bbd0b8d0bdd0b3d0b02028d181d181d18bd0bbd0bad0b020d0bdd0b020d0b2d0b8d0b4d0b5d0be2068747470733a2f2f7777772e796f75747562652e636f6d2f77617463683f763d775439306e6a354556504920292e20d094d0b5d0b2d183d188d0bad0b820d181d0b0d0b4d18fd182d181d18f20d0bdd0b020d0b7d0b5d0bcd0bbd18e2c20d18120d0b4d0b2d183d18520d181d182d0bed180d0bed0bd20d0bed18220d180d0b0d0b7d0b4d0b5d0bbd0b8d182d0b5d0bbd18cd0bdd0bed0b920d0b4d0bed181d0bad0b82c20d0bfd180d0b8d0b6d0b8d0bcd0b0d18ed182d181d18f20d0ba20d0bdd0b5d0b920d181d182d183d0bfd0bdd18fd0bcd0b82e20d0a0d183d0bad0b0d0bcd0b820d0b1d0b5d180d183d182d181d18f20d0b7d0b020d0b3d0b8d0bcd0bdd0b0d181d182d0b8d187d0b5d181d0bad183d18e20d0bfd0b0d0bbd0bad18320d0b4d180d183d0b320d0bfd180d0bed182d0b8d0b220d0b4d180d183d0b3d0b02e20d0a6d0b5d0bbd18c20d181d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d18f20e2809320d0bed182d0bed180d0b2d0b0d182d18c20d181d0bed0bfd0b5d180d0bdd0b8d186d18320d0bed18220d0b7d0b5d0bcd0bbd0b820d0b820d0bfd0b5d180d0b5d182d18fd0bdd183d182d18c20d0bdd0b020d181d0b5d0b1d18f2e','1 человек - девушка. Ограничение по весу - до 65 кг'),
(8,'Ужин','Прочее',NULL,'Лагерь команд',NULL,NULL),
(9,'Боди-арт','Кубок культуры',1.0,'Крытая площадка',X'd093d0bbd0b0d0b2d0bdd18bd0bc20d0bed0b1d18ad0b5d0bad182d0bed0bc20d0b1d0bed0b4d0b82dd0b0d180d182d0b020d181d182d0b0d0bdd0bed0b2d0b8d182d181d18f20d182d0b5d0bbd0be20d187d0b5d0bbd0bed0b2d0b5d0bad0b02c20d0b020d181d0bed0b4d0b5d180d0b6d0b0d0bdd0b8d0b520d180d0b0d181d0bad180d18bd0b2d0b0d0b5d182d181d18f20d18120d0bfd0bed0bcd0bed189d18cd18e20d0bdd0b5d0b2d0b5d180d0b1d0b0d0bbd18cd0bdd0bed0b3d0be20d18fd0b7d18bd0bad0b03a20d0bfd0bed0b72c20d0b6d0b5d181d182d0bed0b22c20d0bcd0b8d0bcd0b8d0bad0b82c20d0bdd0b0d0bdd0b5d181d0b5d0bdd0b8d18f20d0bdd0b020d182d0b5d0bbd0be20d0b7d0bdd0b0d0bad0bed0b22c20c2abd183d0bad180d0b0d188d0b5d0bdd0b8d0b9c2bb2e20d092d180d0b5d0bcd18f20d0bfd180d0b5d0b4d181d182d0b0d0b2d0bbd0b5d0bdd0b8d18f20d0b4d0be203520d0bcd0b8d0bdd183d1822e20d097d0b020d0bfd180d0b5d0b2d18bd188d0b5d0bdd0b8d0b520d0bbd0b8d0bcd0b8d182d0b020d0b2d180d0b5d0bcd0b5d0bdd0b820e2809320d188d182d180d0b0d184203520d0bed187d0bad0bed0b22e20d09ed186d0b5d0bdd0b8d0b2d0b0d0b5d182d181d18f3a20d181d0bed0bed182d0b2d0b5d182d181d182d0b2d0b8d0b520d182d180d0b5d0b1d0bed0b2d0b0d0bdd0b8d18fd0bc20d0b820d182d0b5d0bcd0b0d182d0b8d0bad0b520d0bad0bed0bdd0bad183d180d181d0b02c20d185d183d0b4d0bed0b6d0b5d181d182d0b2d0b5d0bdd0bdd0bed0b520d0bed184d0bed180d0bcd0bbd0b5d0bdd0b8d0b52c20d0bcd183d0b7d18bd0bad0b0d0bbd18cd0bdd0bed0b520d181d0bed0bfd180d0bed0b2d0bed0b6d0b4d0b5d0bdd0b8d0b52c20d0bed180d0b8d0b3d0b8d0bdd0b0d0bbd18cd0bdd0bed181d182d18c20d0b820d0bdd0bed0b2d0b0d182d0bed180d181d182d0b2d0be20d0bfd0bed0b4d0b0d187d0b820d182d0b5d0bcd18b2e','2 человека - 1м + 1ж. В массовке может быть до 5 человек'),
(10,'Ночное ориентирование','Кубок туризма',2.0,NULL,X'd09ed180d0b8d0b5d0bdd182d0b8d180d0bed0b2d0b0d0bdd0b8d0b520d0bfd0be20d0b2d18bd0b1d0bed180d1832e200ad0a1d182d0b0d180d18220d180d0b0d0b7d0b4d0b5d0bbd18cd0bdd18bd0b93a20d0bcd183d0b6d187d0b8d0bdd0b020d0b820d0b6d0b5d0bdd189d0b8d0bdd0b020d181d182d0b0d180d182d183d18ed1822020d180d0b0d0b7d0b4d0b5d0bbd18cd0bdd0be20d0bfd0be20d181d182d0b0d180d182d0bed0b2d0bed0bcd18320d0bfd180d0bed182d0bed0bad0bed0bbd1832e20d09dd0b020d0b4d0b8d181d182d0b0d0bdd186d0b8d0b820d0b1d183d0b4d0b5d18220d183d181d182d0b0d0bdd0bed0b2d0bbd0b5d0bdd0be20d0bad0bed0bdd182d180d0bed0bbd18cd0bdd0bed0b520d0b2d180d0b5d0bcd18f20d0bdd0b020d0bad0b0d0b6d0b4d0bed0b3d0be20d183d187d0b0d181d182d0bdd0b8d0bad0b020d0b8d0b720d0bad0bed0bcd0b0d0bdd0b4d18b2e20d097d0b0d187d0b5d18220d180d0b0d0b7d0b4d0b5d0bbd18cd0bdd18bd0b93a20d0bcd183d0b6d181d0bad0bed0b920d0b820d0b6d0b5d0bdd181d0bad0b8d0b92e20d0a3d187d0b0d181d182d0bdd0b8d0bad0b820d0bfd0bed0bbd183d187d0b0d18ed18220d0b1d0b0d0bbd0bbd18b2c20d0bad0bed182d0bed180d18bd0b520d181d183d0bcd0bcd0b8d180d183d18ed182d181d18f2c20d0b820d0bed0bfd180d0b5d0b4d0b5d0bbd18fd0b5d182d181d18f20d180d0b5d0b7d183d0bbd18cd182d0b0d18220d0bad0bed0bcd0b0d0bdd0b4d18b2e200ad09fd180d0b820d180d0b0d0b2d0bdd0bed0bc20d0bad0bed0bbd0b8d187d0b5d181d182d0b2d0b520d0b1d0b0d0bbd0bbd0bed0b22c20d181d0bcd0bed182d180d0b8d182d181d18f20d0bed0b1d189d0b5d0b520d0b2d180d0b5d0bcd18f20d0bfd180d0bed185d0bed0b6d0b4d0b5d0bdd0b8d18f20d0b4d0b8d181d182d0b0d0bdd186d0b8d0b82c20d0b4d0b0d0bbd0b5d0b520d181d183d0bcd0bcd0b020d0bdd0b0d0b9d0b4d0b5d0bdd0bdd18bd18520d0bfd0b8d0bad0b5d182d0bed0b22e20d095d181d0bbd0b820d0bed0b4d0b8d0bd20d0b8d0b720d183d187d0b0d181d182d0bdd0b8d0bad0bed0b220d0bad0bed0bcd0b0d0bdd0b4d18b20d0bdd0b520d183d0bbd0bed0b6d0b8d0bbd181d18f20d0b220d0bad0bed0bdd182d180d0bed0bbd18cd0bdd0bed0b520d0b2d180d0b5d0bcd18f2c20d182d0be20d180d0b5d0b7d183d0bbd18cd182d0b0d18220d0b220d0bad0bed0bcd0b0d0bdd0b4d0bdd18bd0b920d0b7d0b0d187d0b5d18220e28093d0bdd0bed0bbd18c20d0b1d0b0d0bbd0bbd0bed0b22e','2 человека - 1м + 1ж'),
(11,'Дискотека','Прочее',NULL,'Крытая площадка',NULL,NULL),
(12,'Подъем, завтрак','Прочее',NULL,'Лагерь команд',NULL,NULL),
(13,'Зарядка, подведение итогов первого дня','Прочее',NULL,'Парковка Базы отдыха *Днепровские зори*',NULL,NULL),
(14,'Велотуризм','Кубок туризма',2.0,NULL,X'd0a1d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d18f20d0bfd180d0bed0b2d0bed0b4d18fd182d181d18f20d0bfd0be20d0bfd180d0b0d0b2d0b8d0bbd0b0d0bc20d181d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d0b93a20d0b2d0b8d0b420d181d0bfd0bed180d182d0b020c2abd0a2d183d180d0b8d0b7d0bc20d181d0bfd0bed180d182d0b8d0b2d0bdd18bd0b9c2bb20d181d0bfd0bed180d182d0b8d0b2d0bdd0b0d18f20d0b4d0b8d181d186d0b8d0bfd0bbd0b8d0bdd0b020c2abd0a2d183d180d0b8d181d182d181d0bad0be2dd0bfd180d0b8d0bad0bbd0b0d0b4d0bdd0bed0b520d0bcd0bdd0bed0b3d0bed0b1d0bed180d18cd0b52e20d0a2d0b5d185d0bdd0b8d0bad0b020d0b2d0b5d0bbd0bed181d0b8d0bfd0b5d0b4d0bdd0bed0b3d0be20d182d183d180d0b8d0b7d0bcd0b0c2bb2e20d09dd0b020d181d182d0b0d180d18220d0bad0bed0bcd0b0d0bdd0b4d0b020d0bfd180d0b8d0b1d18bd0b2d0b0d0b5d18220d0bdd0b020d181d0b2d0bed0b8d18520d0b2d0b5d0bbd0bed181d0b8d0bfd0b5d0b4d0b0d18520d0b820d0b220d181d0b2d0bed0b8d18520d188d0bbd0b5d0bcd0b0d1852e20d09fd180d0b8d0bcd0b5d180d0bdd18bd0b920d0bfd0b5d180d0b5d187d0b5d0bdd18c20d18dd182d0b0d0bfd0bed0b220d184d0b8d0b3d183d180d0bdd0bed0b3d0be20d0b2d0bed0b6d0b4d0b5d0bdd0b8d18f20d0b2d0b5d0bbd0bed181d0b8d0bfd0b5d0b4d0b03a20d0b2d0bed181d18cd0bcd0b5d180d0bad0b02c20d0bad180d183d0b32c20d0bad0bed0bbd0b5d18f2c20d0b7d0b8d0b3d0b7d0b0d0b32c20d0bad0b0d187d0b0d18ed189d0b0d18fd181d18f20d0b4d0bed181d0bad0b02c20d0b7d0bcd0b5d0b9d0bad0b02c20d0bfd0b5d180d0b5d0bdd0bed18120d0b1d183d182d18bd0bbd0bad0b82c20d0bfd0b5d180d0b5d0b2d0b5d18120d0bad0bed0bbd18cd186d0b02c20d0bfd180d0bed0b5d0b7d0b420d0bcd0b0d180d0bad0b8d180d0bed0b2d0b0d0bdd0bdd0bed0b3d0be20d183d187d0b0d181d182d0bad0b02c20d0bbd0b5d181d182d0bdd0b8d186d0b02c20d184d0b8d0bdd0b8d1882e20d0a1d182d0b0d180d18220d0bad0bed0bcd0b0d0bdd0b420d181d0bed0b3d0bbd0b0d181d0bdd0be20d181d182d0b0d180d182d0bed0b2d0bed0bcd18320d0bfd180d0bed182d0bed0bad0bed0bbd1832e','2 человека - 1м + 1ж'),
(15,'Волейбол','Кубок спорта',2.0,'Волейбольная площадка',X'd0a1d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d18f20d0bfd180d0bed0b2d0bed0b4d18fd182d181d18f20d181d0bed0b3d0bbd0b0d181d0bdd0be20d183d182d0b2d0b5d180d0b6d0b4d0b5d0bdd0bdd18bd0bc20d0bfd180d0b0d0b2d0b8d0bbd0b0d0bc20d0b8d0b7203320d0bfd0b0d180d182d0b8d0b920d0b4d0be203220d0bfd0bed0b1d0b5d0b42e20d0a1d0b8d181d182d0b5d0bcd0b020d0bfd180d0bed0b2d0b5d0b4d0b5d0bdd0b8d18f20d182d183d180d0bdd0b8d180d0b020d0b1d183d0b4d0b5d18220d0bed0bfd180d0b5d0b4d0b5d0bbd0b5d0bdd0b020d0bdd0b020d181d0bed0b2d0b5d189d0b0d0bdd0b8d0b820d180d183d0bad0bed0b2d0bed0b4d0b8d182d0b5d0bbd0b5d0b920d0bad0bed0bcd0b0d0bdd0b420d0b220d0b7d0b0d0b2d0b8d181d0b8d0bcd0bed181d182d0b820d0bed18220d0bad0bed0bbd0b8d187d0b5d181d182d0b2d0b020d183d187d0b0d181d182d0b2d183d18ed189d0b8d18520d0bad0bed0bcd0b0d0bdd0b42e','6 человек - 2м + 2ж (основной состав), 1м + 1ж (запасные)'),
(16,'Молот Тора','Кубок спорта',1.5,'Футбольная площадка',X'd09cd0b5d182d0b0d0bdd0b8d0b520d0bcd0bed0bbd0bed182d0b020d0bdd0b020d0b4d0b0d0bbd18cd0bdd0bed181d182d18c2e20d09220d180d0b0d181d0bfd0bed180d18fd0b6d0b5d0bdd0b8d0b820d183d187d0b0d181d182d0bdd0b8d0bad0b0203320d0bfd0bed0bfd18bd182d0bad0b82e','1 человек'),
(17,'Выбивалы','Кубок спорта',2.0,'Волейбольная площадка',X'd09220d0b3d180d183d0bfd0bfd0b520d0bfd180d0bed185d0bed0b4d18fd18220d181d182d18bd0bad0bed0b2d18bd0b520d0bcd0b0d182d187d0b82c20d0bbd183d187d188d0b0d18f20d0bad0bed0bcd0b0d0bdd0b4d0b020d0b8d0b720d0b3d180d183d0bfd0bfd18b20d0b2d18bd185d0bed0b4d18fd18220d0b220d184d0b8d0bdd0b0d0bbd18cd0bdd18bd0b920d182d183d180d0bdd0b8d1802c20d0b3d0b4d0b520d0b820d0bed0bfd180d0b5d0b4d0b5d0bbd18fd18ed18220d0bfd0bed0b1d0b5d0b4d0b8d182d0b5d0bbd18f20d0b220d0bad180d183d0b3d0bed0b2d0bed0b920d181d0b8d181d182d0b5d0bcd0b52e20d09220d0b7d0b0d0b2d0b8d181d0b8d0bcd0bed181d182d0b820d0bed18220d0bfd0bed0b1d0b5d0b4d0b8d182d0b5d0bbd18f20d184d0b8d0bdd0b0d0bbd0b020d0b8d0b4d0b5d18220d180d0b0d181d0bfd180d0b5d0b4d0b5d0bbd0b5d0bdd0b8d0b520d0bcd0b5d181d18220d0b220d0bed181d182d0b0d0bbd18cd0bdd18bd18520d0b3d180d183d0bfd0bfd0b0d1852e','10 участников + 2 запасных (замены допускаются только между матчами)'),
(18,'Бивуак','Кубок культуры',1.0,'Лагерь команд',X'd09220d0bad0b0d187d0b5d181d182d0b2d0b520d182d0b5d0bcd18b20d0bbd0b0d0b3d0b5d180d18f20d0bad0b0d0b6d0b4d0b0d18f20d0bad0bed0bcd0b0d0bdd0b4d0b020d0b2d18bd0b1d0b8d180d0b0d0b5d18220d181d0b5d0b1d0b520d0bbd18ed0b1d0bed0b920d0b8d0b720d0bad0b8d0bdd0bed184d0b8d0bbd18cd0bcd0bed0b22e20d09ed186d0b5d0bdd0b8d0b2d0b0d18ed182d181d18f20d182d0b5d0bcd0b0d182d0b8d187d0b5d181d0bad0b0d18f20d0bed180d0b8d0b3d0b8d0bdd0b0d0bbd18cd0bdd0bed181d182d18c20d0bbd0b0d0b3d0b5d180d18f2c20d0bed184d0bed180d0bcd0bbd0b5d0bdd0b8d0b520d0b820d0b5d0b3d0be20d181d0bed0bed182d0b2d0b5d182d181d182d0b2d0b8d0b520d0b2d18bd0b1d180d0b0d0bdd0bdd0bed0b920d182d0b5d0bcd0b52c20d181d0b0d0bdd0b8d182d0b0d180d0bdd0be2dd0b3d0b8d0b3d0b8d0b5d0bdd0b8d187d0b5d181d0bad0bed0b520d181d0bed181d182d0bed18fd0bdd0b8d0b520d0bbd0b0d0b3d0b5d180d18f20d0b820d181d0bed0bed182d0b2d0b5d182d181d182d0b2d0b8d0b520d0b5d0b3d0be20d0bcd0b5d180d0b0d0bc20d0b1d0b5d0b7d0bed0bfd0b0d181d0bdd0bed181d182d0b82e',NULL),
(19,'Драник-fest','Кубок культуры',1.0,'Лагерь команд',X'd09ad0bed0bdd0bad183d180d18120d0bfd0bed185d0bed0b4d0bdd0bed0b3d0be20d0b1d0bbd18ed0b4d0b02c20d0b220d0bad0b0d187d0b5d181d182d0b2d0b520d0bed181d0bdd0bed0b2d0bdd0bed0b3d0be20d18fd0b2d0bbd18fd18ed182d181d18f20d0b4d180d0b0d0bdd0b8d0bad0b82e20d09ed186d0b5d0bdd0b8d0b2d0b0d18ed182d181d18f20d0b2d0bad183d181d0bed0b2d18bd0b520d0bad0b0d187d0b5d181d182d0b2d0b020d0b820d0bed180d0b8d0b3d0b8d0bdd0b0d0bbd18cd0bdd0bed181d182d18c20d0bfd0bed0b4d0b0d187d0b82028d0b4d180d0b0d0bdd0b8d0bad0b1d183d180d0b3d0b5d1802c20d181d183d188d0b820d0b8d0b720d0b4d180d0b0d0bdd0b8d0bad0bed0b220d0b820d1822ed0b42e2920d09ed184d0bed180d0bcd0bbd18fd0b5d182d181d18f20d0b2d181d0b520d0b220d0b2d0b8d0b4d0b520d0b4d0b5d0b3d183d181d182d0b0d186d0b8d0bed0bdd0bdd0bed0b920d0bfd0bbd0bed189d0b0d0b4d0bad0b82e20d09ad0b0d0b6d0b4d0bed0b520d0b1d0bbd18ed0b4d0be20d0b4d0bed0bbd0b6d0bdd0be20d0b1d18bd182d18c20d0bfd0bed0b4d0bfd0b8d181d0b0d0bdd0be2028d0bdd0b0d0b7d0b2d0b0d0bdd0b8d0b520d0bad0bed0bcd0b0d0bdd0b4d18b20d0b820d0bdd0b0d0b7d0b2d0b0d0bdd0b8d0b520d0b1d0bbd18ed0b4d0b0292e',NULL),
(20,'Творческий конкурс','Кубок культуры',1.0,'Крытая площадка',X'd09fd180d0b5d0b4d181d182d0b0d0b2d0bbd18fd0b5d18220d181d0bed0b1d0bed0b920d0b8d181d0bfd0bed0bbd0bdd0b5d0bdd0b8d0b520d0bad0bed0bcd0b0d0bdd0b4d0bed0b920d182d0b2d0bed180d187d0b5d181d0bad0bed0b3d0be20d0bdd0bed0bcd0b5d180d0b02c20d181d0bed0b3d0bbd0b0d181d0bdd0be20d182d0bed0bcd18320d0bad0b8d0bdd0bed184d0b8d0bbd18cd0bcd1832c20d0bad0bed182d0bed180d18bd0b920d0bed0bdd0b820d0b2d18bd0b1d180d0b0d0bbd0b820d0b220d0bad0b0d187d0b5d181d182d0b2d0b520d182d0b5d0bcd18b20d0bbd0b0d0b3d0b5d180d18f2e20d0a2d0b5d0bcd0b020d0bad0bed0bdd0bad183d180d181d0b020c2abd09220d0bfd0bed0b3d0bed0bdd0b520d0b7d0b020d09ed181d0bad0b0d180d0bed0bcc2bb2e20d09ed0b3d180d0b0d0bdd0b8d187d0b5d0bdd0b8d0b520d0bfd0be20d0b2d180d0b5d0bcd0b5d0bdd0b820e2809320d0b4d0be203620d0bcd0b8d0bdd183d1822e20d097d0b020d0bfd180d0b5d0b2d18bd188d0b5d0bdd0b8d0b520d0bbd0b8d0bcd0b8d182d0b020d0b2d180d0b5d0bcd0b5d0bdd0b820e2809320d188d182d180d0b0d184202d3520d0bed187d0bad0bed0b22e',NULL),
(21,'Туристический маршрут','Кубок туризма',2.0,NULL,X'd0a1d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d18f20d0bfd180d0bed0b2d0bed0b4d18fd182d181d18f20d0b1d0b5d0b720d181d182d180d0b0d185d0bed0b2d0bed187d0bdd18bd18520d181d0b8d181d182d0b5d0bc2c20d0bfd0be20d0bfd180d0b0d0b2d0b8d0bbd0b0d0bc20d181d0bed180d0b5d0b2d0bdd0bed0b2d0b0d0bdd0b8d0b93a20d0b2d0b8d0b420d181d0bfd0bed180d182d0b020c2abd0a2d183d180d0b8d0b7d0bc20d181d0bfd0bed180d182d0b8d0b2d0bdd18bd0b9c2bb20d181d0bfd0bed180d182d0b8d0b2d0bdd0b0d18f20d0b4d0b8d181d186d0b8d0bfd0bbd0b8d0bdd0b020c2abd0a2d183d180d0b8d181d182d181d0bad0be2dd0bfd180d0b8d0bad0bbd0b0d0b4d0bdd0bed0b520d0bcd0bdd0bed0b3d0bed0b1d0bed180d18cd0b52e20d0a2d0b5d185d0bdd0b8d0bad0b020d0bfd0b5d188d0b5d185d0bed0b4d0bdd0bed0b3d0be20d182d183d180d0b8d0b7d0bcd0b0c2bb2e20d094d0b8d181d182d0b0d0bdd186d0b8d18f3a312c3520d0bad0b8d0bbd0bed0bcd0b5d182d180d0b02e','4 человека - 2м + 2ж'),
(22,'Перетягивание каната','Кубок спорта',2.0,'Футбольная площадка',X'd0a2d183d180d0bdd0b8d18020d0bfd180d0bed0b2d0bed0b4d0b8d182d181d18f20d0bfd0be20d0bfd0bed0b4d0b3d180d183d0bfd0bfd0b0d0bc2c20d0b220d184d0b8d0bdd0b0d0bbd18cd0bdd18bd0b520d0b1d0bed0b820d0b2d18bd185d0bed0b4d0b8d18220d182d0bed0bbd18cd0bad0be20d0bed0b4d0bdd0b020d0bad0bed0bcd0b0d0bdd0b4d0b020d0b8d0b720d0b3d180d183d0bfd0bfd18b2e20d09220d0b7d0b0d0b2d0b8d181d0b8d0bcd0bed181d182d0b820d0bed18220d0bfd0bed0b1d0b5d0b4d0b8d182d0b5d0bbd18f20d184d0b8d0bdd0b0d0bbd0b020d0b8d0b4d0b5d18220d180d0b0d181d0bfd180d0b5d0b4d0b5d0bbd0b5d0bdd0b8d0b520d0bcd0b5d181d18220d0b220d0bed181d182d0b0d0bbd18cd0bdd18bd18520d0b3d180d183d0bfd0bfd0b0d1852e','Не более 7 мужчин. Ограничение по суммарному весу - не более 570 кг.'),
(23,'Подведение итогов, закрытие туристического слета','Прочее',NULL,'Парковка Базы отдыха *Днепровские зори*',NULL,NULL),
(24,'Отъезд','Прочее',NULL,NULL,NULL,NULL);


UPDATE `event`
SET `name`='Зарядка, подведение итогов первого дня'
WHERE `id`=13;


INSERT INTO `team`
(`name`,`holding`)
VALUES
('Прокат',1),
('Сталь',1),
('ByCord',1),
('ЗУбры',1),
('ГКС+Меттранс',1),
('РАЗАМ',1),
('Белвторчермет',1),
('ММЗ',1),
('МПЗ',1),
('РМЗ',1),
('Интеграл',0),
('МАЗ',0),
('МЗКТ',0),
('Могилевлифтмаш',0);

INSERT INTO `schedule`
(`event_name_id`,`time_start`,`time_end`)
VALUES
((SELECT `id` FROM `event` WHERE `name`='Техника пешеходного туризма'), '2021-07-18 13:00', '2021-07-18 15:30' ),
((SELECT `id` FROM `event` WHERE `name`='Заезд команд, разбивка лагеря'), '2021-07-18 09:00', '2021-07-18 15:30'),
((SELECT `id` FROM `event` WHERE `name`='Заседание оргкомитета, судейской коллегии, совещание капитанов команд, жеребьевка'), '2021-07-18 16:00', '2021-07-18 17:00'),
((SELECT `id` FROM `event` WHERE `name`='Построение команд, торжественное открытие Фестиваля'), '2021-07-18 17:15', '2021-07-18 18:00'),
((SELECT `id` FROM `event` WHERE `name`='Ловкость рук'), '2021-07-18 18:00', '2021-07-18 19:30'),
((SELECT `id` FROM `event` WHERE `name`='Борьба за мужика'), '2021-07-18 19:30', '2021-07-18 20:30'),
((SELECT `id` FROM `event` WHERE `name`='Волейбол'), '2021-07-18 19:30', '2021-07-18 21:30'),
((SELECT `id` FROM `event` WHERE `name`='Боди-арт'), '2021-07-18 21:30', '2021-07-18 23:30'),
((SELECT `id` FROM `event` WHERE `name`='Ночное ориентирование'), '2021-07-18 22:00', '2021-07-19 00:00'),
((SELECT `id` FROM `event` WHERE `name`='Дискотека'), '2021-07-18 23:30', '2021-07-19 02:30'),
((SELECT `id` FROM `event` WHERE `name`='Зарядка, подведение итогов первого дня'), '2021-07-19 08:00', '2021-07-19 08:30'),
((SELECT `id` FROM `event` WHERE `name`='Туристический маршрут'), '2021-07-19 08:30', '2021-07-19 13:00'),
((SELECT `id` FROM `event` WHERE `name`='Волейбол'), '2021-07-19 08:30', '2021-07-19 14:00'),
((SELECT `id` FROM `event` WHERE `name`='Молот Тора'), '2021-07-19 14:00', '2021-07-19 15:30'),
((SELECT `id` FROM `event` WHERE `name`='Выбивалы'), '2021-07-19 15:00', '2021-07-19 20:00'),
((SELECT `id` FROM `event` WHERE `name`='Бивуак'), '2021-07-19 16:00', '2021-07-19 18:00'),
((SELECT `id` FROM `event` WHERE `name`='Драник-fest'), '2021-07-19 18:00', '2021-07-19 19:00'),
((SELECT `id` FROM `event` WHERE `name`='Творческий конкурс'), '2021-07-19 21:00', '2021-07-19 23:30'),
((SELECT `id` FROM `event` WHERE `name`='Дискотека'), '2021-07-19 23:30', '2021-07-20 02:30'),
((SELECT `id` FROM `event` WHERE `name`='Выбивалы'), '2021-07-20 09:15', '2021-07-20 11:00'),
((SELECT `id` FROM `event` WHERE `name`='Велотуризм'), '2021-07-20 09:15', '2021-07-20 11:00'),
((SELECT `id` FROM `event` WHERE `name`='Перетягивание каната'), '2021-07-20 11:00', '2021-07-20 12:00'),
((SELECT `id` FROM `event` WHERE `name`='Подведение итогов, закрытие туристического слета'), '2021-07-20 13:00', '2021-07-20 14:30');


SELECT `name`, `time_start`
FROM `schedule` INNER JOIN `event` ON `schedule`.`event_name_id` = `event`.`id`
WHERE `time_start` > '2021-07-18 19:29:00' 
ORDER BY `time_start`
LIMIT 2;

SELECT time_start FROM schedule ORDER BY time_start LIMIT 1;


ALTER TABLE `event`
ADD `name_en` VARCHAR(100) DEFAULT NULL ;

UPDATE `event` 
SET `name_en`="hiking_technique"
WHERE `name`="Техника пешеходного туризма";
UPDATE `event` 
SET `name_en`="sleight_of_hand"
WHERE `name`="Ловкость рук";
UPDATE `event` 
SET `name_en`="fight_for_the_man"
WHERE `name`="Борьба за мужика";
UPDATE `event` 
SET `name_en`="body_art"
WHERE `name`="Боди-арт";
UPDATE `event` 
SET `name_en`="night_orientation"
WHERE `name`="Ночное ориентирование";
UPDATE `event` 
SET `name_en`="cycling_tourism"
WHERE `name`="Велотуризм";
UPDATE `event` 
SET `name_en`="volleyball"
WHERE `name`="Волейбол";
UPDATE `event` 
SET `name_en`="thors_hammer"
WHERE `name`="Молот Тора";
UPDATE `event` 
SET `name_en`="knockers"
WHERE `name`="Выбивалы";
UPDATE `event` 
SET `name_en`="bivouac"
WHERE `name`="Бивуак";
UPDATE `event` 
SET `name_en`="dranik_fest"
WHERE `name`="Драник-fest";
UPDATE `event` 
SET `name_en`="creative_competition"
WHERE `name`="Творческий конкурс";
UPDATE `event` 
SET `name_en`="tourist_route"
WHERE `name`="Туристический маршрут";
UPDATE `event` 
SET `name_en`="tug_of_war"
WHERE `name`="Перетягивание каната";


SELECT user_id,team_subs, event_subs FROM users;