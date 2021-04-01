import csv
import os
import matplotlib.pyplot as plt
from pathlib import Path

INPUT_FILE_NAME = 'acta_a_citations_review_scores_simon.csv'

data_path = Path('..') / 'data'
file_path = data_path / INPUT_FILE_NAME

def main():
    with open(file_path, mode='r', encoding='utf-8', errors='ignore') as file:
        data = list(csv.DictReader(file, delimiter=','))

    cites = [float(datum.get('Citations (WoS)',0)) for datum in data]
    reviewer_scores = []
    for datum in data:
        try:
            reviewer_scores.append(float(datum.get('Review scores').split()[0].strip()))
        except IndexError:
            reviewer_scores.append(0.0)

    print(cites)
    print(reviewer_scores)
    plt.xlim(1,5)
    plt.ylim(0,145)
    plt.scatter(reviewer_scores[1:], cites[1:])
    plt.show()

if __name__ == "__main__":
    main()