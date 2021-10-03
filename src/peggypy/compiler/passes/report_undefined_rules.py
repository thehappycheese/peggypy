from ...grammar_error import GrammarError
from .. import asts
from ..visitor import Visitor

# Checks that all referenced rules exist.
def reportUndefinedRules(ast, *args):
	def rule_ref (self, node, *args):
		if asts.findRule(ast, node.name) is None:
			raise  GrammarError(
				f'Rule "{node.name=}" is not defined',
				node.location
			)

	check = Visitor(rule_ref = rule_ref)
	check.visit(ast)


