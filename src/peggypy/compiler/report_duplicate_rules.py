

from typing import Any

from ..grammar_error import GrammarError, Diagnostic
from .utils_and_types.visitor import Visitor
from .utils_and_types.syntax_tree import Location, Node, Rule

# Checks that each rule is defined only once.
def reportDuplicateRules(ast:Node, options:dict[str,Any]):
	rule_names_found:dict[str,Location] = {}

	def rule(self:Visitor, node:Rule, options:dict[str,Any]):
		if node.name in rule_names_found:
			raise GrammarError(
				f'Rule "{node.name}" is already defined',
				node.nameLocation,
				[Diagnostic(
					message="Original rule location",
					location=rule_names_found[node.name],
				)]
			)
		rule_names_found[node.name] = node.nameLocation

	Visitor({
		"rule":rule,
	}).visit(ast, options)



