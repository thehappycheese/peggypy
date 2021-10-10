
from typing import Any
from .utils_and_types.syntax_tree import Choice, Expression, Labeled, Node, Rule, Location
from ..grammar_error import GrammarError, Diagnostic
from .utils_and_types.visitor import Visitor

# Checks that each label is defined only once within each scope.
def reportDuplicateLabels(ast:Node, *args:Any, **kwargs:Any):
	
	# def cloneEnv(env):
	# 	clone = {}
	# 	for name in env:
	# 		clone[name] = env[name];
	# 	return clone

	def checkExpressionWithClonedEnv(self:Visitor, node:Expression, env:dict[str, Location], *args:Any, **kwargs:Any):
		self.visit(node.expression, env.copy(), *args, **kwargs)

	def rule(self:Visitor, node:Rule, *args:Any, **kwargs:Any):
		self.visit(node.expression, { })

	def choice(self:Visitor, node:Choice, env:dict[str, Location], *args:Any, **kwargs:Any):
		for alternative in node.alternatives:
			self.visit(alternative, env.copy())
		

	def labeled(self:Visitor, node:Labeled, env:dict[str, Location], *args:Any, **kwargs:Any):
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
		if node.label is not None:
			env[node.label] = node.labelLocation
		else:
			# TODO: not sure what to do in this situation the other branch would not be an error in javascript
			#       this is maybe a benign bug in the original code? or was it deliberate behaviour?
			raise KeyError("What do we do about this error? In the original javascript code `undefined` is a legal index. Python does not allow `None` to be used as an index.")

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



