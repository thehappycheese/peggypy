

#from ...location import Location
#from ...diagnostic import Diagnostic
from typing import Any
from ...grammar_error import GrammarError
from ..visitor import Visitor
from ...syntax_tree import Node, MATCH
import ...syntax_tree as st


# ALWAYS_MATCH = 1
# SOMETIMES_MATCH = 0
# NEVER_MATCH = -1

# Inference match result of the each node. Can be:
# -1: negative result, matching of that node always fails
#  0: neutral result, may be fail, may be match
#  1: positive result, always match
def inferenceMatchResult(ast):
	def sometimesMatch(self, node, *args):
		node.match = MATCH.SOMETIMES
		return MATCH.SOMETIMES

	def alwaysMatch(self, node, *args):
		inference(node.expression) ## TODO
		node.match = MATCH.ALWAYS
		return node.match

	def inferenceExpression(node):
		node.match = inference(node.expression) ## TODO
		return node.match
	
	def inferenceElements(elements, forChoice):
		length = elements.length
		always = 0
		never = 0
		for element in elements:
			
			result = inference(element) ## TODO
			
			if result == MATCH.ALWAYS:
				always+=1

			if result == MATCH.NEVER:
				never+=1
		

		if always == length:
			return MATCH.ALWAYS
		
		if forChoice:
			return MATCH.NEVER if never == length else MATCH.SOMETIMES
		

		return MATCH.NEVER if never > 0 else MATCH.SOMETIMES
	

	def rule(self:Visitor, node:syntax_tree.Rule, *args:Any, **kwargs:Any) -> MATCH:
		oldResult:MATCH
		count = 0

		# If property not yet calculated, do that
		if node.match is None:
			node.match = MATCH.SOMETIMES
			while True:
				oldResult = node.match
				node.match = self.visit(node.expression)
				# 6 == 3! -- permutations count for all transitions from one match
				# state to another.
				# After 6 iterations the cycle with guarantee begins
				# For example, an input of `start = [] start` will generate the
				# sequence: 0 -> -1 -> -1 (then stop)
				#
				# A more complex grammar theoretically would generate the
				# sequence: 0 -> 1 -> 0 -> -1 -> 0 -> 1 -> ... (then cycle)
				# but there are no examples of such grammars yet (possible, they
				# do not exist at all)

				# istanbul ignore next  This is canary test, shouldn't trigger in real life
				count+=1
				if count > 6:
					raise GrammarError(
						"Infinity cycle detected when trying to evaluate node match result",
						node.location
					)
				if oldResult == node.match:
					break
		return node.match
	
	
	def choice(node:Node):
		node.match = inferenceElements(node.alternatives, True)
		return node.match
	
	
	def sequence(node:Node):
		node.match = inferenceElements(node.elements, False)
		return node.match

	
	def simple_not(node:Node):
		node.match = -inference(node.expression)
		return node.match
		
	
	def rule_ref(node:Node):
		rule = asts.findRule(ast, node.name)

		node.match = inference(rule)
		return node.match
	
	def literal(node:Node):
		# Empty literal always match on any input
		node.match = Node_MATCH.ALWAYS_MATCH if node.value.length == 0 else Node_MATCH.SOMETIMES_MATCH
		return node.match
	
	def _class(node:Node):
		# Empty character class never match on any input
		node.match = Node_MATCH.NEVER_MATCH if node.parts.length == 0 else Node_MATCH.SOMETIMES_MATCH
		return node.match
	
	# |any| not match on empty inputde:

	inference = Visitor(
		rule         = rule,
		named        = inferenceExpression,
		choice       = choice,
		action       = inferenceExpression,
		sequence     = sequence,
		labeled      = inferenceExpression,
		text         = inferenceExpression,
		simple_and   = inferenceExpression,
		simple_not   = simple_not,
		optional     = alwaysMatch,
		zero_or_more = alwaysMatch,
		one_or_more  = inferenceExpression,
		group        = inferenceExpression,
		semantic_and = sometimesMatch,
		semantic_not = sometimesMatch,
		rule_ref     = rule_ref,
		literal      = literal,
		_class       = _class,
		_any         = sometimesMatch,
		# |any| not match on empty input
	)

	inference(ast);
}

inferenceMatchResult.ALWAYS_MATCH    = Node_MATCH.ALWAYS_MATCH;
inferenceMatchResult.SOMETIMES_MATCH = Node_MATCH.SOMETIMES_MATCH;
inferenceMatchResult.NEVER_MATCH     = Node_MATCH.NEVER_MATCH;


