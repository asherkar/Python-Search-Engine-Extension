#!/usr/bin/env python3
import re


def process_cacm_files(file_name):
    file = {}
    f = open('cacm/' + file_name, 'r')
    line = f.readline()
    while line:
        next_line = None

        if '.I ' in line:
            file_id = re.sub('.I ', '', line).rstrip()

            file[file_id] = {
                'id': file_id,
                'abstract': '',
                'title': '',
                'publication': '',
                'author': ''
            }
            next_line = f.readline()

            while next_line and not ('.I ' in next_line):
                if '.W' in next_line:
                    next_line = f.readline()
                    abstract = ''

                    while next_line and not re.match(r'[.][A-Z]\s', next_line):
                        abstract += ' ' + next_line.rstrip()
                        next_line = f.readline()

                    file[file_id]['abstract'] = abstract

                if '.T' in next_line:
                    file[file_id]['title'] = f.readline().rstrip()

                if '.B' in next_line:
                    file[file_id]['publication'] = f.readline().rstrip()

                if '.A' in next_line:
                    file[file_id]['author'] = f.readline().rstrip()

                next_line = f.readline()

        line = f.readline() if next_line is None else next_line

    f.close()
    return file
