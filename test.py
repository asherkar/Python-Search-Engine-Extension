#!/usr/bin/env python3
from invert import Invert
from porter import PorterStemmer
import json
import time
import math


class Test:

    def __init__(self):
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
        self.search_user_input()

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
                self.search_term(query)

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
        start_time = time.time()  ##start timer
        processed_query = self.process_query(word)
        for doc_id, term_weights in self.invert.vector_space_dictionary.items():
        # TODO: COSINE SIMILARITY SOMEHOW juse need the dot product

        # if self.stemming_toggle:
        #     p = PorterStemmer()
        #     word = p.stem(word, 0, len(word) - 1)
        #
        # if word in self.term_dictionary:
        #     found_items = self.posting_list[word]
        #     found_documents = []
        #     document_ids = found_items.keys()
        #     for doc_id in document_ids:
        #         position = found_items[doc_id]['position']
        #         abstract = self.invert.documents[doc_id]['abstract'].split(' ')
        #         first_pos = position[0]
        #         start_pos = 0
        #         end_pos = len(abstract) -1
        #         summary = ''
        #         if len(abstract) > 10:
        #             start_pos = first_pos - 5
        #             if start_pos < 0:
        #                 start_pos = 0
        #
        #             end_pos = start_pos + 10
        #
        #             if end_pos > len(abstract) -1:
        #                 end_pos = len(abstract) -1
        #                 start_pos = end_pos - 10
        #
        #         for term in abstract[start_pos:end_pos]:
        #             summary += term + ' '
        #
        #         document = {
        #             'doc_id': doc_id,
        #             'title': self.invert.documents[doc_id]['title'],
        #             'term frequency': found_items[doc_id]['frequency'],
        #             'positions': position,
        #             'summary': summary
        #         }
        #         found_documents.append(document)
        #
        #     print(json.dumps(found_documents, indent=4, sort_keys=True))
        #     end_time = time.time()
        #     search_time = round(end_time - start_time, 3)
        #     self.search_times.append(search_time)
        #     print("Found", str(self.term_dictionary[word]), "items in", search_time, "seconds")
        # else:
        #     print('No results found for the term ' + word)

    def process_query(self, query):
        all_doc_count = len(self.invert.documents.keys())
        query_array = query.split(' ')
        query_weights = {}
        while query_array:
            word = query_array.pop(0)
            print(word)
            frequency = 1

            while word in query_array:
                query_array.pop(query_array.index_word)
                frequency += 1

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
