-- MySQL Script generated by MySQL Workbench
-- Thu Dec 16 13:38:39 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema postman
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema postman
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `postman` ;
USE `postman` ;

-- -----------------------------------------------------
-- Table `postman`.`companies`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`companies` ;

CREATE TABLE IF NOT EXISTS `postman`.`companies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `active` TINYINT NULL DEFAULT 1,
  `company_name` VARCHAR(45) NULL,
  `short_name_latin` VARCHAR(20) NULL,
  `code_EDRPOU` VARCHAR(9) NULL,
  `phone` VARCHAR(19) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `company_name_UNIQUE` (`company_name` ASC) VISIBLE,
  UNIQUE INDEX `code_EDRPOU_UNIQUE` (`code_EDRPOU` ASC) VISIBLE,
  UNIQUE INDEX `phone_UNIQUE` (`phone` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`receivers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`receivers` ;

CREATE TABLE IF NOT EXISTS `postman`.`receivers` (
  `id_receivers` INT NOT NULL AUTO_INCREMENT,
  `id_companies` INT NOT NULL,
  `surname` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `middle_name` VARCHAR(45) NULL,
  `phone` VARCHAR(19) NULL,
  `city` VARCHAR(45) NULL,
  `street` VARCHAR(45) NULL,
  `building` VARCHAR(5) NULL,
  `floor` INT NULL,
  `receiverscol` VARCHAR(45) NULL,
  `comment` VARCHAR(255) NULL,
  `date_in` DATE NULL,
  `branch` VARCHAR(45) NULL,
  `active` TINYINT NULL DEFAULT 1,
  PRIMARY KEY (`id_receivers`),
  INDEX `id_idx` (`id_companies` ASC) VISIBLE,
  CONSTRAINT `id`
    FOREIGN KEY (`id_companies`)
    REFERENCES `postman`.`companies` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`postservices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`postservices` ;

CREATE TABLE IF NOT EXISTS `postman`.`postservices` (
  `id_postcervice` INT NOT NULL AUTO_INCREMENT,
  `postservice_name` VARCHAR(45) NULL,
  `last_contract` VARCHAR(45) NULL,
  PRIMARY KEY (`id_postcervice`),
  UNIQUE INDEX `id_postcervice_UNIQUE` (`id_postcervice` ASC) VISIBLE,
  UNIQUE INDEX `postcervice_name_UNIQUE` (`postservice_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`delivery_contracts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`delivery_contracts` ;

CREATE TABLE IF NOT EXISTS `postman`.`delivery_contracts` (
  `id_delivery_contract` INT NOT NULL AUTO_INCREMENT,
  `postservice_id` INT NULL,
  `name` VARCHAR(45) NULL,
  `bank_account` VARCHAR(45) NULL,
  `subcontract_nnumber` VARCHAR(45) NULL,
  `sending_date` DATE NULL,
  `payer` ENUM('Sender', 'Receiver') NULL,
  `finished` TINYINT NULL DEFAULT 0,
  `active` TINYINT NULL DEFAULT 1,
  PRIMARY KEY (`id_delivery_contract`),
  UNIQUE INDEX `subcontract_nnumber_UNIQUE` (`subcontract_nnumber` ASC) VISIBLE,
  INDEX `postcervice_id_idx` (`postservice_id` ASC) VISIBLE,
  CONSTRAINT `postcervice_id`
    FOREIGN KEY (`postservice_id`)
    REFERENCES `postman`.`postservices` (`id_postcervice`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`cities`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`cities` ;

CREATE TABLE IF NOT EXISTS `postman`.`cities` (
  `id_cities` INT NOT NULL AUTO_INCREMENT,
  `postservice_id` INT NULL,
  `city_name` VARCHAR(45) NULL,
  `city_token` VARCHAR(45) NULL,
  `citiescol` VARCHAR(45) NULL,
  PRIMARY KEY (`id_cities`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`streets`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`streets` ;

CREATE TABLE IF NOT EXISTS `postman`.`streets` (
  `id_streets` INT NOT NULL AUTO_INCREMENT,
  `city_id` INT NULL,
  `street_name` VARCHAR(45) NULL,
  `street_token` VARCHAR(45) NULL,
  PRIMARY KEY (`id_streets`),
  INDEX `city_id_idx` (`city_id` ASC) VISIBLE,
  CONSTRAINT `city_id`
    FOREIGN KEY (`city_id`)
    REFERENCES `postman`.`cities` (`id_cities`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`contract_waybills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`contract_waybills` ;

CREATE TABLE IF NOT EXISTS `postman`.`contract_waybills` (
  `id_waybills` INT NOT NULL AUTO_INCREMENT,
  `delivery_contracts_id` INT NULL,
  `waybills_receivers_id` INT NULL,
  `waybills_street_token_id` INT NULL,
  `total_cost` FLOAT NULL,
  `total_volume` FLOAT NULL,
  `total_places` INT NULL,
  `contract_waybills_token` VARCHAR(45) NULL,
  `waybils_pdf_file_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id_waybills`),
  UNIQUE INDEX `id_delivery_demands_UNIQUE` (`id_waybills` ASC) VISIBLE,
  UNIQUE INDEX `contract_waybills_token_UNIQUE` (`contract_waybills_token` ASC) VISIBLE,
  INDEX `waybills_to_receivers_idx` (`waybills_receivers_id` ASC) VISIBLE,
  INDEX `waybills_to_contracts_idx` (`delivery_contracts_id` ASC) VISIBLE,
  INDEX `contract_receiver_street_id_idx` (`waybills_street_token_id` ASC) VISIBLE,
  CONSTRAINT `waybills_to_receivers`
    FOREIGN KEY (`waybills_receivers_id`)
    REFERENCES `postman`.`receivers` (`id_receivers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `waybills_to_contracts`
    FOREIGN KEY (`delivery_contracts_id`)
    REFERENCES `postman`.`delivery_contracts` (`id_delivery_contract`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `contract_receiver_street_id`
    FOREIGN KEY (`waybills_street_token_id`)
    REFERENCES `postman`.`streets` (`id_streets`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `postman`.`parcells`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `postman`.`parcells` ;

CREATE TABLE IF NOT EXISTS `postman`.`parcells` (
  `id_parcells` INT NOT NULL AUTO_INCREMENT,
  `parcells_waybills_id` INT NULL,
  `items_number` INT NULL,
  `packs_number` INT NULL,
  `height_calculated` FLOAT NULL,
  `cost_calculated` FLOAT NULL,
  `pacells_pdf_file` VARCHAR(45) NULL,
  PRIMARY KEY (`id_parcells`),
  UNIQUE INDEX `id_delivery_demands_UNIQUE` (`id_parcells` ASC) VISIBLE,
  INDEX `parcells_waybills_id_idx` (`parcells_waybills_id` ASC) VISIBLE,
  UNIQUE INDEX `pacells_pdf_file_UNIQUE` (`pacells_pdf_file` ASC) VISIBLE,
  CONSTRAINT `parcells_waybills_id`
    FOREIGN KEY (`parcells_waybills_id`)
    REFERENCES `postman`.`contract_waybills` (`id_waybills`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
