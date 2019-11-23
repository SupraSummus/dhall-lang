# Sphinx project configuration
project = 'Dhall'
copyright = '2019, Dhall Contributors'
author = 'Dhall Contributors'
master_doc = 'index'

pygments_style = 'sphinx'
html_theme_options = {
    'show_related': True,
    'page_width': 'auto',
    'github_user': 'dhall-lang',
    'github_repo': 'dhall-lang',
    'logo': 'dhall-logo.svg',
    # sticky sidebar
    #'fixed_sidebar': True,
    'sidebar_collapse': False,
}
html_static_path = ['_static']
templates_path = ['_templates']
# Add markdown support
from recommonmark.parser import CommonMarkParser
source_suffix = ['.md']
source_parsers = {
    '.md': CommonMarkParser,
}

# Install AutoStructify to support toctree through eval_rst
from recommonmark.transform import AutoStructify

def setup(app):
    app.add_config_value('recommonmark_config', {
        'enable_auto_toc_tree': False,
    }, True)
    app.add_transform(AutoStructify)

# Add a custom lexer for dhall pygments
from pygments.lexer import RegexLexer, bygroups
from pygments import token
from sphinx.highlighting import lexers

# TODO: finish the lexer
DhallWords = r'|'.join((
    r'->',
    r'→',
    r'λ',
    r'∀',
    r'##'
    r'#',
    r'!='
    r'\?',
    r'\+\+',
    r'\+',
    r'-',
    r'&&',
    r'&',
    r'\|\|',
    r'\|',
    r'==',
    r'=',
    r':',
    r'\∧'
))
DhallKeywords = '|'.join((
    'if', 'then', 'else',
    'let', 'in',
    'as',
    'using',
    'merge',
    'forall'
))
class DhallLexer(RegexLexer):
    name = 'dhall'

    tokens = {
        'root': [
            (r'^(.*)(-- .*)$', bygroups(token.Text, token.Comment)),
            (r'{-(?:.|\n)*?-}', token.Comment),
            (r"'[^']+'", token.String.Char),
            (r'"[^"]+"', token.String.Char),
            # / is a \breaker and this avoid prelude url to be highlighted
            (r'(http[:a-zA-Z/\.-]+)', token.Text),
            (r'(\'\'(?:.|\n)*?\'\')', token.String.Char),
            (r'\b(\+\d+|-\d+|\d+)', token.Number.Integer),
            (r'\b(None|Some|Bool|Natural|Integer|Double|Text|Type|List|Optional)\b', token.Keyword.Type),
            (r'\b(%s)\b' % DhallKeywords, token.Keyword),
            (r'(%s)' % DhallWords, token.Operator.Word),
            (r'\b(True|False)\b', token.Name.Builtin.Pseudo),
                        (r'-- .*$', token.Comment),
            (r',', token.Punctuation),
            (r'.', token.Text),
        ]
    }
lexers['dhall'] = DhallLexer(startinline=True)

# Alias for compat with github syntax highligher name
from pygments.lexers.shell import BashLexer
from pygments.lexers.haskell import HaskellLexer
lexers['bash'] = BashLexer(startinline=True)
lexers['haskell'] = HaskellLexer(startinline=True)