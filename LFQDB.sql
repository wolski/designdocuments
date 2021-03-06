-- MySQL Script generated by MySQL Workbench
-- Fri Aug  7 13:16:15 2015
-- Model: LFQDB    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema LFQDB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema LFQDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LFQDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `LFQDB` ;

-- -----------------------------------------------------
-- Table `LFQDB`.`Protein`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Protein` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Protein` (
  `idProtein` INT NOT NULL COMMENT '',
  `proteinID` VARCHAR(45) NOT NULL COMMENT '',
  `houseKeeping` TINYINT(1) NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT 'ID',
  PRIMARY KEY (`idProtein`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`Experiment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Experiment` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Experiment` (
  `idExperiment` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NOT NULL COMMENT '',
  `desicription` VARCHAR(45) NULL COMMENT '',
  UNIQUE INDEX `name_UNIQUE` (`name` ASC)  COMMENT '',
  PRIMARY KEY (`idExperiment`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`Run`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Run` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Run` (
  `idRun` INT NOT NULL COMMENT '',
  `fileName` VARCHAR(45) NOT NULL COMMENT '',
  `condition` VARCHAR(45) NULL COMMENT 'For group comparison experiments, this column indicates groups of interest (such as “Disease” or “Control”). For time-course experiments, this column indicates time points (such as “T1”, “T2”, etc).',
  `bioReplicate` VARCHAR(45) NULL COMMENT 'This column should contain a unique identifier for each biological replicate in the experiment. For example, in a clinical proteomic investigation this should be a unique patient id. Patients from distinct groups should have distinct ids.',
  `Experiment_idExperiment` INT NOT NULL COMMENT '',
  PRIMARY KEY (`Experiment_idExperiment`, `idRun`)  COMMENT '',
  INDEX `fk_Run_Experiment1_idx` (`Experiment_idExperiment` ASC)  COMMENT '',
  UNIQUE INDEX `fileName_UNIQUE` (`fileName` ASC)  COMMENT '',
  CONSTRAINT `fk_Run_Experiment1`
    FOREIGN KEY (`Experiment_idExperiment`)
    REFERENCES `LFQDB`.`Experiment` (`idExperiment`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`QuantProtein`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`QuantProtein` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`QuantProtein` (
  `idQuantProtein` INT NOT NULL COMMENT '',
  `area` DOUBLE NULL COMMENT '',
  `intensity` DOUBLE NULL COMMENT '',
  `signalToNoise` DOUBLE NULL COMMENT '',
  `Protein_idProtein` INT NOT NULL COMMENT '',
  `Run_Experiment_idExperiment` INT NOT NULL COMMENT '',
  `Run_idRun` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idQuantProtein`, `Protein_idProtein`, `Run_Experiment_idExperiment`, `Run_idRun`)  COMMENT '',
  INDEX `fk_QuantProtein_Protein1_idx` (`Protein_idProtein` ASC)  COMMENT '',
  INDEX `fk_QuantProtein_Run1_idx` (`Run_Experiment_idExperiment` ASC, `Run_idRun` ASC)  COMMENT '',
  CONSTRAINT `fk_QuantProtein_Protein1`
    FOREIGN KEY (`Protein_idProtein`)
    REFERENCES `LFQDB`.`Protein` (`idProtein`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_QuantProtein_Run1`
    FOREIGN KEY (`Run_Experiment_idExperiment` , `Run_idRun`)
    REFERENCES `LFQDB`.`Run` (`Experiment_idExperiment` , `idRun`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`Peptide`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Peptide` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Peptide` (
  `idPeptide` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT '',
  `mz` DOUBLE NULL COMMENT '',
  `iRT` DOUBLE NULL COMMENT '',
  `strippedSequence` VARCHAR(45) NULL COMMENT 'The stripped amino acid sequence of the peptide excluding any modifications. Please only use the single letter code for the 20 standard proteinogenic amino acids.',
  `modifiedSequence` VARCHAR(45) NULL COMMENT 'In case your peptide is modified use this column to specify the amino acid sequence including modifications. The modified sequence should be constant for one unique precursor. This Page 18 of 33 information is used for labelling your precursors in Spectronaut™ and automatically generating a unique ID if necessary. The modified sequence is not used for fragment calculation but only for grouping and displaying purposes. The actual content can therefore be in any desired format (e.g. _[ac]M[ox]AGILC[CAM]K_).',
  `score` VARCHAR(45) NULL COMMENT '',
  `scoreType` VARCHAR(45) NULL COMMENT '',
  PRIMARY KEY (`idPeptide`)  COMMENT '')
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`QuantPeptide`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`QuantPeptide` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`QuantPeptide` (
  `idQuantPeptide` INT NOT NULL COMMENT '',
  `mz` DOUBLE NULL COMMENT '',
  `rt` DOUBLE NULL COMMENT '',
  `area` DOUBLE NULL COMMENT '',
  `intensity` DOUBLE NULL COMMENT '',
  `QuantProtein_idQuantProtein` INT NULL COMMENT '',
  `Peptide_idPeptide` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idQuantPeptide`, `Peptide_idPeptide`)  COMMENT '',
  INDEX `fk_QuantPeptide_QuantProtein1_idx` (`QuantProtein_idQuantProtein` ASC)  COMMENT '',
  INDEX `fk_QuantPeptide_Peptide1_idx` (`Peptide_idPeptide` ASC)  COMMENT '')
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `LFQDB`.`Precursor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Precursor` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Precursor` (
  `idPrecursor` INT NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL COMMENT '',
  `mz` DOUBLE NULL COMMENT '',
  `charge` INT NULL COMMENT '',
  `Peptide_idPeptide` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idPrecursor`)  COMMENT '',
  INDEX `fk_Precursor_Peptide1_idx` (`Peptide_idPeptide` ASC)  COMMENT '')
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `LFQDB`.`QuantPrecursorDIA`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`QuantPrecursorDIA` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`QuantPrecursorDIA` (
  `idQuantPrecursorDIA` INT NOT NULL COMMENT 'Values derived from transitions\n',
  `rt` DOUBLE NULL COMMENT 'Average / re median RT of fragments (derived information)\n',
  `area` DOUBLE NULL COMMENT 'Area derived from MS2',
  `intensity` DOUBLE NULL COMMENT 'Intensity derived from MS2\n',
  `cScore` DOUBLE NULL COMMENT '',
  `qValue` DOUBLE NULL COMMENT '',
  `signalToNoise` VARCHAR(45) NULL COMMENT '',
  `QuantPeptide_idQuantPeptide` INT NOT NULL COMMENT '',
  `Precursor_idPrecursor` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idQuantPrecursorDIA`, `QuantPeptide_idQuantPeptide`, `Precursor_idPrecursor`)  COMMENT '',
  INDEX `fk_QuantPrecursorMS2_QuantPeptide1_idx` (`QuantPeptide_idQuantPeptide` ASC)  COMMENT '',
  INDEX `fk_QuantPrecursorDIA_Precursor1_idx` (`Precursor_idPrecursor` ASC)  COMMENT '',
  CONSTRAINT `fk_QuantPrecursorMS2_QuantPeptide1`
    FOREIGN KEY (`QuantPeptide_idQuantPeptide`)
    REFERENCES `LFQDB`.`QuantPeptide` (`idQuantPeptide`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_QuantPrecursorDIA_Precursor1`
    FOREIGN KEY (`Precursor_idPrecursor`)
    REFERENCES `LFQDB`.`Precursor` (`idPrecursor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`Fragment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`Fragment` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`Fragment` (
  `idSpectraLibraryFragment` INT NOT NULL COMMENT 'Allows you to specify the fragment loss-type (e.g. NH3 or H2O). This is mainly used for labelling your fragment ions in plots.',
  `mz` DOUBLE NULL COMMENT '',
  `mzPredicted` VARCHAR(45) NULL COMMENT 'predicted mass - theoretical mass',
  `charge` INT NULL COMMENT '',
  `relativeIntensity` DOUBLE NULL COMMENT 'The relative peptide fragment ion intensity expressed as a percentage of the most intense fragment ion.',
  `fragmentType` VARCHAR(45) NULL COMMENT 'The peptide fragment ion type. Usually this is “y” or “b”.',
  `fragmentNumber` INT NULL COMMENT 'The peptide fragment ion number. This number should be between 1 and the length of your peptide in amino acids minus one.',
  `losstype` VARCHAR(45) NULL COMMENT 'Allows you to specify the fragment loss-type (e.g. NH3 or H2O).',
  `excludeFromQuantification` TINYINT(1) NULL COMMENT '',
  `Precursor_idPrecursor` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idSpectraLibraryFragment`, `Precursor_idPrecursor`)  COMMENT '',
  INDEX `fk_SpectraLibraryFragment_Precursor1_idx` (`Precursor_idPrecursor` ASC)  COMMENT '',
  CONSTRAINT `fk_SpectraLibraryFragment_Precursor1`
    FOREIGN KEY (`Precursor_idPrecursor`)
    REFERENCES `LFQDB`.`Precursor` (`idPrecursor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`QuantFragments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`QuantFragments` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`QuantFragments` (
  `idQuantFragment` VARCHAR(45) NOT NULL COMMENT '',
  `mz` DOUBLE NULL COMMENT '',
  `rt` DOUBLE NULL COMMENT '',
  `area` DOUBLE NULL COMMENT '',
  `intensity` DOUBLE NULL COMMENT '',
  `interference` DOUBLE NULL COMMENT '',
  `signalToNoise` DOUBLE NULL COMMENT '',
  `QuantPrecursorDIA_idQuantPrecursorDIA` INT NOT NULL COMMENT '',
  `Fragment_idSpectraLibraryFragment` INT NOT NULL COMMENT '',
  `Fragment_Precursor_idPrecursor` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idQuantFragment`, `QuantPrecursorDIA_idQuantPrecursorDIA`, `Fragment_idSpectraLibraryFragment`, `Fragment_Precursor_idPrecursor`)  COMMENT '',
  INDEX `fk_QuantFragments_QuantPrecursorDIA1_idx` (`QuantPrecursorDIA_idQuantPrecursorDIA` ASC)  COMMENT '',
  INDEX `fk_QuantFragments_Fragment1_idx` (`Fragment_idSpectraLibraryFragment` ASC, `Fragment_Precursor_idPrecursor` ASC)  COMMENT '',
  CONSTRAINT `fk_QuantFragments_QuantPrecursorDIA1`
    FOREIGN KEY (`QuantPrecursorDIA_idQuantPrecursorDIA`)
    REFERENCES `LFQDB`.`QuantPrecursorDIA` (`idQuantPrecursorDIA`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_QuantFragments_Fragment1`
    FOREIGN KEY (`Fragment_idSpectraLibraryFragment` , `Fragment_Precursor_idPrecursor`)
    REFERENCES `LFQDB`.`Fragment` (`idSpectraLibraryFragment` , `Precursor_idPrecursor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`QuantPrecursorLFQ`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`QuantPrecursorLFQ` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`QuantPrecursorLFQ` (
  `idQuantPrecursorMS1` INT NOT NULL COMMENT '',
  `rt` DOUBLE NULL COMMENT '',
  `mz` DOUBLE NULL COMMENT '',
  `area` DOUBLE NULL COMMENT '',
  `intensity` DOUBLE NULL COMMENT '',
  `signalToNoise` DOUBLE NULL COMMENT '',
  `QuantPeptide_idQuantPeptide` INT NOT NULL COMMENT '',
  `Precursor_idPrecursor` INT NOT NULL COMMENT '',
  PRIMARY KEY (`idQuantPrecursorMS1`, `QuantPeptide_idQuantPeptide`, `Precursor_idPrecursor`)  COMMENT '',
  INDEX `fk_QuantPrecursorMS1_QuantPeptide1_idx` (`QuantPeptide_idQuantPeptide` ASC)  COMMENT '',
  INDEX `fk_QuantPrecursorLFQ_Precursor1_idx` (`Precursor_idPrecursor` ASC)  COMMENT '',
  CONSTRAINT `fk_QuantPrecursorMS1_QuantPeptide1`
    FOREIGN KEY (`QuantPeptide_idQuantPeptide`)
    REFERENCES `LFQDB`.`QuantPeptide` (`idQuantPeptide`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_QuantPrecursorLFQ_Precursor1`
    FOREIGN KEY (`Precursor_idPrecursor`)
    REFERENCES `LFQDB`.`Precursor` (`idPrecursor`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LFQDB`.`ProteinPeptide`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `LFQDB`.`ProteinPeptide` ;

CREATE TABLE IF NOT EXISTS `LFQDB`.`ProteinPeptide` (
  `Peptide_idPeptide` INT NOT NULL COMMENT '',
  `ProteinInformation_idProtein` INT NOT NULL COMMENT '',
  PRIMARY KEY (`Peptide_idPeptide`, `ProteinInformation_idProtein`)  COMMENT '',
  INDEX `fk_Peptide_has_ProteinInformation1_ProteinInformation1_idx` (`ProteinInformation_idProtein` ASC)  COMMENT '',
  INDEX `fk_Peptide_has_ProteinInformation1_Peptide1_idx` (`Peptide_idPeptide` ASC)  COMMENT '',
  CONSTRAINT `fk_Peptide_has_ProteinInformation1_Peptide1`
    FOREIGN KEY (`Peptide_idPeptide`)
    REFERENCES `LFQDB`.`Peptide` (`idPeptide`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Peptide_has_ProteinInformation1_ProteinInformation1`
    FOREIGN KEY (`ProteinInformation_idProtein`)
    REFERENCES `LFQDB`.`Protein` (`idProtein`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
