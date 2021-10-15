import AIDA.Extract_Sentence_abstract
import os
# import nltk
# nltk.data.path.append(r"C:\Users\lukac\PycharmProjects\knowledge-management\NLTK_data")

# from AIDA.Extract_Sentence_abstract import extract_sentences

# extract_sentences(directory='AIDA/original3_Conclusions', output_path='AIDA/extracted_conclusions/results_conclusion.csv', threshold=50)

import utils

pdf_folder = r'articles/10articels_about_wether_online_vocational_education/originals'
output_folder = r'articles/10articels_about_wether_online_vocational_education/'

for file in os.listdir(pdf_folder):
    path = os.path.join(pdf_folder, file)

    pdf = open(path, 'rb')
    text=utils.pdf2text(pdf)
    asd=0
