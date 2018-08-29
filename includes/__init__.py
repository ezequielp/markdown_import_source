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
    for language in languages:
        selector = '.language-eval-{}'.format(language)
        if language == 'clojure':
            klipse_settings['selector'] = '.language-klipse, {}'.format(selector)
        else:
            klipse_settings['selector_eval_{}'.format(language if language != 'python' else 'python_client')] = selector

    return KLIPSE_INCLUDE.format(klipse_settings=json.dumps(klipse_settings)).split("\n")
