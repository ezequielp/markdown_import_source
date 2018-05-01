import json
KLIPSE_INCLUDE = """<!-- Klipse includes -->
<link
    rel="stylesheet"
    type="text/css"
    href="https://storage.googleapis.com/app.klipse.tech/css/codemirror.css">
<script>
    window.klipse_settings = {klipse_settings};
</script>
<script src="https://storage.googleapis.com/app.klipse.tech/plugin/js/klipse_plugin.js">
</script>"""


def klipse_include(languages):
    klipse_settings = {}
    selectors = ['language-klipse']
    for language in languages:
        selector = '.lang-eval-{}'.format(language)
        selectors.append(selector)
        klipse_settings['selector_eval_{}'.format(language)] = selector

    klipse_settings['selector'] = ', '.join(selectors)
    return KLIPSE_INCLUDE.format(klipse_settings=json.dumps(klipse_settings)).split("\n")
