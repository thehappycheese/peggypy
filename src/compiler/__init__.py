

from .passes.generate_bytecode import generateBytecode;
from .passes.generate_py import generatePY;
from .passes.inference_match_result     import  inferenceMatchResult
from .passes.remove_proxy_rules         import  removeProxyRules
from .passes.report_duplicate_labels    import  reportDuplicateLabels
from .passes.report_duplicate_rules     import  reportDuplicateRules
from .passes.report_infinite_recursion  import  reportInfiniteRecursion
from .passes.report_infinite_repetition import  reportInfiniteRepetition
from .passes.report_undefined_rules     import  reportUndefinedRules
from .passes.report_incorrect_plucking  import  reportIncorrectPlucking
from . import visitor 

# Compiler passes.
#
# Each pass is a function that is passed the AST. It can perform checks on it
# or modify it as needed. If the pass encounters a semantic error, it throws
# |peg.GrammarError|.
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

# Generates a parser from a specified grammar AST. Throws |peg.GrammarError|
# if the AST contains a semantic error. Note that not all errors are detected
# during the generation and some may protrude to the generated parser and
# cause its malfunction.
def compile(ast, passes, options):

	if options["allowedStartRules"] is None:
		options["allowedStartRules"] = [ast.rules[0].name]

	if not isinstance(options["allowedStartRules"], list):
		raise Exception("allowedStartRules must be an array")

	if len(options["allowedStartRules"])==0:
		raise Exception("Must have at least one start rule")
	
	allRules = [rule.name for rule in ast.rules]

	for rule in options.allowedStartRules:
		if not rule in allRules:
			raise Exception(f'Unknown start rule "{rule}"')
		
	for stage in passes:
		for each_pass in stage:
			# mutates ast
			each_pass(ast, options)

	if options["output"]=="parser":
		return eval(ast.code)
	elif options["output"]=="source":
		return ast.code
	else:
		raise Exception(f"Invalid output format: {options.output}.")
