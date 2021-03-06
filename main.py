import os
import nltk
nltk.data.path.append(r"C:\Users\lukac\PycharmProjects\knowledge-management\NLTK_data")

import timeit
from AIDA.Extract_Sentence_abstract import extract_sentences

start = timeit.default_timer()

extract_sentences(directory=r'articles\10articels_about_wether_online_vocational_education', output_path=r'extracted_conclusions\10_vocational_conclusion.csv')

stop = timeit.default_timer()
print('Extraction Time: ', stop - start)



def half_manual_conversion():
    global start
    import utils
    pdf_folder = r'articles/10articels_about_wether_online_vocational_education/originals'
    output_folder = r'articles/10articels_about_wether_online_vocational_education/'
    for file in os.listdir(pdf_folder):
        path = os.path.join(pdf_folder, file)

        pdf = open(path, 'rb')
        text = utils.pdf2text(pdf).lower()
        beg_search_term = ''
        end_search_term = ''
        start = text.find(beg_search_term.lower())
        end = text.find(end_search_term.lower())

        with open(os.path.join(output_folder, file[:-4]), 'w') as output_text_file:
            output_text_file.write(text[start:end])






