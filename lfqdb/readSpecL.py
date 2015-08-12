from lfqdb import Experiment, Run, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///lfqdb.db')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

exp1 = Experiment(name="test", description="the long description")
run1 = Run(fileName="c:/x/y/z.wiff", condition="failure", bioReplicate="A1", Experiment_idExperiment=exp1.idExperiment)

session.add(exp1)
session.add(run1)
session.commit()


