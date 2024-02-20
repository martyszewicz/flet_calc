import re


class Expression:
    def __init__(self):
        self.expression = ""
        self.operations = "÷×-+"
        self.max_length = 28
        self.open_brackets = 0

    def handle_button_click(self, button):
        if button == "C":
            self.clear_expression()
        elif button == "<":
            self.remove_last_character()
        elif len(self.expression) < self.max_length:
            if button.isdigit():
                self.append_digit(button)
            elif button == ",":
                self.append_decimal_point()
            elif button in self.operations:
                self.append_operation(button)
            elif button == "+/-":
                self.negation()
            elif button == "( )":
                self.brackets()
        return self.expression

    def clear_expression(self):
        self.expression = ""

    def remove_last_character(self):
        if self.expression:
            self.expression = self.expression[:-1]

    def append_digit(self, digit):
        if self.expression == "0":
            self.expression = digit
        else:
            self.expression += digit

    def append_decimal_point(self):
        if len(self.expression) == 0 or self.expression[-1] in self.operations or self.expression[-1] == "(":
            self.expression += "0,"
            return self.expression
        if self.expression[-1] == ")":
            self.expression += "×0,"
        if self.expression != "":
            numbers = re.findall(r'[-+]?\d[\d,.]*', self.expression)
            if numbers:
                last_number = numbers[-1]
                if "," in last_number:
                    return self.expression
        else:
            self.expression += "0"
        self.expression += ","
        return self.expression

    def append_operation(self, operation):
        if len(self.expression) != 0:
            if self.expression[-1] == "-" and self.expression[-2] == "(":
                return self.expression
            if self.expression[-1] == "(" and (operation == "÷" or operation == "×" or operation == "+"):
                return self.expression
            if self.expression and self.expression[-1] not in self.operations:
                self.expression += operation
                return self.expression
            if self.expression[-1] in self.operations:
                self.remove_last_character()
                self.expression += operation
                return self.expression

    def negation(self):
        if self.expression == "(-":
            self.expression = ""
            return self.expression
        if len(self.expression) == 0:
            self.expression += "(-"
            return self.expression
        if self.expression[-1] == "(":
            self.expression += "-"
            return self.expression
        if self.expression[-1] == "-" and self.expression[-2] == "(":
            self.expression = self.expression[:-2]
            return self.expression
        if len(self.expression) != 0 and self.expression[-1] == "-" or len(self.expression) != 0 and self.expression[-1] == "+":
            self.expression += "(-"
            return self.expression
        if self.expression[-1] in self.operations:
            self.expression += "(-"
            return self.expression
        if self.expression[-1] == ")":
            self.expression += "×(-"
        if self.expression[-1].isdigit() or self.expression[-1] == ",":
            numbers = re.findall(r'[-+]?\d[\d,.]*', self.expression)
            last_number = numbers[-1]
            self.expression = self.expression[:-len(last_number)]
            if self.expression:
                if "-" in last_number:
                    self.expression = self.expression[:-1]+last_number[1:]
                elif self.expression[-1] == "×" or self.expression[-1] == "÷":
                    self.expression += "(-" + last_number
                else:
                    if self.expression[-1] == "(":
                        self.expression = self.expression + "-" + last_number
                    else:
                        self.expression += last_number[0] + "(-" + last_number[1:]
            else:
                self.expression = "(-" + last_number

    def brackets(self):
        self.open_brackets = self.expression.count("(") - self.expression.count(")")
        if len(self.expression) == 0:
            self.expression += "("
            return self.expression
        if self.expression[-1] in self.operations:
            self.expression += "("
            return self.expression
        if self.expression[-1] == "(":
            self.expression += "("
            return self.expression
        if (self.expression[-1].isdigit() or self.expression[-1] == ",") and self.open_brackets != 0:
            self.expression += ")"
            return self.expression
        if (self.expression[-1].isdigit() or self.expression[-1] == ",") and self.open_brackets == 0:
            self.expression += "×("
            return self.expression
        if self.expression[-1] == ")" and self.open_brackets != 0:
            self.expression += ")"
            return self.expression
        if self.expression[-1] == ")" and self.open_brackets == 0:
            self.expression += "×("
            return self.expression
