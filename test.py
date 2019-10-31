#!/usr/bin/env python3
from invert import Invert
from porter import PorterStemmer
import json
from util import fetch_stopwords
import math
import numpy
import operator


class Test:

    def __init__(self, auto=False):
        """
        main function of the application, sets the
        default values for stopword and stemming
        """
        self.stopword_toggle = False
        self.stemming_toggle = False
        self.posting_list = {}
        self.term_dictionary = {}
        self.search_times = []

        self.invert = Invert()
        self.load_files()
        if not auto:
            self.search_user_input()
        #self.k_value = 10

    def search_user_input(self):
        """
        gets user input and acts accordingly to provided term
        strips the leading spaces

        Note: all term searches are not case sensitive
        special key terms
            stopword: toggles the use of stop words
            stemming: toggles the use of stemming
            HELP: help menu
            ZZEND: exits the program
        :return:
        """
        data = input('Enter a search term or stopword to toggle stopwords\n')
        while data is not None:
            query = data.lower().rstrip()

            if 'HELP' in data:
                print('Enter stopword to toggle the use of stopwords')
                print('Enter stemming to toggle the use of stemming')
                print('Enter ZZEND to exit')

            elif 'stopword' in query:
                use_stop_words = input('use stop words? (y/n)\n')

                while use_stop_words is not None:
                    if use_stop_words.lower() == 'y':
                        self.stopword_toggle = True
                        self.load_files()
                        print('Stopwords are being used in the search')
                        print(len(self.posting_list))
                        break

                    elif use_stop_words.lower() == 'n':
                        self.stopword_toggle = False
                        self.load_files()
                        print('Stopwords are not being used in the search')
                        break

                    use_stop_words = input('please enter y or n\n')

            elif 'stemming' in query:
                use_stemming = input('stem the words? (y/n)\n')

                while use_stemming is not None:
                    if use_stemming.lower() == 'y':
                        print(len(self.posting_list))
                        self.stemming_toggle = True
                        self.load_files()
                        print('the words are now being stemmed in search')
                        break

                    elif use_stemming.lower() == 'n':
                        self.stemming_toggle = False
                        self.load_files()
                        print('the words are not being stemmed in search')
                        break

                    use_stemming = input('please enter y or n\n')

            elif data == 'ZZEND':
                average_search_time = round(sum(self.search_times) / len(self.search_times), 3)
                print('Average search time:', average_search_time, ' seconds')
                print('exiting program')
                exit()

            else:
                found_documents = self.search_term(query)
                if len(found_documents) > 0:
                    print(json.dumps(found_documents, indent=4, sort_keys=True))
                else:
                    print('No results found for ' + query)

            data = input('Enter a search term or HELP for more options\n')

    def load_files(self):
        """
        calls the create_posting_list function in invert
        using the stopword and stemming toggles

        imports the files created by invert into dictionaries
        """
        self.invert.create_posting_list(self.stopword_toggle, self.stemming_toggle)
        self.invert.format_ranking_list()
        f = open('posting-list.json', 'r')
        self.posting_list = json.load(f)
        f.close()
        f = open('dictionary.json', 'r')
        self.term_dictionary = json.load(f)
        f.close()

    def search_term(self, word):
        """
        searches for the term provided by the user
        used the stemming toggles to stem the provided term
        formats the search result to provide:
            doc_id: id of the document
            title: document title
            term_frequency: number of times the term appeared in documents
            positions: array of index of each term in the document
            summary: summary of document with 10 characters around the first instance of term


        :param word: term to search

        :return: prints out the time taken and the results in pretty print json
                 and the number of documents the term appeared in
        """
        k_value = 10
        processed_query = self.process_query(word)
        document_ranking = {}
        query_vector = numpy.sqrt(numpy.sum(numpy.square(list(processed_query.values()))))
        for doc_id, term_weights in self.invert.vector_space_dictionary.items():
            doc_vector = numpy.sqrt(numpy.sum(numpy.square(list(term_weights.values()))))
            if query_vector == 0 or doc_vector == 0:
                document_ranking[doc_id] = 0.0
                continue
            dot_product = 0
            for word, weight in processed_query.items():
                if word in term_weights.keys():
                    dot_product += (weight * term_weights[word])
            cosine_similarity = dot_product / (query_vector * doc_vector)
            document_ranking[doc_id] = cosine_similarity
        document_ranking = dict(sorted(document_ranking.items(), key=operator.itemgetter(1), reverse=True))

        found_documents = []
        for doc_id, similarity in document_ranking.items():
            if len(found_documents) == k_value:
                break
            if similarity <= 0 or numpy.isnan(similarity):
                continue
            document = {
                'ranking': len(found_documents) + 1,
                'doc_id': doc_id,
                'title': self.invert.documents[doc_id]['title'],
                'author': self.invert.documents[doc_id]['author'],
            }
            found_documents.append(document)

        return found_documents

    def process_query(self, query):
        all_doc_count = len(self.invert.documents.keys())
        query_array = [x.lower() for x in query.split(' ')]
        query_weights = {}
        stopwords = []
        if self.stopword_toggle:
            stopwords = fetch_stopwords()
        while query_array:
            word = query_array.pop(0)
            frequency = 1

            for a in [',', '.', '{', '}', '(', ')', ';', ':', '"', '\'']:
                if a in word:
                    if word.index(a) == 0 or word.index(a) == len(word) - 1:
                        word = word.replace(a, '')

            while word in query_array:
                query_array.pop(query_array.index(word))
                frequency += 1

            if self.stemming_toggle:
                p = PorterStemmer()
                word = p.stem(word, 0, len(word) - 1)

            if word in stopwords:
                continue

            term_weight = 0
            if word in self.invert.termsDictionary.keys():
                document_frequency = self.invert.termsDictionary[word]
                idf = math.log(all_doc_count / document_frequency)
                term_frequency = 1 + math.log(frequency)
                term_weight = idf * term_frequency

            query_weights[word] = term_weight
        return query_weights


if __name__ == '__main__':
    """
    main function called when ./test.py is called
    calls the Test class
    """
    t = Test()
