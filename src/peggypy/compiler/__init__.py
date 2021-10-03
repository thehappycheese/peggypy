


from typing import Any, Callable

from peggypy.node import Node


# Generates a parser from a specified grammar AST. Throws |peg.GrammarError|
# if the AST contains a semantic error. Note that not all errors are detected
# during the generation and some may protrude to the generated parser and
# cause its malfunction.
def compile_ast_code(ast:Node, passes:list[Callable[..., Any]], **options:Any) -> str:

	if "allowedStartRules" not in options or options["allowedStartRules"] is None:
		options["allowedStartRules"] = [ast.rules[0].name]

	if not isinstance(options["allowedStartRules"], list):
		raise Exception("allowedStartRules must be an array") ## TODO: Of node names??

	if len(options["allowedStartRules"])==0:
		raise Exception("Must have at least one start rule")
	
	allRules = [rule.name for rule in ast.rules]

	for rule in options["allowedStartRules"]:
		if not rule in allRules:
			raise Exception(f'Unknown start rule "{rule}"')
		
	for each_pass in passes:
			# mutates ast
			each_pass(ast, options)

	return ast.code


def compile_parser(ast:Node, passes:list[Callable[..., Any]], **options:Any) -> Callable[..., Any]:
	# mutates ast
	compile_ast_code(ast, passes, **options)
	return eval(ast.code)


def compile_to_source(ast:Node, passes:list[Callable[..., Any]], **options:Any) -> str:
	# mutates ast
	compile_ast_code(ast, passes, **options)
	return ast.code