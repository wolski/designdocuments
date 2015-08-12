import pandas as pd
from getSpecnautMappings import get_specnaut_mappings
import lfqdb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import itertools

def get_column_mappings(table_name, df_prot_id):
    '''
    :param table_name:
    :param df_prot_id:
    :return:
    '''
    column_mappings = {}
    for key, value in mappings[table_name].iteritems():
        print "{} {}".format(key, value)
        if value in df_prot_id:
            column_mappings[key] = value
    return column_mappings


def convert_to_insertset(columns_mappings, dataframe):
    '''
    :param columns_mappings:
    :param dataframe:
    :return:
    '''
    unique_df = dataframe[columns_mappings.values()].drop_duplicates()
    print unique_df.shape
    res = []
    for i in unique_df.index:
        row_map = {}
        for key, value in columns_mappings.iteritems():
            row_map[key] = unique_df[value].at[i]
        res.append(row_map)
    return res



#df = pd.read_table('/Users/witold/prog/imsbInfer/playground/20150811_131108_p1503_Sham_VS_Transection_Report.xls',header=0)
#df.to_hdf("testdata.hdf5",'table',append=False)

engine = create_engine('sqlite:///lfqdb.db')
lfqdb.Base.metadata.drop_all(engine)
lfqdb.Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

df = pd.read_hdf("testdata.hdf5",'table')
print(df.columns.values)

# cick out decoys.
dfProtID = df[df['PG.ProteinGroupID'] != 'n. def.']
mappings = get_specnaut_mappings("../MappingSpectronaut.csv")

table_filling_order = ["Experiment", "Run", "Protein", "Peptide", "Precursor", "QuantPeptide", "Precursor", "Fragment"]

columns = get_column_mappings("Experiment", dfProtID)
insert_set_experiment = convert_to_insertset(columns, dfProtID)

exp = []
for row_map in insert_set_experiment:
    exp.append(lfqdb.Experiment(**row_map))
    session.add(exp[0])

del insert_set_experiment
session.flush()

columns = get_column_mappings("Run", dfProtID)
insert_set_run = convert_to_insertset(columns, dfProtID)

rowidsRun = []
for element in insert_set_run:
    rowidsRun.append(df[df[mappings['Run']['fileName']]==element["fileName"]].index.tolist())


rowidsRun

columns = get_column_mappings("Protein", dfProtID)
insert_set_protein = convert_to_insertset(columns, dfProtID)



columns = get_column_mappings("Peptide", dfProtID)
insert_set_peptide = convert_to_insertset(columns, dfProtID)




idExperiment = exp[0].idExperiment
print "experiment ID ", exp[0].idExperiment


runs = []
for row_map in insert_set_run:
    row_map.update({"Experiment_idExperiment": exp[0].idExperiment})
    run = lfqdb.Run(**row_map)
    session.add(run)
    runs.append(run)
session.flush()




for row_map in insert_set_protein:
    protein = lfqdb.Protein(**row_map)
    session.add(protein)

for row_map in insert_set_peptide:
    peptide = lfqdb.Peptide(**row_map)
    session.add(peptide)


session.commit()

