import csv

def get_specnaut_mappings(file_name):
    with open(file_name, 'rU') as csv_file:
        csv_in = csv.reader(csv_file)
        mappings = {}

        for row in csv_in:
            str_split_res = str.split(row[0], "_")
            if len(str_split_res) == 2:
                #print "{} {}".format(str_split_res[0], str_split_res[1])
                if str_split_res[0] not in mappings:
                    mappings[str_split_res[0]] = {str_split_res[1]: row[1]}
                else:
                    mappings[str_split_res[0]].update({str_split_res[1]: row[1]})
        return mappings

if __name__ == "__main__":
    res = get_specnaut_mappings("MappingSpectronaut.csv")
