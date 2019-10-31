#!/usr/bin/env python3
from util import process_cacm_files

class Eval:
    def __init__(self):
        """
        main function of the application, sets the
        default values for stopword and stemming
        """
        self.queries = {}
        self.process_files()


    def process_files(self):
        self.queries = process_cacm_files('query.text')
        for id, query in self.queries.items():


if __name__ == '__main__':
    """
    main function called when ./eval.py is called
    calls the Test class
    """
    Eval()
