import os
import csv
import nltk

def file_names_publ():
    for f in os.listdir("data/"):
        if not "publ_" in f: continue
        yield f

def row_to_stats(line):
    row = line.split("','")
    if len(row) != 8:
        print("row has wrong number of columns, it will be skipped")
        return []

    year, month, day, publ_date, publ_num, area, title, content = row
    tokens = nltk.word_tokenize(content)
    
    verdict_result = 0
    num_references_art = 0
    num_references_bge = 0

    return [year, month, day, publ_date, area, title,
        len(content),
        verdict_result,
        num_references_art,
        num_references_bge
    ]

for file_name in file_names_publ():
    print(file_name)

    file_h = open("data/" + file_name, "r")
    #csv_reader = csv.reader(file_h, delimiter=",", quotechar="'")

    file_stats_h = open("data/stats_" + file_name, "w")
    csv_writer = csv.writer(file_stats_h)

    for line in file_h.readlines():
    #for row in csv_reader:
        csv_writer.writerow(row_to_stats(line))
        break

    file_h.close()
    file_stats_h.close()

    break
