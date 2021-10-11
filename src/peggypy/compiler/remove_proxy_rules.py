

from typing import Any, cast

from .utils_and_types.syntax_tree import Grammar, Rule_Ref
from .utils_and_types.visitor import Visitor



def rule_ref(self:Visitor, node:Rule_Ref, options:dict[str, Any]):
	if node.name == options["from_rule_name"]:
		node.name = options["to_rule_name"]
	
replace_rule_refs_visitor = Visitor({
	"rule_ref":rule_ref,
})

def replace_rule_refs(grammar:Grammar, from_rule_name:str, to_rule_name:str, options:dict[str, Any]):
		replace_rule_refs_visitor.visit(grammar, {**options, "from_rule_name":from_rule_name, "to_rule_name":to_rule_name})

# Removes proxy rules -- that is, rules that only delegate to other rule.
def removeProxyRules(grammar:Grammar, options:dict[str, Any]):
	
	indices:list[int] = []

	for index, rule in enumerate(grammar.rules):
		if rule.expression.type == "rule_ref":
			rule.expression = cast(Rule_Ref, rule.expression)
			replace_rule_refs(grammar, rule.name, rule.expression.name, options)
			# TODO:
			if rule.name not in options["allowed_start_rules"]:
				indices.append(index)
	
	# Note: indices are already sorted
	for index in reversed(indices):
		grammar.rules.pop(index)


