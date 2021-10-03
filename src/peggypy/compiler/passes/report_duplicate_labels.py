
from ...location import Location
from ...diagnostic import Diagnostic
from ...grammar_error import GrammarError
from ..visitor import Visitor

# Checks that each label is defined only once within each scope.
def reportDuplicateLabels(ast, *args):
	
	# def cloneEnv(env):
	# 	clone = {}
	# 	for name in env:
	# 		clone[name] = env[name];
	# 	return clone

	def checkExpressionWithClonedEnv(self, node, env:dict[str, Location], *args):
		self.visit(node.expression, env.copy())

	def rule(self, node, *args):
		self.visit(node.expression, { })

	def choice(self, node, env:dict[str, Location], *args):
		for alternative in node.alternatives:
			self.visit(alternative, env.copy())
		

	def labeled(self, node, env:dict[str, Location], *args):
		# TODO: make sure node constructor has attribute label set to None by default, or change to dict access
		# TODO: pretty much all these compiler passes will need to be checked once we find out the specifics of the Node type
		if node.label is not None and node.label in env:
			raise GrammarError(
				f'Label "{node.label}" is already defined',
				node.labelLocation,
				[Diagnostic(
					message= "Original label location",
					location= env[node.label],
				)]
			)
		self.visit(node.expression, env)
		env[node.label] = node.labelLocation

	Visitor(
		rule         = rule,
		choice       = choice,
		action       = checkExpressionWithClonedEnv,
		labeled      = labeled,
		text         = checkExpressionWithClonedEnv,
		simple_and   = checkExpressionWithClonedEnv,
		simple_not   = checkExpressionWithClonedEnv,
		optional     = checkExpressionWithClonedEnv,
		zero_or_more = checkExpressionWithClonedEnv,
		one_or_more  = checkExpressionWithClonedEnv,
		group        = checkExpressionWithClonedEnv,
	).visit(ast)



