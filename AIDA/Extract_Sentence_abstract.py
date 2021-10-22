# This program processes text from a scientific paper and identifies and extracts the core claims from the paper.
# The core and non-core word lists can be manually adjusted as well as the score values.
# The program requires a text file or a directory of text files containing the text from research papers as input. Therafter, the results for each file is stored in a .csv file 
# The code is written in Python 3.9 so ahaving a similar version or atleast Python3 is recommended.

# Assumptions
# The scores assigned to sentences are based on research conducted by authors and we assume them to be accurately represented
# -*- coding: utf-8 -*-
# Import the required libraries

import nltk, re, csv, os

nltk.data.path.append(r"knowledge-management/NLTK_data")

from nltk.corpus import stopwords
from collections import Counter
from difflib import SequenceMatcher


def check_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


dirname = os.path.dirname(__file__)
sent_path = os.path.join(dirname, '../nltk_data/tokenizers/punkt/english.pickle')
sent_detector = nltk.data.load(sent_path)

# Define core and non-core words

core_words = ["highlight", "constitute", "suggest", "indicate", "demonstrate", "show", "reveal", "provide",
              "illustrate", "describe", "conclude", "support", "establish", "propose", "advocate", "determine",
              "confirm", "argue", "imply", "display", "offer", "highlights", "constitutes", "suggests", "indicates",
              "demonstrates", "shows", "reveals", "provides", "illustrates", "describes", "concludes", "supports",
              "establishes", "proposes", "advocates", "determines", "confirms", "argues", "implies", "displays",
              "offers", "underlines", "underline", "underlined", "overall", "sum", "therefore", "thus", "together",
              "conclusion", "collectively", "altogether", "conclude", "conclusively", "consequently", "study",
              "extracted_conclusions", "findings", "research", "report", "data", "paper", "observations", "experiment", "publication",
              "analysis"]

non_core_words = ["sought", "addition", "well-replicated", "replicated", "sample", "aimed", "aims", "questionnaire",
                  "survey", "based", "interviews", "cross-sectional", "participants", "descriptive", "CI ", "%",
                  "interview", "participant", "cc by 3.0", "previously"]


# Function that seperates all the lines and creates a list of the most frequent words in the provided text
# # Parameter - utf8 encoding, English stop words
# Input - Text and path of text
# Output - Tokenised sentences and list of frequent words
# Dependencies on functions - Output is used by assign_sentences_score(). Nested call in extract_sentences().


def determine_lines_and_frequent_words(conclusions, path):
    lines = sent_detector.tokenize(conclusions)
    text = open(path, encoding="utf8")
    
    body_text = ''
    for line in text:
        body_text += line

    base_words = nltk.tokenize.casual.casual_tokenize(body_text.lower())
    english_stopwords = stopwords.words('english')
    words = [word for word in base_words if word not in english_stopwords]
    counts = Counter(words)

    frequent_words = []
    for word, count in counts.most_common(10):
        frequent_words.append(word)
    return lines, frequent_words


# This function assigns every sentence with a score based on some criteria - key phrases, core words, frequent words, non-core words, and sentence length
# Parameters -  Score for key phrases, core words, frequent words, non-core words, and sentence length
# Input - List of tokenized sentences, list of frequent words
# Output -  Dictionary of sentences with assigned scores
# Dependencies on functions - Input received by calling determine_lines_and_frequent_words(). Output is used by extract_sentences_above_threshold() or go_over_sentences(). Nested call in extract_sentences().
def assign_sentences_score(lines, frequent_words):
    sentences = {}
    for line in lines:
        score = 0
        words = nltk.tokenize.casual.casual_tokenize(line)
        words = [word for word in words if word != '[' or ']']
        searchObj = re.search(
            r'(overall|in sum|therefore|thus|together|in conclusion|concluding|taken together|collectively|altogether|taken collectively|to conclude|conclusively|all together|all things considered|everything considered|as a result|consequently|conclusion|thus|as expressed)*.*(the|these|this|the present|our)*(study|extracted_conclusions|findings|research|report|data|observation|experiment|publication|analysis|data set|we)+.*(highlight|constitute|suggest|indicate|demonstrate|show|reveal|provide|illustrate|describe|conclude|support|establish|propose|advocate|determine|confirm|argue|impl|display|offer|underline|allow|found|find)+',
            line, re.I)
        if searchObj != None:
            score += 25
        for word in words:
            if word.lower() in core_words and line.count(word) == 1:
                score += 10
            if word.lower() in frequent_words and line.count(word) == 1:
                score += 5
            if word.lower() in non_core_words:
                score -= 5
        if len(line) >= 400:
            score -= 50
        sentences[line] = score
    return sentences


