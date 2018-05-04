import os
import csv

def file_names_publ():
    for f in os.listdir("data/"):
        if not "publ_" in f: continue
        yield f

def row_to_stats(row):
    return [0, 1, 2]

for file_name in file_names_publ():
    print(file_name)

    file_h = open("data/" + file_name, "r")
    csv_reader = csv.reader(file_h)

    file_stats_h = open("data/stats_" + file_name, "w")
    csv_writer = csv.writer(file_stats_h)

    for row in csv_reader:
        csv_writer.writerow(row_to_stats(row))

    file_h.close()
    file_stats_h.close()
