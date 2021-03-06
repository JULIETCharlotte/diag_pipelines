import pandas
import re
import csv
from collections import defaultdict

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]



dist = csv.reader(open(snakemake.input[0]), delimiter=' ')
ref = snakemake.wildcards["core_genome_or_full_genome"]
all_samples = snakemake.params["samples"]
all_samples.sort(key=natural_keys)


matrix_distances = pandas.DataFrame(0, index=all_samples + [ref], columns = all_samples + [ref])

for i in dist:
    if i[0]=="ref":
        matrix_distances.loc[ref, i[1]] = int(i[2])
        matrix_distances.loc[i[1], ref] = int(i[2])
    else:
        matrix_distances.loc[i[0], i[1]] = int(i[2])
        matrix_distances.loc[i[1], i[0]] = int(i[2])




out_xlsx_distances = snakemake.output["out_xlsx_distance"]
writer = pandas.ExcelWriter(out_xlsx_distances)
matrix_distances.to_excel(writer, snakemake.wildcards["distance_type"], index=True)
writer.save()

matrix_distances.to_csv(snakemake.output["out_tsv_distance"], sep="\t", index=True)
