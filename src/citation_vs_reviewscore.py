#import section
import csv
import os
import sys
import matplotlib.pyplot as plt
from pathlib import Path
#---------------------------------------------------------
#input section
INPUT_FILE_NAME = 'acta_a_citations_review_scores_utf8.csv'

#---------------------------------------------------------


src_path = Path.cwd()
parent_path = src_path.resolve().parent
data_path = parent_path / 'data'

file_path = data_path / INPUT_FILE_NAME

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
        review_scores.append(float(data[i][review_scores_index].split()[0]))
        #print(review_scores)
        #sys.exit()
#print(type(data[1][review_scores_index]))
#print(len(review_scores),len(citations))

plt.xlim(1,5)
plt.ylim(0,145)
plt.scatter(review_scores, citations)
plt.show()



