import os


class Importer():
    def __init__(self, filename, start, end):
        self.filename = filename
        self.start = start
        self.end = end

    def readlines(self):
        # Indices are 0 based on python and 1 based on IDEs and github.
        # We leave `end` as it is because we want to include the last line
        start = self.start - 1
        end = self.end
        with open(self.filename, 'r') as f:
            return f.readlines()[start:end]
