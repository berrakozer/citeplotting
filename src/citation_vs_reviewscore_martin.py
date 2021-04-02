# Import section
import sys
import os
import glob
import openpyxl
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from pathlib import Path

# Input section
FILE_EXT = '.csv'

# ---------------------------------------------------------------------------

def xlsx_reader(file):
    # Load the workbook, i.e. .xlsx file.
    wb = openpyxl.load_workbook(file)

    # Activate the worksheet of the workbook.
    ws = wb.active

    # Read the data into a list.
    # Each row in the worksheet is read into a tuple of strings.
    data = list(ws.iter_rows(values_only=True))

    return data
    # End of function.

def csv_reader(file):
    # Open the .csv file and put the lines in a list.
    with open(file, mode='r', encoding='utf8') as input_file:
        data = list(csv.reader(input_file, delimiter=';'))
    input_file.close()

    return data

def xlsx_citations_scores_extracter(data):
    # Getting the header from the data list.
    header = data[0]

    # Getting the indices (columns) of the citations and review scores.
    for i in range(0, len(header)):
        if 'Citations' in header[i]:
            citations_index = i

        elif 'Review scores' in header[i]:
            review_scores_index = i

    # Appending citations, review scores, and raw scores into lists.
    citations, review_scores, raw_scores = [], [], []
    for i in range(1, len(data)):

        if data[i][review_scores_index] != None:
            citations.append(int(data[i][citations_index]))

            scores = data[i][review_scores_index]

            review_scores.append(float(scores.split(' ')[0]))

            # raw_scores_string = scores.split(' ')[1].strip('()').split(',')
            raw_scores_string = scores.split(' ')[1].strip('()').split(',')

            raw_scores_int = []
            for j in range(0, len(raw_scores_string)):
                raw_scores_int.append(int(raw_scores_string[j]))

            raw_scores.append(raw_scores_int)

    citations_scores = []
    citations_scores.append(citations)
    citations_scores.append(review_scores)
    citations_scores.append(raw_scores)

    return citations_scores
    # End of function.

def csv_citations_scores_extracter(data):
    # Getting the header from the data list.
    header = data[0]

    # Getting the indices (columns) of the citations and review scores.
    for i in range(0, len(header)):
        if 'Citations' in header[i]:
            citations_index = i

        elif 'Review scores' in header[i]:
            review_scores_index = i

    # Appending citations, review scores, and raw scores into lists.
    citations, review_scores, raw_scores = [], [], []
    for i in range(1, len(data)):

        # if data[i][review_scores_index] != None:
        if len(data[i][review_scores_index]) > 0:
            citations.append(int(data[i][citations_index]))

            scores = data[i][review_scores_index]

            review_scores.append(float(scores.split(' ')[0]))

            # raw_scores_string = scores.split(' ')[1].strip('()').split(',')
            raw_scores_string = scores.split(' ')[1].strip('()').split(',')

            raw_scores_int = []
            for j in range(0, len(raw_scores_string)):
                raw_scores_int.append(int(raw_scores_string[j]))

            raw_scores.append(raw_scores_int)

    citations_scores = []
    citations_scores.append(citations)
    citations_scores.append(review_scores)
    citations_scores.append(raw_scores)

    return citations_scores
    # End of function.

def citations_scores_writer(file, txtdir, citations_scores):
    citations = citations_scores[0]
    review_scores = citations_scores[1]
    raw_scores = citations_scores[2]

    # Appending string elements to list for .txt export.
    txt = []
    txt.append('Citations\tReview scores\tRaw scores\n')
    for i in range(0, len(citations)):
        txt.append(str(citations[i]) + ('\t')*2 + str(review_scores[i]) + ('\t')*2)
        for j in range(0, len(raw_scores[i])-1):
            txt.append(str(raw_scores[i][j]) + ', ')
        txt.append(str(raw_scores[i][-1]))
        txt.append('\n')

    # Writing the .txt file.
    txt_filename = str(Path(file).stem) + '.txt'
    with open(txtdir / txt_filename, 'w') as output_file:
        output_file.writelines(txt)
    output_file.close()

    return None
    # End of function.

def citations_scores_plotter(file, pngdir, pdfdir, citations_scores):
    citations = citations_scores[0]
    review_scores = citations_scores[1]
    raw_scores = citations_scores[2]

    # Make figure.
    fig_size = (12,4)
    fig, ax = plt.subplots(dpi=300, figsize=fig_size)

    billinge_blue = '#0B3C5D'
    billinge_red = '#B82601'
    billinge_green = '#1c6b0a'
    billinge_lightblue = '#328CC1'
    billinge_darkblue = '#062F4F'
    billinge_yellow = '#D9B310'
    billinge_darkred = '#984B43'
    billinge_bordeaux = '#76323F'
    billinge_olivegreen = '#626E60'
    billinge_yellowgrey = '#AB987A'
    billinge_brownorange = '#C09F80'

    # Make scatter plot.
    ax.scatter(citations, review_scores, s=3, c=billinge_blue)

    # Make axes labels.
    ax.set_xlabel("Citations")
    ax.set_ylabel("Review Score")

    # Set axes limits.
    min_citations = min(citations)
    max_citations = max(citations)
    range_citations = max_citations - min_citations

    min_review_scores = min(review_scores)
    max_review_scores = max(review_scores)
    range_review_scores = max_review_scores - min_review_scores

    aspect_ratio = fig_size[0]/fig_size[1]
    offset = 0.01
    ax.set_xlim([min_citations-offset*range_citations, max_citations+offset*range_citations])
    ax.set_ylim([min_review_scores-aspect_ratio*offset*range_review_scores, max_review_scores+aspect_ratio*offset*range_review_scores])

    # Set axes ticks.
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(2))

    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))

    # Save figure.
    png_filename = str(Path(file).stem) + '.png'
    pdf_filename = str(Path(file).stem) + '.pdf'
    plt.savefig(pngdir / png_filename, bbox_inches='tight')
    plt.savefig(pdfdir / pdf_filename, bbox_inches='tight')

    # Show plot
    # plt.show()

    # Close close.
    plt.close()

    return None
    # End of function.

def main():
    # File extension for files we want to load.
    # file_ext = '.xlsx'

    # Source and data directories.
    srcdir = Path.cwd()
    parentdir = srcdir.resolve().parent
    datadir = parentdir / 'data'

    # List of files with the extension that we want to process.
    file_list = glob.glob(str(datadir) + '/**' + FILE_EXT)

    # Folders (subdirectories) for plots and .txt file(s).
    pngdir = srcdir / 'png'
    pdfdir = srcdir / 'pdf'
    txtdir = srcdir / 'txt'

    folders = [pngdir, pdfdir, txtdir]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for file in file_list:
        if FILE_EXT == '.xlsx':
            data = xlsx_reader(file)
            citations_scores = xlsx_citations_scores_extracter(data)
            txtfile = citations_scores_writer(file, txtdir, citations_scores)
            plot = citations_scores_plotter(file, pngdir, pdfdir, citations_scores)

        elif FILE_EXT == '.csv':
            data = csv_reader(file)
            citations_scores = csv_citations_scores_extracter(data)
            txtfile = citations_scores_writer(file, txtdir, citations_scores)
            plot = citations_scores_plotter(file, pngdir, pdfdir, citations_scores)

    return None
    # End of function.

if __name__ == "__main__":
    main()

# End of file.
