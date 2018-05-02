Markdown Insert Source
========================

A Python Markdown extension that replaces code blocks with contents from
a given source file.

Keep all your code in one place and insert it in your markdown document.

This plugin will optionally insert all needed [klipse](https://github.com/viebel/klipse)
configuration on your post to allow your code to run client side.

Should work with any Python-Markdown-based static site generation, such as 
[MkDocs](http://www.mkdocs.org/), [Pelican](http://blog.getpelican.com/), and
[Nikola](https://getnikola.com/). It was tested with Pelican.

# Installation

    

# Configuration

Activate the `mdx_importsource` extension. For example, with Pelican, you add a
configuration line to your configuration file (i.e. `pelicanconf.py`):

```
MARKDOWN = {
    'extension_configs': {
        'importsource': {
            'source_paths': [
                os.path.abspath('./source')
            ],
            'enable_live_code': True
        },
        ...
    }
```

Also, in order for the `hide=all` and `hide=results` params to work you'll need to
add the following css to your site:

```css
.hidden {
    display: none;
}

.hidden-results .klipse-result {
    display: none;
}
```

The `source_paths` option is needed if you plan to import source files and it needs to contain at least one absolute path to search for files.

# Markdown Examples

## Embedded code with live code disabled

This is just the default way a Markdown `code` block works. The syntax is the same and 
the extension won't do anything:

````
```clojure
(def my-value 10)
```
````


## Using an external file with live code disabled

You can use the `source` parameter to select which file to import code from. The file must
exist on any of the given `source_paths`. Additionally, you can use the `#LN-LM` to only include
lines `N` through `M`. By default, the whole file will be included.

````
```java source=price-decided.cljs#L1-L4
```
````

You can leave the block empty or add any extra code you want to be appended to the rendered
block.

## Using live code

You can set `enable_live_code` to `True` on your config file. That will allow you to make code live
so that it runs on the client side. To achieve this, this extension uses the 
[Klipse](https://github.com/viebel/klipse) plugin, which supports clojure, ruby, javascript,
python, scheme, es2017, jsx, brainfuck, c++, reagent, lua, ocaml and reasonml.

Even with `enable_live_code` set to `True`, you'll still need to activate code on a per block
basis:

````
```python live
# This code will execute
print(1+2)
```
````

````
```python
#This code will remain unexecuted
print(2+2)
```
````

In addition to the `source` param, when using live code you can also use the `hide` param
to either hide the complete block (`all`) or only hide the result block (`results`). Using `all`
is useful in case you want to run some initialization code (of course, the source code can still
be seen by using the browser's view source). Using `results` is useful when the return value of
the executed commands is relevant to your post.


# Credits

Live code support is done by [Klipse](https://github.com/viebel/klipse). You can check their site
to learn more about this extension.

# License

[MIT License](http://www.opensource.org/licenses/mit-license.php)