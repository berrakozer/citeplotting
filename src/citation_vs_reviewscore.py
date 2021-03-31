import csv
import os
import sys

src_path = os.getcwd()
data_path = src_path.strip('src') + 'data/'
input_file = 'acta_a_citations_review_scores_utf8.csv'
file_path = data_path + input_file

with open(file_path,mode='r',encoding='utf-8') as file:
    data = list(csv.reader(file,delimiter=';'))
file.close()

print(type(data),len(data))
print(data[0])
