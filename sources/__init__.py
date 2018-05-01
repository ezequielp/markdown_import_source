from .filesystem import Importer
from .utils import resolve
import re


class SourceLineParser():
    def __init__(self, sourceline, source_paths):
        if source_paths:
            self.search_paths = source_paths
        else:
            self.search_paths = ['./']

        self.sourceline = sourceline

    def get_reader(self):
        filename, lines = self.sourceline.split('#')

        filename = resolve(self.search_paths, filename)
        lines = re.match('L(\d+)\-L(\d+)', lines)

        start, end = map(int, lines.groups()) if lines else (1, -1)

        return Importer(filename, start, end)
