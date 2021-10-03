

from ...diagnostic import Diagnostic
from ...grammar_error import GrammarError
from ..visitor import Visitor

# Checks that each rule is defined only once.
def reportDuplicateRules(ast, *args):
	rule_names_found = {}

	def rule(self, node, *args):
		if node.name in rule_names_found:
			raise GrammarError(
				f'Rule "{node.name}" is already defined',
				node.nameLocation,
				[Diagnostic(
					message= "Original rule location",
					location= rule_names_found[node.name],
				)]
			)
		rule_names_found[node.name] = node.nameLocation

	Visitor(
		rule=rule,
	).visit(ast)



