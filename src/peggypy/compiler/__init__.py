


from typing import Any, Callable

from .utils_and_types.syntax_tree import Grammar


def compile_ast_code(ast:Grammar, passes:list[Callable[..., Any]], **options:Any) -> str:
	"""
	Generates a parser from a specified grammar AST. Throws `GrammarError`
	if the AST contains a semantic error. Note that not all errors are detected
	during the generation and some may protrude to the generated parser and
	cause its malfunction.
	"""

	if "allowed_start_rules" not in options or options["allowed_start_rules"] is None:
		options["allowed_start_rules"] = [ast.rules[0].name]

	if not isinstance(options["allowed_start_rules"], list):
		raise Exception("allowed_start_rules must be an array") ## TODO: Of node names??

	if len(options["allowed_start_rules"])==0:
		raise Exception("Must have at least one start rule")
	
	allRules = [rule.name for rule in ast.rules]

	for rule in options["allowed_start_rules"]:
		if not rule in allRules:
			raise Exception(f'Unknown start rule "{rule}"')
		
	for each_pass in passes:
			# mutates ast
			each_pass(ast, options)

	# TODO: is this right? if not go back and check the definition of Grammar.
	#   Maybe ast is not actually a grammar by this point... I think it has been mutated.
	return ast.code if ast.code is not None else "" 


def compile_parser(ast:Grammar, passes:list[Callable[..., Any]], **options:Any) -> Callable[..., Any]:
	return eval(
		compile_ast_code(ast, passes, **options)
	)


def compile_to_source(ast:Grammar, passes:list[Callable[..., Any]], **options:Any) -> str:
	return compile_ast_code(ast, passes, **options)