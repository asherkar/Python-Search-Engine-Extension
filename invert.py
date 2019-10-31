#!/usr/bin/env python3
import re
import json
from porter import PorterStemmer
import math
from util import process_cacm_files
from util import fetch_stopwords


class Invert:
    f = None
    p = None
    then = None
    documents = {}
    terms = {}
    termsDictionary = {}
    vector_space_dictionary = {}

    def __init__(self):
        """
        main function of the application calls the function to create
        formatted documents object for ease of access
        """
        self.documents = self.parse_documents()

    def parse_documents(self):
        """
        main parser function
        opens the 'cacm/cacm.all' file and runs through the file
        creating and adding each document to the documents object

        :return: documents object containing formatted documents
        """
        return process_cacm_files(file_name='cacm.all')

    def create_posting_list(self, stopword_toggle, stemming_toggle):
        """
        function to go through all the documents abstracts cleaning
        and adding each term to a posting_list object and the
        term dictionary. removes all the special characters for each
        term. toggles stopwords and stemming accordingly

        Note: all terms are converted to lowercase

        :param stopword_toggle: boolean, toggles the stopword usage
        :param stemming_toggle: boolean, toggles the stemming of words
        """
        self.terms = {}
        self.termsDictionary = {}
        documents = self.documents
        stopwords = []
        if stopword_toggle:
            stopwords = fetch_stopwords()
        for doc_id, document in documents.items():
            if 'abstract' in document:
                for index, word in enumerate(document['abstract'].split(' ')):
                    word = word.rstrip().lower()

                    for a in [',', '.', '{', '}', '(', ')', ';', ':', '"', '\'']:
                        if a in word:
                            if word.index(a) == 0 or word.index(a) == len(word) - 1:
                                word = word.replace(a, '')
                    if stemming_toggle:
                        p = PorterStemmer()
                        word = p.stem(word, 0, len(word) - 1)

                    if word in stopwords:
                        continue

                    if len(word) > 0:
                        if word not in self.terms.keys():
                            self.terms[word] = {}

                        if doc_id not in self.terms[word].keys():
                            self.terms[word][doc_id] = {
                                'frequency': 0,
                                'position': [],
                            }

                        self.terms[word][doc_id]['frequency'] += 1
                        self.terms[word][doc_id]['position'].append(index)

        for term, value in self.terms.items():
            self.termsDictionary[term] = len(value)

        f = open('dictionary.json', 'w')
        f.write(json.dumps(self.termsDictionary, indent=4, sort_keys=True))
        f.close()

        f = open('posting-list.json', 'w')
        f.write(json.dumps(self.terms, indent=4, sort_keys=True))
        f.close()

    def format_ranking_list(self):
        vector_space_dictionary = self.vector_space_dictionary
        posting_list = self.terms
        all_doc_count = len(self.documents.keys())
        for term, postings in posting_list.items():
            document_frequency = self.termsDictionary[term]
            idf = math.log(all_doc_count / document_frequency)
            for doc_id, doc_info in postings.items():
                frequency = doc_info['frequency']
                term_frequency = 1 + math.log(frequency)
                term_weight = term_frequency * idf
                if doc_id not in vector_space_dictionary.keys():
                    vector_space_dictionary[doc_id] = {}
                vector_space_dictionary[doc_id][term] = term_weight

        self.vector_space_dictionary = vector_space_dictionary


if __name__ == '__main__':
    """
    main function called when ./test.py is called
    calls the Test class
    """
    t = Invert()
    t.parse_documents
    t.create_posting_list(False, False)
    t.format_ranking_list()
