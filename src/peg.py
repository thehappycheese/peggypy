
from typing import Any, Dict, Literal, Optional, TypedDict, Union

from .grammar_error import GrammarError
from .compiler import compile
from .parser import parse


from .compiler.passes.generate_bytecode          import generateBytecode
from .compiler.passes.generate_py                import generatePY
from .compiler.passes.inference_match_result     import inferenceMatchResult
from .compiler.passes.remove_proxy_rules         import removeProxyRules
from .compiler.passes.report_duplicate_labels    import reportDuplicateLabels
from .compiler.passes.report_duplicate_rules     import reportDuplicateRules
from .compiler.passes.report_infinite_recursion  import reportInfiniteRecursion
from .compiler.passes.report_infinite_repetition import reportInfiniteRepetition
from .compiler.passes.report_undefined_rules     import reportUndefinedRules
from .compiler.passes.report_incorrect_plucking  import reportIncorrectPlucking

# Each pass is a function that may mutate the AST. 
# throws |peg.GrammarError|.
# TODO: this could be a flat array. 
# Maybe it is broken up like this for the benefit of 
# plugins which may modify the stages/passes?
passes = {
	"check": [
		reportUndefinedRules,
		reportDuplicateRules,
		reportDuplicateLabels,
		reportInfiniteRecursion,
		reportInfiniteRepetition,
		reportIncorrectPlucking,
	],
	"transform": [
		removeProxyRules,
		inferenceMatchResult,
	],
	"generate": [
		generateBytecode,
		generatePY,
	],
},


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


class GenerateOptions:
	allowedStartRules:list[str] = None
	cache:bool = False
	dependencies:dict = {} # valid only for "amd", "commonjs", "es", or "umd".
	exportVar:Optional[str] = None
	format:Literal["amd", "bare", "commonjs", "es", "globals", "umd"] = "bare"
	grammarSource = None
	output:Literal["parser", "source"] = "parser"
	plugins:list = []
	trace:bool = False

default_options = GenerateOptions()

def generate(grammar:str, options:GenerateOptions=None):
	options = default_options.update(options) if options else default_options
	

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
	
