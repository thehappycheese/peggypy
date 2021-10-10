

from ...grammar_error import GrammarError
from .. import asts
from ..visitor import Visitor


# Reports left recursion in the grammar, which prevents infinite recursion in
# the generated parser.
#
# Both direct and indirect recursion is detected. The pass also correctly
# reports cases like this:
#
#   start = "a"? start
#
# In general, if a rule reference can be reached without consuming any input,
# it can lead to left recursion.
def reportInfiniteRecursion(ast, *args):
	# Array with rule names for error message
	visitedRules = []
	# Array with rule_refs for diagnostic
	backtraceRefs = []

	def rule(self, node, *args):
		visitedRules.append(node.name)
		self.visit(node.expression)
		visitedRules.pop()

	def sequence(self, node, *args):
		# TODO:  Array.every result is unused in original code???  Array.every appears to be used as a way to stop iteration on the first false result
		for element in node.elements:
			self.visit(element)
			if not asts.alwaysConsumesOnSuccess(ast, element):
				break

	def rule_ref(self, node, *args):
		backtraceRefs.push(node)

		rule = asts.findRule(ast, node.name)

		if node.name in visitedRules:
			self.visit(rule, *args)
			backtraceRefs.pop()
		else:
			visitedRules.push(node.name)
			diagnostics = []
			for index, ref in enumerate(backtraceRefs):
				if index + 1 != len(backtraceRefs):
					message = f'Step {index + 1}: call of the rule "{ref.name}" without input consumption' 
				else:
					message = f"Step {index + 1}: call itself without input consumption - left recursion"
				diagnostics.append({"message":message, "location": ref.location})
			raise GrammarError(
				f"Possible infinite loop when parsing (left recursion: {visitedRules.join(' -> ')} )",
				rule.nameLocation,
				diagnostics
			)

	Visitor(
		rule=rule,
		sequence=sequence,
		rule_ref=rule_ref
	).visit(ast)


