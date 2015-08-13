__author__ = 'witold'

from sqlalchemy import Table, Column, Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Protein(Base):
    __tablename__ = "Protein"
    idProtein = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    houseKeeping = Column(Integer)

class Peptide(Base):
    __tablename__ = "Peptide"
    idPeptide = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    mz = Column(Numeric)
    iRT = Column(Numeric)
    strippedSequence = Column(String)
    modifiedSequence = Column(String)
    score = Column(Numeric) # identification score i.e. peptideProphet
    scoreType = Column(Integer)
    idProtein = Column(Integer,ForeignKey(Protein.idProtein)) # idiotset

class ProteinPeptideAssociation(Base):
    __tablename__= "ProteinPeptideAssociation"
    ProteinPeptideAssociation = Column(Integer, primary_key=True, autoincrement=True)
    idPeptide = Column(Integer, ForeignKey(Peptide.idPeptide), primary_key=True)
    idProtein = Column(Integer, ForeignKey(Protein.idProtein), primary_key=True)

class Precursor(Base):
    __tablename__ = "Precursor"
    idPrecursor = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String)
    mz = Column(Numeric)
    charge = Column(Integer)
    idPeptide = Column(Integer,ForeignKey(Peptide.idPeptide))

class Fragment(Base):
    __tablename__ = "Fragment"
    idFragment = Column(Integer, primary_key=True, autoincrement=True)
    mz = Column(Numeric)
    mzPredicted = Column(Numeric)
    charge = Column(Integer)
    relativeIntensity = Column(Numeric)
    fragmentType = Column(String(1))
    fragmentNumber = Column(Integer)
    lossType = Column(String)
    excludeFromQuantification = Column(Integer)
    idPrecursor = Column(Integer, ForeignKey(Precursor.idPrecursor))


class Experiment(Base):
    __tablename__ = 'Experiment'
    idExperiment = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)

class Run(Base):
    __tablename__ = 'Run'
    idRun = Column(Integer, primary_key=True, autoincrement=True)
    fileName = Column(String)
    condition = Column(String)
    bioReplicate = Column(String)
    idExperiment = Column(Integer, ForeignKey(Experiment.idExperiment))

class QuantProtein(Base):
    __tablename__ = 'QuantProtein'
    idQuantProtein = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(Numeric)
    intensity = Column(Numeric)
    signalToNoise = Column(Numeric)
    idProtein = Column(Integer, ForeignKey(Protein.idProtein))
    idRun = Column(Integer, ForeignKey(Run.idRun))

class QuantPeptide(Base):
    __tablename__ = 'QuantPeptide'
    idQuantPeptide = Column(Integer, primary_key=True, autoincrement=True)
    area = Column(Numeric)
    intensity = Column(Numeric)
    signalToNoise = Column(Numeric)
    idPeptide = Column(Integer,ForeignKey(Peptide.idPeptide))
    idRun = Column(Integer, ForeignKey(Run.idRun))

class QuantPrecursorLFQ(Base):
    __tablename__ = "QuantPrecursorLFQ"
    idQuantPrecursorLFQ = Column(Integer, primary_key=True, autoincrement=True)
    rt = Column(Numeric)
    mz = Column(Numeric)
    area = Column(Numeric)
    intensity = Column(Numeric)
    signalToNoise = Column(Numeric)
    idPrecursor = Column(Integer, ForeignKey(Precursor.idPrecursor))
    idRun = Column(Integer, ForeignKey(Run.idRun))

class QuantPrecursorDIA(Base):
    __tablename__ = "QuantPrecursorDIA"
    idQuantPrecursorDIA = Column(Integer, primary_key=True, autoincrement=True)
    rt = Column(Numeric)
    area = Column(Numeric)
    intensity = Column(Numeric)
    cScore = Column(Numeric)
    qValue = Column(Numeric)
    signalToNoise = Column(Numeric)
    idPrecursor = Column(Integer, ForeignKey(Precursor.idPrecursor))
    idRun = Column(Integer, ForeignKey(Run.idRun))

class QuantFragment(Base):
    __tablename__="QuantFragment"
    idQuantFragment = Column(Integer, primary_key=True, autoincrement=True)
    mz = Column(Integer)
    rt = Column(Numeric)
    area = Column(Numeric)
    intensity = Column(Numeric)
    interference = Column(Numeric)
    signalToNoise = Column(Numeric)
    idFragment = Column(Integer, ForeignKey(Fragment.idFragment))
    idRun = Column(Integer, ForeignKey(Run.idRun))

