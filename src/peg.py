
from typing import Any, Literal, Optional, TypedDict, Union

from .grammar_error import GrammarError
from .compiler import compile, passes
from .parser import parse

# TODO: these appear to be javascript reserved words.

RESERVED_WORDS = [
	# Reserved keywords as of ECMAScript 2015
	"break",
	"case",
	"catch",
	"class",
	"const",
	"continue",
	"debugger",
	"default",
	"delete",
	"do",
	"else",
	"export",
	"extends",
	"finally",
	"for",
	"function",
	"if",
	"import",
	"in",
	"instanceof",
	"new",
	"return",
	"super",
	"switch",
	"this",
	"throw",
	"try",
	"typeof",
	"var",
	"void",
	"while",
	"with",
	# "yield", # encountered twice on the web page

	# Special constants
	"null",
	"true",
	"false",

	# These are always reserved:
	"enum",

	# The following are only reserved when they are found in strict mode code
	# Peggy generates code in strictly mode, so it applicable to it
	"implements",
	"interface",
	"let",
	"package",
	"private",
	"protected",
	"public",
	"static",
	"yield",

	# The following are only reserved when they are found in module code:
	"await",
]


class OptionsType(TypedDict):
	allowedStartRules:list[str]
	cache:bool
	dependencies:dict # valid only for "amd", "commonjs", "es", or "umd".
	exportVar:Optional[str]
	format:Literal["amd", "bare", "commonjs", "es", "globals", "umd"]
	grammarSource:Any
	output:Literal["parser", "source"]
	plugins:list
	trace:bool

default_options:OptionsType = {
	"allowedStartRules": None,
	"cache": False,
	"dependencies": {},
	"exportVar": None,
	"format": "bare",
	"grammarSource":None,
	"output": "parser",
	"plugins": [],
	"trace": False,
}

def generate(grammar:str, options:OptionsType=None):
	options = default_options | options if options else default_options
	

	config = {
		"parser":parse,
		"passes":{stage:passes[:] for stage, passes in passes},
		"reservedWords":RESERVED_WORDS[:],
	}

	parsed_grammar = parse(
		grammar, 
		{
			"grammarSource":options.get("grammarSource", None),
			"reservedWords":config["reservedWords"]
		}
	)
	options["plugins"] = options.get("plugins", [])

	for plugin in options["plugins"]:
		plugin.use(config, options)

	return compile(
		parsed_grammar,
		config["passes"],
		options
	)
	
