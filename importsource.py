from markdown import Extension
from markdown.preprocessors import Preprocessor
import re
import os

BLOCKS = {
    'start': re.compile(
        r'```(?P<lang>[^=\s]+)\s(?P<attrs>.*)$'
    ),
    'end': re.compile(r'^```$')
}
KLIPSE_INCLUDE = """<!-- Klipse includes -->
<link
    rel="stylesheet"
    type="text/css"
    href="https://storage.googleapis.com/app.klipse.tech/css/codemirror.css">
<script>
    window.klipse_settings = {
      selector: ".language-klipse, .lang-eval-clojure",
      selector_eval_js: ".lang-eval-js"
    };
</script>
<script src="https://storage.googleapis.com/app.klipse.tech/plugin/js/klipse_plugin.js">
</script>""".split("\n")


def extract_attrs(line):
    match = BLOCKS['start'].match(line)
    language = match.group('lang')
    attr_string = match.group('attrs')
    return dict(lang=language, **dict(re.compile('([^=\s]+)=([^=\s]+)').findall(attr_string)))


class ImportSourcePreprocessor(Preprocessor):
    def __init__(self, md, config, *args, **kwargs):
        self.source_directories = config['source_paths']
        self.enable_live_code = config['enable_live_code']
        super(ImportSourcePreprocessor, self).__init__(*args, **kwargs)

    def find_blocks(self, lines):
        starts = [i for i, line in enumerate(lines) if BLOCKS['start'].match(line)]
        ends = [i for i, line in enumerate(lines) if BLOCKS['end'].match(line)]
        for start, end in zip(starts, ends):
            if end < start:
                raise Exception("Unmatched start block at line {}".format(start))
        if len(starts) > len(ends):
            raise Exception("Code block on line {} is not closed".format(starts[len(ends)]))

        return list(zip(starts, ends))

    def run(self, lines):
        new_lines = lines[:]
        blocks = self.find_blocks(lines)
        for start, end in blocks[::-1]:
            block_attrs = extract_attrs(lines[start])
            new_lines[start] = self.build_start_block(block_attrs, self.enable_live_code)

            end_offset = 0
            source = self.fetch_source(block_attrs)
            if source:
                # Insert source lines after start
                new_lines[start+1:start+1] = source
                end_offset = len(source)

            new_lines[end + end_offset] = self.build_end_block(self.enable_live_code)

        if blocks and self.enable_live_code:
            new_lines.extend(KLIPSE_INCLUDE)

        return new_lines

    def build_start_block(self, attrs, use_klipse):
        def new_class(name):
            return 'class={}'.format(name)

        pre_block = ['pre']
        code_block = ['code']

        # `lang` attr sets the language of the block
        if 'lang' in attrs:
            code_block.append(new_class('lang-eval-{}'.format(attrs.get('lang'))))

        # `hide` attr can be set to hide `all` the block or just the `results`
        hide = attrs.get('hide')
        if hide:
            if hide == 'all':
                pre_block.append(new_class('hidden'))
            elif hide == 'results':
                pre_block.append(new_class('hidden-results'))
            else:
                raise Exception("Unrecognized 'hide' value {}".format(hide))

        if use_klipse:
            return '<{}><{}>'.format(' '.join(pre_block), ' '.join(code_block))
        else:
            return '```{}'.format(attrs.get('lang', ''))

    def build_end_block(self, use_klipse):
        return "</code></pre>" if use_klipse else '```'

    def fetch_source(self, block_attrs):
        if self.source_directories:
            directories = self.source_directories
        else:
            directories = ['./']

        if 'source' in block_attrs:
            file_name, lines = block_attrs['source'].split('#')
            lines = re.match('L(\d+)\-L(\d+)', lines)

            start, end = map(int, lines.groups()) if lines else (1, -1)

            # Indices are 0 based on python and 1 based on IDEs and github.
            # We leave end as it is because we want to include the end line
            start = start-1

            tries = []
            for search_dir in directories:
                try:
                    full_name = os.sep.join([search_dir, file_name])
                    tries.append(full_name)
                    with open(full_name, 'r') as f:
                        return f.readlines()[start:end]
                except FileNotFoundError:
                    pass

                # Did not find the source file. Throw error
                error = (
                    "Could not find {} in supplied search paths. Tried: {}. "
                    "Remember to configure all search paths in the source_paths "
                    "configuration option."
                ).format(file_name, ', '.join(tries))
                raise FileNotFoundError(error)


class ImportSource(Extension):
    def __init__(self, *args, **kwargs):
        # Define config options and defaults
        self.config = {
            'source_paths': [[], 'The paths to search for source files'],
            'enable_live_code': [False, 'Use Klipse to run the inserted code client side']
        }

        # Call the parent class's __init__ method to configure options
        super(ImportSource, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('sourcecode', ImportSourcePreprocessor(md, self.getConfigs()), '_begin')


def makeExtension(*args, **kwargs):
    return ImportSource(*args, **kwargs)