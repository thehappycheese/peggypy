

from typing import Any
from .utils_and_types.syntax_tree import (
	Action,
	Choice,
	Class,
	Grammar,
	Group,
	Labeled,
	Named,
	One_or_More,
	Optional,
	Rule,
	Semantic_Not,
	Sequence,
	Simple_And,
	Simple_Not,
	Text,
	Zero_or_More
)
from .utils_and_types.stack import Stack
from .utils_and_types.visitor import Visitor
from .utils_and_types.opcodes import opcodes as op



# Generates bytecode.
#
# Instructions
# ============
#
# Stack Manipulation
# ------------------
#
#  [35] PUSH_EMPTY_STRING
#
#        stack.push("");
#
#  [1] PUSH_UNDEFINED
#
#        stack.push(undefined);
#
#  [2] PUSH_NULL
#
#        stack.push(null);
#
#  [3] PUSH_FAILED
#
#        stack.push(FAILED);
#
#  [4] PUSH_EMPTY_ARRAY
#
#        stack.push([]);
#
#  [5] PUSH_CURR_POS
#
#        stack.push(currPos);
#
#  [6] POP
#
#        stack.pop();
#
#  [7] POP_CURR_POS
#
#        currPos = stack.pop();
#
#  [8] POP_N n
#
#        stack.pop(n);
#
#  [9] NIP
#
#        value = stack.pop();
#        stack.pop();
#        stack.push(value);
#
# [10] APPEND
#
#        value = stack.pop();
#        array = stack.pop();
#        array.push(value);
#        stack.push(array);
#
# [11] WRAP n
#
#        stack.push(stack.pop(n));
#
# [12] TEXT
#
#        stack.push(input.substring(stack.pop(), currPos));
#
# [36] PLUCK n, k, p1, ..., pK
#
#        value = [stack[p1], ..., stack[pK]]; # when k != 1
#        -or-
#        value = stack[p1];                   # when k == 1
#
#        stack.pop(n);
#        stack.push(value);
#
# Conditions and Loops
# --------------------
#
# [13] IF t, f
#
#        if (stack.top()) {
#          interpret(ip + 3, ip + 3 + t);
#        } else {
#          interpret(ip + 3 + t, ip + 3 + t + f);
#        }
#
# [14] IF_ERROR t, f
#
#        if (stack.top() == FAILED) {
#          interpret(ip + 3, ip + 3 + t);
#        } else {
#          interpret(ip + 3 + t, ip + 3 + t + f);
#        }
#
# [15] IF_NOT_ERROR t, f
#
#        if (stack.top() != FAILED) {
#          interpret(ip + 3, ip + 3 + t);
#        } else {
#          interpret(ip + 3 + t, ip + 3 + t + f);
#        }
#
# [16] WHILE_NOT_ERROR b
#
#        while(stack.top() != FAILED) {
#          interpret(ip + 2, ip + 2 + b);
#        }
#
# Matching
# --------
#
# [17] MATCH_ANY a, f, ...
#
#        if (input.length > currPos) {
#          interpret(ip + 3, ip + 3 + a);
#        } else {
#          interpret(ip + 3 + a, ip + 3 + a + f);
#        }
#
# [18] MATCH_STRING s, a, f, ...
#
#        if (input.substr(currPos, literals[s].length) == literals[s]) {
#          interpret(ip + 4, ip + 4 + a);
#        } else {
#          interpret(ip + 4 + a, ip + 4 + a + f);
#        }
#
# [19] MATCH_STRING_IC s, a, f, ...
#
#        if (input.substr(currPos, literals[s].length).toLowerCase() == literals[s]) {
#          interpret(ip + 4, ip + 4 + a);
#        } else {
#          interpret(ip + 4 + a, ip + 4 + a + f);
#        }
#
# [20] MATCH_CHAR_CLASS c, a, f, ...
#
#        if (classes[c].test(input.charAt(currPos))) {
#          interpret(ip + 4, ip + 4 + a);
#        } else {
#          interpret(ip + 4 + a, ip + 4 + a + f);
#        }
#
# [21] ACCEPT_N n
#
#        stack.push(input.substring(currPos, n));
#        currPos += n;
#
# [22] ACCEPT_STRING s
#
#        stack.push(literals[s]);
#        currPos += literals[s].length;
#
# [23] FAIL e
#
#        stack.push(FAILED);
#        fail(expectations[e]);
#
# Calls
# -----
#
# [24] LOAD_SAVED_POS p
#
#        savedPos = stack[p];
#
# [25] UPDATE_SAVED_POS
#
#        savedPos = currPos;
#
# [26] CALL f, n, pc, p1, p2, ..., pN
#
#        value = functions[f](stack[p1], ..., stack[pN]);
#        stack.pop(n);
#        stack.push(value);
#
# Rules
# -----
#
# [27] RULE r
#
#        stack.push(parseRule(r));
#
# Failure Reporting
# -----------------
#
# [28] SILENT_FAILS_ON
#
#        silentFails++;
#
# [29] SILENT_FAILS_OFF
#
#        silentFails--;
#
# This pass can use the results of other previous passes, each of which can
# change the AST (and, as consequence, the bytecode).
#
# In particular, if the pass |inferenceMatchResult| has been run before self.pass,
# then each AST node will contain a |match| property, which represents a possible
# match result of the node:
# - `<0` - node is never matched, for example, `!('a'*)` (negation of the always
#          matched node). Generator can put |FAILED| to the stack immediately
# - `=0` - sometimes node matched, sometimes not. This is the same behavior
#          when |match| is missed
# - `>0` - node is always matched, for example, `'a'*` (because result is an
#          empty array, or an array with some elements). The generator does not
#          need to add a check for |FAILED|, because it is impossible
#
# To handle the situation, when the |inferenceMatchResult| has not run (that
# happens, for example, in tests), the |match| value extracted using the
# `|0` trick, which performing cast of any value to an integer with value `0`
# that is equivalent of an unknown match result and signals the generator that
# runtime check for the |FAILED| is required. Trick is explained on the
# Wikipedia page (https://en.wikipedia.org/wiki/Asm.js#Code_generation)
def generateBytecode(grammar:Grammar, options:dict[str, Any]):

	literals     = []
	classes      = []
	expectations = []
	functions    = []

	def addLiteralConst(value):
		if value in literals:
			return literals.index(value)
		else:
			literals.append(value)
			return len(literals) - 1
	

	def addClassConst(node:Class):
		cls = {
			"value": node.parts,
			"inverted": node.inverted,
			"ignoreCase": node.ignoreCase,
		}
		# TODO
		pattern = JSON.stringify(cls)
		index = classes.findIndex(lambda c: JSON.stringify(c) == pattern)
		return index == -1 ? classes.push(cls) - 1 : index
	

	def addExpectedConst(expected):
		pattern = JSON.stringify(expected)
		index = expectations.findIndex(e => JSON.stringify(e) == pattern)
		return index == -1 ? expectations.push(expected) - 1 : index
	

	def addFunctionConst(predicate, params, code):
		func = { predicate, params, body: code };
		pattern = JSON.stringify(func);
		index = functions.findIndex(f => JSON.stringify(f) == pattern)
		return index == -1 ? functions.push(func) - 1 : index

	def cloneEnv(env):
		clone = {};
		Object.keys(env).forEach(name => {
			clone[name] = env[name];
		})
		return clone
	

	def buildSequence(first, ...args):
		return first.concat(...args)
	

	def buildCondition(match, condCode, thenCode, elseCode):
		if (match == ALWAYS_MATCH) { return thenCode; }
		if (match == NEVER_MATCH)  { return elseCode; }

		return condCode.concat(
			[thenCode.length, elseCode.length],
			thenCode,
			elseCode
		);
	

	def buildLoop(condCode, bodyCode):
		return condCode.concat([bodyCode.length], bodyCode)

	def buildCall(functionIndex, delta, env, sp):
		params = Object.keys(env).map(name => sp - env[name])
		return [op.CALL, functionIndex, delta, params.length].concat(params)

	def buildSimplePredicate(expression, negative, context):
		match = expression.match or 0

		return buildSequence(
			[op.PUSH_CURR_POS],
			[op.SILENT_FAILS_ON],
			generate(expression, {
				sp: context.sp + 1,
				env: cloneEnv(context.env),
				action: None,
			}),
			[op.SILENT_FAILS_OFF],
			buildCondition(
				negative ? -match : match,
				[negative ? op.IF_ERROR : op.IF_NOT_ERROR],
				buildSequence(
					[op.POP],
					[negative ? op.POP : op.POP_CURR_POS],
					[op.PUSH_UNDEFINED]
				),
				buildSequence(
					[op.POP],
					[negative ? op.POP_CURR_POS : op.POP],
					[op.PUSH_FAILED]
				)
			)
		);
	

	def buildSemanticPredicate(node, negative, context):
		functionIndex = addFunctionConst(
			True, Object.keys(context.env), node.code
		);

		return buildSequence(
			[op.UPDATE_SAVED_POS],
			buildCall(functionIndex, 0, context.env, context.sp),
			buildCondition(
				node.match | 0,
				[op.IF],
				buildSequence(
					[op.POP],
					negative ? [op.PUSH_FAILED] : [op.PUSH_UNDEFINED]
				),
				buildSequence(
					[op.POP],
					negative ? [op.PUSH_UNDEFINED] : [op.PUSH_FAILED]
				)
			)
		)
	

	def buildAppendLoop(expressionCode):
		return buildLoop(
			[op.WHILE_NOT_ERROR],
			buildSequence([op.APPEND], expressionCode)
		);
	











	
	def grammar(self:Visitor, node:Grammar):
		node.rules.forEach(generate);

		node.literals = literals;
		node.classes = classes;
		node.expectations = expectations;
		node.functions = functions;
	

	def rule(self:Visitor, node:Rule):
		node.bytecode = generate(node.expression, {
			sp: -1,        # Stack pointer
			env: {},       # Mapping of label names to stack positions
			pluck: [],     # Fields that have been picked
			action: None,  # Action nodes pass themselves to children here
		});

	def named(self:Visitor, node:Named, context):
		match = node.match | 0;
		# Expectation not required if node always fail
		nameIndex = (match == NEVER_MATCH)
			? None
			: addExpectedConst({ type: "rule", value: node.name });

		# The code generated below is slightly suboptimal because |FAIL| pushes
		# to the stack, so we need to stick a |POP| in front of it. We lack a
		# dedicated instruction that would just report the failure and not touch
		# the stack.
		return buildSequence(
			[op.SILENT_FAILS_ON],
			generate(node.expression, context),
			[op.SILENT_FAILS_OFF],
			buildCondition(match, [op.IF_ERROR], [op.FAIL, nameIndex], [])
		);

	def choice(self:Visitor, node:Choice, context):
		def buildAlternativesCode(alternatives, context) {
			match = alternatives[0].match | 0;
			first = generate(alternatives[0], {
				sp: context.sp,
				env: cloneEnv(context.env),
				action: None,
			});
			# If an alternative always match, no need to generate code for the next
			# alternatives. Because their will never tried to match, any side-effects
			# from next alternatives is impossible so we can skip their generation
			if (match == ALWAYS_MATCH) {
				return first;
			}
			# Even if an alternative never match it can have side-effects from
			# a semantic predicates or an actions, so we can not skip generation
			# of the first alternative.
			# We can do that when analysis for possible side-effects will be introduced
			return buildSequence(
				first,
				alternatives.length > 1
					? buildCondition(
						SOMETIMES_MATCH,
						[op.IF_ERROR],
						buildSequence(
							[op.POP],
							buildAlternativesCode(alternatives.slice(1), context)
						),
						[]
					)
					: []
			);
		}
		return buildAlternativesCode(node.alternatives, context);
	

	def action(self:Visitor, node:Action, context):
		env = cloneEnv(context.env);
		emitCall = node.expression.type != "sequence" or node.expression.elements.length == 0
		expressionCode = generate(node.expression, {
			sp: context.sp + (1 if emitCall else 0),
			env,
			action: node,
		});
		match = node.expression.match | 0;
		# Function only required if expression can match
		functionIndex = addFunctionConst(False, Object.keys(env), node.code) if emitCall and match != NEVER_MATCH else None;

		return buildSequence(
				[op.PUSH_CURR_POS],
				expressionCode,
				buildCondition(
					match,
					[op.IF_NOT_ERROR],
					buildSequence(
						[op.LOAD_SAVED_POS, 1],
						buildCall(functionIndex, 1, env, context.sp + 2)
					),
					[]
				),
				[op.NIP]
			) if emitCall else expressionCode
	

	def sequence(self:Visitor, node:Sequence, context):
		def buildElementsCode(elements, context) {
			if (elements.length > 0) {
				processedCount = node.elements.length - elements.length + 1;

				return buildSequence(
					generate(elements[0], {
						sp: context.sp,
						env: context.env,
						pluck: context.pluck,
						action: None,
					}),
					buildCondition(
						elements[0].match | 0,
						[op.IF_NOT_ERROR],
						buildElementsCode(elements.slice(1), {
							sp: context.sp + 1,
							env: context.env,
							pluck: context.pluck,
							action: context.action,
						}),
						buildSequence(
							processedCount > 1 ? [op.POP_N, processedCount] : [op.POP],
							[op.POP_CURR_POS],
							[op.PUSH_FAILED]
						)
					)
				);
			} else {
				if (context.pluck.length > 0) {
					return buildSequence(
						[op.PLUCK, node.elements.length + 1, context.pluck.length],
						context.pluck.map(eSP => context.sp - eSP)
					);
				}

				if (context.action) {
					functionIndex = addFunctionConst(
						False,
						Object.keys(context.env),
						context.action.code
					);

					return buildSequence(
						[op.LOAD_SAVED_POS, node.elements.length],
						buildCall(
							functionIndex,
							node.elements.length + 1,
							context.env,
							context.sp
						)
					);
				} else {
					return buildSequence([op.WRAP, node.elements.length], [op.NIP]);
				}
			}
		}

		return buildSequence(
			[op.PUSH_CURR_POS],
			buildElementsCode(node.elements, {
				sp: context.sp + 1,
				env: context.env,
				pluck: [],
				action: context.action,
			})
		);

	def labeled(self:Visitor, node:Labeled, context):
		let env = context.env;
		label = node.label;
		sp = context.sp + 1;

		if (label) {
			env = cloneEnv(context.env);
			context.env[node.label] = sp;
		}

		if (node.pick) {
			context.pluck.push(sp);
		}

		return generate(node.expression, {
			sp: context.sp,
			env,
			action: None,
		});
	

	def text(self:Visitor, node:Text, context):
		return buildSequence(
			[op.PUSH_CURR_POS],
			generate(node.expression, {
				sp: context.sp + 1,
				env: cloneEnv(context.env),
				action: None,
			}),
			buildCondition(
				node.match | 0,
				[op.IF_NOT_ERROR],
				buildSequence([op.POP], [op.TEXT]),
				[op.NIP]
			)
		);
	

	def simple_and(self:Visitor, node:Simple_And, context):
		return buildSimplePredicate(node.expression, False, context);
	

	def simple_not(self:Visitor, node:Simple_Not, context):
		return buildSimplePredicate(node.expression, True, context);
	

	def optional(self:Visitor, node:Optional, context):
		return buildSequence(
			generate(node.expression, {
				sp: context.sp,
				env: cloneEnv(context.env),
				action: None,
			}),
			buildCondition(
				# Check expression match, not the node match
				# If expression always match, no need to replace FAILED to NULL,
				# because FAILED will never appeared
				-(node.expression.match | 0),
				[op.IF_ERROR],
				buildSequence([op.POP], [op.PUSH_NULL]),
				[]
			)
		);
	

	def zero_or_more(self:Visitor, node:Zero_or_More, context):
		expressionCode = generate(node.expression, {
			sp: context.sp + 1,
			env: cloneEnv(context.env),
			action: None,
		});

		return buildSequence(
			[op.PUSH_EMPTY_ARRAY],
			expressionCode,
			buildAppendLoop(expressionCode),
			[op.POP]
		);
	

	def one_or_more(self:Visitor, node:One_or_More, context) {
		expressionCode = generate(node.expression, {
			sp: context.sp + 1,
			env: cloneEnv(context.env),
			action: None,
		});

		return buildSequence(
			[op.PUSH_EMPTY_ARRAY],
			expressionCode,
			buildCondition(
				# Condition depends on the expression match, not the node match
				node.expression.match | 0,
				[op.IF_NOT_ERROR],
				buildSequence(buildAppendLoop(expressionCode), [op.POP]),
				buildSequence([op.POP], [op.POP], [op.PUSH_FAILED])
			)
		);
	

	def group(self:Visitor, node:Group, context) {
		return generate(node.expression, {
			sp: context.sp,
			env: cloneEnv(context.env),
			action: None,
		});
	

	def semantic_and(self:Visitor, node, context) {
		return buildSemanticPredicate(node, False, context);
	

	def semantic_not(self:Visitor, node:Semantic_Not, context) {
		return buildSemanticPredicate(node, True, context);
	

	def rule_ref(self:Visitor, node:Class, options:dict[str, Any]):
		return [op.RULE, asts.indexOfRule(ast, node.name)];
	

	def literal(self:Visitor, node:Class, options:dict[str, Any]):
		if (node.value.length > 0) {
			match = node.match | 0;
			# String only required if condition is generated or string is
			# case-sensitive and node always match
			need= match == SOMETIMES_MATCH
										or (match == ALWAYS_MATCH and !node.ignoreCase);
			stringIndex = needConst
				? addLiteralConst(
					node.ignoreCase ? node.value.toLowerCase() : node.value
				)
				: None;
			# Expectation not required if node always match
			expectedIndex = (match != ALWAYS_MATCH)
				? addExpectedConst({
					type: "literal",
					value: node.value,
					ignoreCase: node.ignoreCase,
				})
				: None;

			# For case-sensitive strings the value must match the beginning of the
			# remaining input exactly. As a result, we can use |ACCEPT_STRING| and
			# save one |substr| call that would be needed if we used |ACCEPT_N|.
			return buildCondition(
				match,
				node.ignoreCase
					? [op.MATCH_STRING_IC, stringIndex]
					: [op.MATCH_STRING, stringIndex],
				node.ignoreCase
					? [op.ACCEPT_N, node.value.length]
					: [op.ACCEPT_STRING, stringIndex],
				[op.FAIL, expectedIndex]
			);
		}

		return [op.PUSH_EMPTY_STRING];
	

	def _class(self:Visitor, node:Class, options:dict[str, Any]):
		match = node.match | 0;
		# Character class constant only required if condition is generated
		classIndex = match == SOMETIMES_MATCH ? addClassConst(node) : None;
		# Expectation not required if node always match
		expectedIndex = (match != ALWAYS_MATCH)
			? addExpectedConst({
				type: "class",
				value: node.parts,
				inverted: node.inverted,
				ignoreCase: node.ignoreCase,
			})
			: None;

		return buildCondition(
			match,
			[op.MATCH_CHAR_CLASS, classIndex],
			[op.ACCEPT_N, 1],
			[op.FAIL, expectedIndex]
		);
	

	def any(self:Visitor, node:Class, options:dict[str, Any]):
		match = node.match | 0;
		# Expectation not required if node always match
		expectedIndex = (match != ALWAYS_MATCH)
			? addExpectedConst({
				type: "any",
			})
			: None;

		return buildCondition(
			match,
			[op.MATCH_ANY],
			[op.ACCEPT_N, 1],
			[op.FAIL, expectedIndex]
		);

	generate = visitor.build({
		
	});

	generate(ast);
}