# In some cases, two sentences end up with the same score, in such a case an extra check is performed to make sure only one sentence is chosen in the end by adding a score for sentences that have less frequent words
# Parameter - Size of the list with less frequent words
# Input - Sentences that have the same score and list of frequent words
# Output - Candidate sentences that are updated with new scores
# Dependencies on functions - Conditionally called by go_over_sentences(). Indirectly called in extract_sentences().
def perform_extra_check(candidate_sentences, frequent_words):
    less_frequent_words = frequent_words[:5]
    sentences = {}
    for sentence in candidate_sentences:
        score = 0
        words = nltk.tokenize.casual.casual_tokenize(sentence)
        for word in words:
            if word in less_frequent_words:
                score += 1
        sentences[sentence] = score
    return sentences


# When all the sentences have an assigned score, this function goes over all the sentences and picks the sentence(s) with the highest score
# Input - Dictionary of sentences with scores assigned, threshold value to pick sentences that have a score above it
# Output -  Core sentences
# Parameter - threshold
# Dependencies on functions - Input received by calling assign_sentences_score(). Nested call in extract_sentences().
def extract_sentences_above_threshold(sentences, threshold):
    candidate_sentences = []
    for sentence, score in sentences.items():
        if score >= threshold:
            candidate_sentences.append(sentence)
    return candidate_sentences

#If a threshold is not decided, the function iterates over all sentences and identifies sentences with highest scores. If the candidate sentences have the same score, an extra check is performed to narrow down to one sentence.
# Input - Dictionary of sentences with scores assigned, threshold value to pick sentences that have a score above it
# Output -  Core sentence
# Parameter - Size of the list with less frequent words
# Dependencies on functions - Input received by calling assign_sentences_score(). Conditionally calls perform_extra_check(). Nested call in extract_sentences().
def go_over_sentences(sentences, frequent_words):
    scores = sentences.values()
    highest_score = max(scores)
    core_sentence_counter = 0
    candidate_sentences = []
    for sentence, score in sentences.items():
        if score == highest_score:
            core_sentence_counter += 1
    for sentence, score in sentences.items():
        if score == highest_score and core_sentence_counter == 1:
            core_sentence = sentence
        if score == highest_score and core_sentence_counter > 1:
            candidate_sentences.append(sentence)
    if candidate_sentences:
        less_frequent_words = frequent_words[:5]
        sentences = perform_extra_check(candidate_sentences, less_frequent_words)
        scores = sentences.values()
        highest_score = max(scores)
        for sentence, score in sentences.items():
            if score == highest_score:
                core_sentence = sentence
    return core_sentence

# Opens the directory with all the files with conclusions and calls all functions required to score and extract sentences.
# The results are written and saved in a .csv file
# directory: Provide the directory here with all the articles that should be processed
# Parameter - utf8 encoding
# Input - Directory, output path, and threshold value
# Output - CSV file with extracted sentences for each file
# Dependencies on functions - Calls the following functions - determine_lines_and_frequent_words, assign_sentences_score, extract_sentences_above_threshold, go_over_sentences. Indirectly may call perform_extra_check.
def extract_sentences(directory=r'original3_Conclusions', output_path='AIDA_example_articles/extracted_conclusions/results_conclusion.csv',
                      threshold=None):
    csv_file = open(output_path, 'w')

    fieldnames = ['File', 'Sentence']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()
    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        text = open(path, encoding="utf8")
  
        conclusions = ''

        for line in text:    
            conclusions += line
            

        lines, frequent_words = determine_lines_and_frequent_words(conclusions, path)
        sentences = assign_sentences_score(lines, frequent_words)
        if threshold is not None:
            core_sentences=extract_sentences_above_threshold(sentences, threshold)
        else:
            core_sentence = go_over_sentences(sentences, frequent_words)
            core_sentences=[core_sentence]
        core_sentences = map(lambda s: s.replace('\n', ' ').replace(';', ','), core_sentences)
        
        for sentence in core_sentences: writer.writerow({'File': file, 'Sentence': sentence})
