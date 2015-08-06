#script to convert schema generated with mysql workbench to sqlite3

import re

f = open("lfqdbsqlite3.sql",'w')

with open("LFQDB.sql") as fp:

    preprocess = []
    for line in fp:
        line = line.strip()
        line = line.replace("`LFQDB`.", "")
        line = line.replace("`", "")
        line = re.sub(r"COMMENT '.*'", r"", line)
        if re.match("^SET", line) is not None:
            continue
        if re.match("^USE", line) is not None:
            continue
        if re.match("CREATE SCHEMA",  line) is not None:
            continue
        if re.search(r"\)$", line) is not None:
            preprocess.append(re.sub("\)$","",line))
            preprocess.append(")")
            continue
        preprocess.append(line)

    result = []
    table_name = ""
    index_lines = []

    for line in preprocess:
        if re.match("CREATE TABLE", line) is not None:
            table_name = re.search("EXISTS ([A-Za-z]+)", line).group(1)
            print(table_name)
            index_lines =[]
        if re.search("INDEX", line) is not None:
            index_lines.append(line)
            continue
        if re.match("ENGINE", line) is not None and len(index_lines) > 0:
            newlines = ""
            for idxline in index_lines:
                idxline=idxline.strip(",")
                idxline = re.sub("\(", " ON {} (".format(table_name), idxline)
                idxline = ";\nCREATE {};".format(idxline)
                newlines += idxline
            line = newlines

        line = re.sub("ENGINE = .*;", ";", line)
        result.append(line)

    for i in range(1,len(result)):
        if result[i] == ")":
            result[i-1] = re.sub(",$", "", result[i-1])

    for line in result:
        f.write(line + "\n")
