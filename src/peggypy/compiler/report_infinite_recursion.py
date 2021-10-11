

from typing import Any

from peggypy.compiler.always_consumes_on_success import always_consumes_on_success

from ..grammar_error import Diagnostic, GrammarError
from .utils_and_types.visitor import Visitor
from .utils_and_types.syntax_tree import (
	Grammar,
	Rule,
	Rule_Ref,
	Sequence
)


def rule(self:Visitor, node:Rule, options:dict[str, Any]):
	options["visited_rules"].append(node.name)
	self.visit(node.expression, options)
	options["visited_rules"].pop()

def sequence(self:Visitor, node:Sequence, options:dict[str, Any]):
	# TODO:  Array.every result is unused in original code???  Array.every appears to be used as a way to stop iteration on the first false result
	for element in node.elements:
		self.visit(element, options)
		if not always_consumes_on_success(options["grammar"], element, options):
			break

def rule_ref(self:Visitor, node:Rule_Ref, options:dict[str, Any]):
	options["backtrace_refs"].push(node)
	rule = options["grammar"].findRule(node.name)

	if node.name in options["visited_rules"]:
		self.visit(rule, options)
		options["backtrace_refs"].pop()
	else:
		options["visited_rules"].push(node.name)
		diagnostics:list[Diagnostic] = []
		for index, ref in enumerate(options["backtrace_refs"]):
			if index + 1 != len(options["backtrace_refs"]):
				message = f'Step {index + 1}: call of the rule "{ref.name}" without input consumption' 
			else:
				message = f"Step {index + 1}: call itself without input consumption - left recursion"
			diagnostics.append(Diagnostic(message, ref.location))
		raise GrammarError(
			f"Possible infinite loop when parsing (left recursion: {options['visited_rules'].join(' -> ')} )",
			rule.nameLocation,
			diagnostics
		)

report_infinite_recusrsion_visitor = Visitor({
	"rule"     : rule,
	"sequence" : sequence,
	"rule_ref" : rule_ref
})


def report_infinite_recusrsion(grammar:Grammar, options:dict[str, Any]):
	"""
	Reports left recursion in the grammar, which prevents infinite recursion in
	the generated parser.

	Both direct and indirect recursion is detected. The pass also correctly
	reports cases like this:

	start = "a"? start

	In general, if a rule reference can be reached without consuming any input,
	it can lead to left recursion.
	"""

	report_infinite_recusrsion_visitor.visit(grammar, {
		**options,
		"grammar":grammar,
		"visited_rules":[],
		"backtrace_refs": []
	})


