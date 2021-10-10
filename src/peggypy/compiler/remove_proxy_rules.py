

from typing import Any

from ..grammar_error import GrammarError
from ..diagnostic import Diagnostic

from .utils_and_types.syntax_tree import Node
from .utils_and_types.visitor import Visitor

# Removes proxy rules -- that is, rules that only delegate to other rule.
def removeProxyRules(ast:list[Node], **options:Any):
	
	def isProxyRule(node:Node) -> bool:
		return node.type == "rule" and node.expression.type == "rule_ref"
	
	def replaceRuleRefs(ast:list[Node], _from:str, to:str):
		
		def rule_ref(self:Visitor, node:Node, *args:Any, **kwargs:Any) -> None:
			if node.name == _from:
				node.name = to
			
		Visitor(
			rule_ref=rule_ref,
		).visit(ast)
	

	indices = []

	for index, rule in enumerate(ast):
		if isProxyRule(rule):
			replaceRuleRefs(ast, rule.name, rule.expression.name)
			if rule.name not in options.allowedStartRules:
				indices.push(index)
	
	# Note: indices are already sorted
	for index in reversed(indices):
		ast.rules.pop(index)


