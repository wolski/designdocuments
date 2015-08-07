from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import inspect

Base = automap_base()

engine = create_engine("sqlite:///lfqdb.db")
Base.prepare(engine, reflect=True)

session = Session(engine)

quant_peptide = Base.classes.QuantPeptide;
print(quant_peptide)

for i in range(1, 10):
    q1 = quant_peptide(idQuantPeptide=i, mz=100, rt=30, Peptide_idPeptide=i)
    session.add(q1)


session.commit()

