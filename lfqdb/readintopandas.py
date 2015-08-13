import pandas as pd
from getSpecnautMappings import get_specnaut_mappings
import lfqdb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

def get_column_mappings(mappings, table_name, df_prot_id):
    '''
    :param table_name:
    :param df_prot_id:
    :return:
    '''
    column_mappings = {}
    for key, value in mappings[table_name].iteritems():
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

def experimentGenrator(row_map):
    return lfqdb.Experiment(**row_map)

def runGenerator(row_map):
    return lfqdb.Run(**row_map)

def proteinGenerator(row_map):
    return lfqdb.Protein(**row_map)

def peptideGenerator(row_map):
    return lfqdb.Peptide(**row_map)

def precursorGenerator(row_map):
    return lfqdb.Precursor(**row_map)

def fragmentGenerator(row_map):
    return lfqdb.Fragment(**row_map)

def quantPrecursorDiaGenerator(row_map):
    return lfqdb.QuantPrecursorDIA(**row_map)

def quantPrecursorLFQGenerator(row_map):
    return lfqdb.QuantPrecursorLFQ(**row_map)

def quantFragmentGenerator(row_map):
    return lfqdb.QuantFragment(**row_map)


def generatorFactory(name):
    if name == "Experiment":
        return experimentGenrator
    elif name == "Run":
        return runGenerator
    elif name == "Protein":
        return proteinGenerator
    elif name == "Peptide":
        return peptideGenerator
    elif name == "Precursor":
        return precursorGenerator
    elif name == "Fragment":
        return fragmentGenerator
    elif name == "QuantPrecursorDIA":
        return quantPrecursorDiaGenerator
    elif name == "QuantPrecursorLFQ":
        return quantPrecursorLFQGenerator
    elif name == "QuantFragment":
        return quantFragmentGenerator
    else :
        print "No such ting"

def insertDataIntoTable(insert_set, tableRowGenerator, session):
    rows = []
    for row_map in insert_set:
        tablerow = tableRowGenerator(row_map)
        session.add(tablerow)
        rows.append(tablerow)
    # with this the id's of the object are updated
    session.flush()

    rowsWithIDs = [x.__dict__ for x in rows]
    rowsWithIDs = pd.DataFrame(rowsWithIDs)
    rowsWithIDs.drop('_sa_instance_state',axis=1,inplace=True)
    return rowsWithIDs

def setUpSession():
    engine = create_engine('sqlite:///lfqdb.db')
    lfqdb.Base.metadata.drop_all(engine)
    lfqdb.Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = setUpSession()

    #df = pd.read_table('/Users/witold/prog/imsbInfer/playground/20150811_131108_p1503_Sham_VS_Transection_Report.xls',header=0)
    #df.to_hdf("testdata.hdf5",'table',append=False)

    df = pd.read_hdf("testdata.hdf5",'table')
    # cick out decoys.
    # remove decoys
    dfProtID = df[df['PG.ProteinGroupID'] != 'n. def.']
    mappings = get_specnaut_mappings("../MappingSpectronaut.csv")
    table_filling_order = ["Experiment", "Run", "Protein", "Peptide", "Precursor", "QuantPeptide", "Precursor", "Fragment"]

    def insertInto(columns, tablename, data, session):
        insert_set = convert_to_insertset(columns, data)
        generator = generatorFactory(tablename)
        exper = insertDataIntoTable(insert_set, generator, session)
        data = pd.merge(left = data, right= exper, left_on =columns.values(), right_on=columns.keys(),copy=False)
        return data

    columns = get_column_mappings(mappings, "Experiment", dfProtID)
    dfExp = insertInto(columns, "Experiment", dfProtID,session)

    columns = get_column_mappings(mappings, "Run" , dfProtID)
    columns['idExperiment'] = 'idExperiment'
    dfRun = insertInto(columns, "Run", dfExp, session)

    #
    columns = get_column_mappings(mappings,"Protein", dfProtID)
    dfProtein = insertInto(columns, "Protein", dfRun, session)

    columns = get_column_mappings(mappings,"Peptide", dfProtID)
    columns['idProtein'] = 'idProtein'
    dfPeptide = insertInto(columns, "Peptide", dfProtein, session)

    columns = get_column_mappings(mappings,"Precursor", dfPeptide)
    columns['idPeptide'] = 'idPeptide'
    dfPeptide = insertInto(columns, "Precursor", dfPeptide, session)

    columns = get_column_mappings(mappings,"Fragment", dfPeptide)
    columns['idPrecursor'] = 'idPrecursor'
    dfFragment = insertInto(columns, "Fragment", dfPeptide, session)

    columns = get_column_mappings(mappings,"QuantPrecursorDIA", dfFragment)
    columns['idPrecursor'] = 'idPrecursor'
    columns['idRun'] = 'idRun'
    dfFragment = insertInto(columns, "QuantPrecursorDIA", dfFragment, session)

    columns = get_column_mappings(mappings,"QuantPrecursorLFQ", dfFragment)
    columns['idPrecursor'] = 'idPrecursor'
    columns['idRun'] = 'idRun'
    dfFragment = insertInto(columns, "QuantPrecursorLFQ", dfFragment, session)

    columns = get_column_mappings(mappings,"QuantFragment",dfFragment)
    columns['idFragment'] = 'idFragment'
    columns['idRun'] = 'idRun'
    dfFragment = insertInto(columns, "QuantFragment", dfFragment, session)

    session.commit()

