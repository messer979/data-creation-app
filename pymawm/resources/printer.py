from pygments import highlight
from pygments.lexers import JsonLexer, Python3Lexer
from pygments.token import Token
from pygments.formatters import TerminalFormatter, Terminal256Formatter
from pygments.style import Style
import json


from pprint import pformat

class PymawmStyle(Style):
    styles = {
        Token.String: 'ansibrightgreen',
        Token.Number: 'ansibrightblue',
    }

def pretty_json(obj):
    print(
        highlight(
            json.dumps(obj, sort_keys=True, indent=2),
            JsonLexer(), 
            TerminalFormatter()
            )
        )

def pretty_py(obj):
    print(
        highlight(
            pformat(obj),
            Python3Lexer(), 
            Terminal256Formatter(style=PymawmStyle)
            )
        )
