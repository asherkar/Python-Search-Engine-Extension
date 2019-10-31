#!/usr/bin/env python3
from util import process_cacm_files
from test import Test
import numpy


class Eval:
    test = Test(auto=True)

    def __init__(self):
        """
        main function of the application, sets the
        default values for stopword and stemming
        """
        self.queries = {}
        self.process_files()

    def process_files(self):
        self.queries = process_cacm_files('query.text')
        relative_documents = open('cacm/qrels.text', 'r')
        line = relative_documents.readline().split(' ')
        for query_id, query in self.queries.items():
            query['relative_docs'] = []
            while line:
                if len(line) < 2 or (int(line[0]) != int(query_id)):
                    break
                query['relative_docs'].append(line[1])
                line = relative_documents.readline().split(' ')

        for query_id, query in self.queries.items():
            results = self.test.search_term(query['abstract'])
            if len(results) > 0:
                precision_relative_documents = []
                for index, result in enumerate(results):
                    if result['doc_id'] in query['relative_docs']:
                        precision = (len(precision_relative_documents) + 1) / (index + 1)
                        precision_relative_documents.append(precision)
                query_map = numpy.sum(precision_relative_documents) / len(results)
                r_precision = len(precision_relative_documents) / len(results)
                print(query_id + ':\n' + 'R_precision: ' + str(r_precision) + '\nmap: ' + str(query_map))


if __name__ == '__main__':
    """
    main function called when ./eval.py is called
    calls the Test class
    """
    Eval()
