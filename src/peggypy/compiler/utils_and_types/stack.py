


from typing import Callable, Literal, Optional


class Stack:
	"""Utility class that helps generating code for C-like languages."""
	
	sp:int
	maxSp:int
	varName:str
	ruleName:str

	# TODO: type is a reserved word
	# TODO: python may not require the type. all stack declarations in the output appear to be local variables... no need for global
	def __init__(self, ruleName:str, varName:str, type: Literal["let", "var"]): 
		"""
		Constructs the helper for tracking variable slots of the stack virtual machine
		
		### Parameters
		
		ruleName : str
			The name of rule that will be used in error messages
		varName : str
			The prefix for generated names of variables
		type
			The type of the variables. For JavaScript there are `var` or `let`
		"""
		# Last used variable in the stack.
		self.sp       = -1
		# Maximum stack size. */
		self.maxSp    = -1
		self.varName  = varName
		self.ruleName = ruleName
		self.type     = type
	

	def name(self, i:int) -> str:
		"""
		Returns name of the variable at the index `i`.
		
		### Parameters
		
		i : number
			Index for which name must be generated

		### Returns
		
		string
			Generated name
		
		### Raises
		
		IndexError
			If `i < 0`, which means a stack underflow (there are more `pop`s than `push`es)
		"""
		if i < 0:
			raise IndexError(
				f"Rule '{self.ruleName}': The variable stack underflow: attempt to use a variable '{self.varName}<x>' at an index {i}"
			)
		
		return f"{self.varName}{i}"
	

	def push(self, exprCode:str):
		"""
		Assigns `exprCode` to the new variable in the stack, returns generated code.
		As the result, the size of a stack increases on 1.

		### Parameters
		
		exprCode : string
			Any expression code that must be assigned to the new variable in the stack

		### Returns

		string
			Assignment code
		"""
		self.sp+=1

		code = f"{self.name(self.sp)} = {exprCode};";

		if self.sp > self.maxSp: 
			self.maxSp = self.sp

		return code


	def pop_many(self, n:int) -> list[str]:
		"""
		Returns the names of the `n` variables removed from the top of the stack.
				
		### Parameters 

		n : number
			Quantity of variables, which need to be removed from the stack
		
		### Returns
		
		list[string]
			Generated names. If `n > 1` than array has length of `n`
		
		### Raises
		
		IndexError
			If the stack underflow (there are more `pop`s than `push`es)
		"""
		self.sp -= n
		return [self.name(self.sp+1+i) for i in range(n)]


	def pop(self) -> str:
		"""
		Returns name of the variable removed from the top of the stack.
				
		### Returns
		
		string 
			Generated name
		
		### Raises
		
		IndexError
			If the stack underflow (there are more `pop`s than `push`es)
		"""
		
		result = self.name(self.sp)
		self.sp -= 1
		return result

	
	def top(self):
		"""
		 Returns name of the first free variable. The same as `index(0)`.
		
		### Returns
		
		str
			Generated name
		
		### Raises

		IndexError
			If the stack is empty (there was no `push`'s yet)
		"""
		return self.name(self.sp); 
		

	def index(self, i:int):
		"""
		Returns name of the variable at index `i`.

		### Parameters	

		i : Number
			Index of the variable from top of the stack
		
		### Returns
		
		str
			Generated name
			
		### Raises
		
		IndexError
			If `i < 0` or more than the stack size
		"""
		if i < 0:
			raise IndexError(
				f"Rule '{self.ruleName}': The variable stack overflow: attempt to get a variable at a negative index {i}"
			)

		return self.name(self.sp - i)
	

	# TODO: unused????
	def result(self):
		"""
		Returns variable name that contains result (bottom of the stack).
		
		### Returns 
		
		str
			Generated name
		
		### Raises
		
		IndexError
			If the stack is empty (there was no `push`es yet)

		"""
		if self.maxSp < 0:
			raise IndexError(
				f"Rule '{self.ruleName}': The variable stack is empty, can't get the result'"
			)

		return self.name(0)
	

	# TODO: unused????
	def defines(self):
		"""
		Returns defines of all used variables.
		
		### Returns
		
		str 
			Generated define variable expression with the type `self.type`.
			If the stack is empty, returns empty string
		"""
		if self.maxSp < 0:
			return ""
		return f"{self.type} {', '.join(self.name(i) for i in range(self.maxSp+1))};"
	

	# TODO: unused????
	def checkedIf(self, position:int, generateIf:Callable[[], None], generateElse:Optional[Callable[[], None]]=None):
		"""
		### Parameters

		pos : int
			Opcode number for error messages
		
		### Raises

		Error
			If `generateElse` is defined and the stack pointer moved differently in the
		    `generateIf` and `generateElse`
		"""
		stack_pointer_start = self.sp
		
		# TODO: This looks like it might be improved with a different approach?? lambdas dont feel like the right way to do side-effects in python?
		generateIf()

		if generateElse is not None:

			stack_pointer_after_if = self.sp
			
			# reset the stack pointer before calling the else arm
			self.sp = stack_pointer_start 
			generateElse()
			stack_pointer_after_else = self.sp

			# confirm that the stack pointer moved by the same amount in both the if and else arms
			if not stack_pointer_after_if == stack_pointer_after_else:
				raise Exception(
					f"Rule='{self.ruleName}', {position=}: " +
					"Branches of a condition can't move the stack pointer differently " +
					f"(before: {stack_pointer_start}, after then: {stack_pointer_after_if}, after else: {self.sp})."
				)
	
	 # TODO: unused????
	def checkedLoop(self, position:int, generateBody:Callable[..., None]):
		"""
		Checks that code in the `generateBody` do not move stack pointer.
		
		### Parameters

		pos: int
			Opcode number for error messages
		
		generateBody : Function
			Function that works with self.stack
		
		### Raises
		
		Exception
			If `generateBody` move the stack pointer (if it contains unbalanced `push`es and `pop`s)
		"""
		baseSp = self.sp

		generateBody()

		if not baseSp == self.sp:
			raise Exception(
				f"Rule '{self.ruleName}', position {position}: " +
				"Body of a loop can't move the stack pointer " +
				f"(before: {baseSp}, after: {self.sp})."
			)
