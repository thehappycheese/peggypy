


from . import visitor 



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
