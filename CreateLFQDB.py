__author__ = 'witold'

from sqlalchemy import Table, Column, Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProteinPeptideAssociation(Base):
    Peptide_idPeptide = Column(Integer, ForeignKey('Peptide.idPeptide'), primary_key=True)
    Protein_idProtein = Column(Integer, ForeignKey('Protein.idProtein'), primary_key=True)

class Protein(Base):
    idProtein = Column(Integer, primary_key=True)
    name = Column(String)
    houseKeeping = Column(Integer)

    def __repr__(self):
        return "<Protein(name={}, houseKeeping={})>".format(self.name, self.idProtein)

class Peptide(Base):
    idPeptide = Column(Integer, primary_key=True)
    name = Column(String)
    mz = Column(Numeric)
    iRt= Column(Numeric)
    strippedSequence = Column(String)
    modifiedSequence = Column(String)
    score = Column(Numeric)
    scoreType = Column(Integer)

class Precursor(Base):
    idPrecursor = Column(Integer, primary_key = True)
    name = Column(String)
    mz = Column(Numeric)
    charge = Column(Integer)
    Peptide_idPeptide = Column(Integer,ForeignKey('Peptide.idPeptide'))

class Fragment(Base):
    idFragment = Column(Integer, primary_key= True)
    mz = Column(Numeric)
    mzPredicted = Column(Numeric)
    charge = Column(Integer)
    relativeIntensity = Column(Numeric)
    fragmentType = Column(String(1))
    fragmentNumber = Column(Integer)
    losstype = Column(String)
    excludeFromQuantification = Column(Integer)
    Precursor_idPrecursor = Column(Integer,ForeignKey('Precursor.idPrecursor'))



# tables mapping the qunatitative experiment

class Experiment(Base):
    __tablename__ = 'Experiment'
    idExperiment = Column(Integer,primary_key=True)
    name = Column(String)
    description=Column(String)
    run = relationship("Run", backref = "parent")

class Run(Base):
    __tablename__ = 'Run'
    idRun = Column(Integer, primary_key=True)
    fileName = Column(String)
    condition = Column(String)
    bioReplicate = Column(String)
    Experiment_idExperiment = Column(Integer , ForeignKey('Experiment.idExperiment'))

class QuantProtein(Base):
    __tablename__ = 'QuantProtein'
    idQuantProtein = Column(Integer, primary_key=True)
    area = Column(Numeric)
    intensity = Column(Numeric)
    signalToNoise = Column(Numeric)
    Run_idRun = Column(Integer, ForeignKey('Run.idRun'))


class QuantPrecursorLFQ(Base):
    idQuantPrecursorLFQ = Column(Integer, primary_key=True)
    rt = Column(Numeric)
    mz = Column(Numeric)
    area = Column(Numeric)
    intensity = Column(Numeric)
    signalToNoise = Column(Numeric)
    QuantProtein_idQuantProtein = Column(Integer, ForeignKey('QuantProtein.idQuantProtein'))

class QuantPrecursorDIA(Base):
    idQuantPrecursorDIA = Column(Integer, primary_key= True)
    rt = Column(Numeric)
    area = Column(Numeric)
    intensity = Column(Numeric)
    cScore = Column(Numeric)
    qValue = Column(Numeric)
    QuantProtein_idQuantProtein = Column(Integer ,ForeignKey('QuantProtein.idQuantProtein'))


