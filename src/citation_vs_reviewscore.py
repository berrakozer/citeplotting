import csv
import os
import sys

src_path = os.getcwd()
data_path = src_path.strip('src') + 'data/'
input_file = 'acta_a_citations_review_scores_utf8.csv'
file_path = data_path + input_file

with open(file_path,mode='r',encoding='utf-8') as file:
    data = list(csv.reader(file,delimiter=';'))

header = data[0]
for i in range(0,len(header)):
    if 'citations' in header[i]:
        citation_index = i

    elif 'Citations' in header[i]:
        citation_index = i

    elif 'Review scores' in header[i]:
        review_scores_index = i

citations,review_scores  = [],[]

for i in range(1,len(data)):
    if data[i][review_scores_index] != '':
        citations.append(int(data[i][citation_index]))
        review_scores.append(data[i][review_scores_index])

print(type(data[1][review_scores_index]))
print(len(review_scores),len(citations))