from decimal import Decimal, getcontext


class Calculate:
	getcontext().prec = 10

	@staticmethod
	def evaluate_simple_expression(expression):
		expression = expression.replace(" ", "")
		expression = expression.replace(',', '.')

		# Create list of numbers and operators
		elements = []
		current_number = ""
		for char in expression:
			if char.isdigit() or char == '.':
				current_number += char
			else:
				if current_number:
					elements.append(current_number)
					current_number = ""
				elements.append(char)
		if current_number:
			elements.append(current_number)

		# Create negation in numbers
		i = 0
		while i < len(elements):
			if elements[i] == '-' and (i == 0 or elements[i - 1] in ['(', '+', '-', '×', '÷']):
				elements[i] += elements[i + 1]
				elements.pop(i + 1)
			else:
				i += 1

		# Performs multiplication and division
		i = 0
		while i < len(elements):
			if elements[i] in ['×', '÷']:
				left = Decimal(elements[i - 1])
				right = Decimal(elements[i + 1])
				if elements[i] == '÷' and right == 0:
					return "Error: division by zero"
				result = left * right if elements[i] == '×' else left / right
				elements[i - 1:i + 2] = [str(result)]
			else:
				i += 1

		# Performs addition and subtraction
		result = Decimal(elements[0])
		i = 1
		while i < len(elements):
			if elements[i] == '+':
				result += Decimal(elements[i + 1])
			elif elements[i] == '-':
				result -= Decimal(elements[i + 1])
			i += 2
		return result.to_eng_string()

	@staticmethod
	def evaluate_expression(expression):
		# A helper function for evaluating expressions in brackets
		def evaluate_subexpression(subexpression):
			return str(Calculate.evaluate_expression(subexpression))

		# Find first bracket
		closing_index = expression.find(')')
		if closing_index != -1:
			# Find first bracket before close
			opening_index = expression[:closing_index].rfind('(')
			if opening_index != -1:
				# Evaluate expression in bracket
				subexpression = expression[opening_index + 1: closing_index]
				result = evaluate_subexpression(subexpression)
				result = str(Calculate.evaluate_simple_expression(result))
				modified_expression = expression[:opening_index] + result + expression[closing_index + 1:]
				return Calculate.evaluate_expression(modified_expression)
		expression = Calculate.evaluate_simple_expression(expression)
		if expression == "ZeroDivision":
			expression = "ZeroDivision"
			return expression
		return expression
