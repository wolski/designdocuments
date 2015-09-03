__author__ = 'witold'


from lfqdb import Peptide, Protein
import readintopandas

session = readintopandas.setUpSessionForRead("lfqdb2.db")

print session.query(Protein).count()
print session.query(Peptide).count()

