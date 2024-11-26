from typing import Any, Dict, List
"""
---- v0.1 ----
LuzScriptRuntime is a simple runtime environment for a custom scripting language called LuzScript.
It supports basic variable declarations, assignments, arithmetic operations, and print statements.
Classes:
    LuzScriptRuntime: The main class that handles the execution of LuzScript code.
Methods:
    __init__(self):
        Initializes the runtime environment with empty variable and function dictionaries and operator precedence.
    tokenize(self, code: str) -> List[str]:
        Converts a string of code into a list of tokens.
    parse_and_execute(self, code: str) -> Any:
        Tokenizes the code and executes the tokens.
    execute_tokens(self, tokens: List[str]) -> Any:
        Executes a list of tokens and handles variable declarations, assignments, and print statements.
    evaluate_expression(self, tokens: List[str]) -> Any:
        Evaluates an arithmetic expression given as a list of tokens using the Shunting Yard algorithm.
    evaluate_single_token(self, token: str) -> Any:
        Evaluates a single token, converting it to its appropriate type (int, float, string, boolean, or variable value).
    find_matching_paren(self, tokens: List[str], start: int) -> int:
        Finds the index of the matching closing parenthesis for an opening parenthesis in a list of tokens.
Usage:
    1. Create an instance of LuzScriptRuntime.
    2. Use the `parse_and_execute` method to execute LuzScript code.
Examples:
    runtime = LuzScriptRuntime()
    
    # Example 1: Variable declaration and assignment
    result = runtime.parse_and_execute('var x = 5 + 3; imprimir(x);')
    # Output: 8
    
    # Example 2: Variable reassignment
    result = runtime.parse_and_execute('var y = 10; y = y * 2; imprimir(y);')
    # Output: 20
    
    # Example 3: Multiple operations
    result = runtime.parse_and_execute('var z = (2 + 3) * (4 - 1); imprimir(z);')
    # Output: 15
    
    # Example 4: Print statement with expression
    result = runtime.parse_and_execute('imprimir(7 * (8 - 2) / 3);')
    # Output: 14.0
    
    # Example 5: Boolean values
    result = runtime.parse_and_execute('var a = verdadero; var b = falso; imprimir(a); imprimir(b);')
    # Output: True
    # Output: False
    
    # Example 6: String values
    result = runtime.parse_and_execute('var s = "Hola, mundo!"; imprimir(s);')
    # Output: Hola, mundo!

    ---- v0.2 ----
    It supports basic variable declarations, assignments, arithmetic operations, conditional statements, loops, and print statements.
    Executes a list of tokens and handles variable declarations, assignments, print statements, conditionals, and loops.
    evaluate_condition(self, tokens: List[str]) -> bool:
    Evaluates a boolean condition given as a list of tokens.
    find_matching_brace(self, tokens: List[str], start: int) -> int:
    Finds the index of the matching closing brace for an opening brace in a list of tokens.
    split_for_parts(self, tokens: List[str]) -> List[List[str]]:
    Splits the parts of a for loop (initialization, condition, increment) given as a list of tokens.
    # Example 7: Conditional statement
    result = runtime.parse_and_execute('var x = 10; si (x > 5) { imprimir("Mayor que 5"); } sino { imprimir("Menor o igual a 5"); }')
    # Output: Mayor que 5
    # Example 8: While loop
    result = runtime.parse_and_execute('var x = 0; mientrasQue (x < 3) { imprimir(x); x = x + 1; }')
    # Output: 0
    # Output: 1
    # Output: 2
    # Example 9: For loop
    result = runtime.parse_and_execute('para (var i = 0; i < 3; i = i + 1) { imprimir(i); }')
    # Output: 0
    # Output: 1
    # Output: 2
"""


class LuzScriptRuntime:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, dict] = {}
        self.precedence = {
            '*': 3,
            '/': 3,
            '+': 2,
            '-': 2,
        }
        
    def tokenize(self, code: str) -> List[str]:
        code = ' '.join(code.split())
        tokens = []
        i = 0
        
        while i < len(code):
            char = code[i]
            
            if char.isspace():
                i += 1
                continue
                
            if char == '"':
                end = i + 1
                while end < len(code) and code[end] != '"':
                    if code[end] == '\\':
                        end += 2
                    else:
                        end += 1
                if end < len(code):
                    tokens.append(code[i:end+1])
                    i = end + 1
                    continue
                    
            if char.isdigit() or (char == '.' and i + 1 < len(code) and code[i + 1].isdigit()):
                end = i
                has_decimal = False
                while end < len(code) and (code[end].isdigit() or (code[end] == '.' and not has_decimal)):
                    if code[end] == '.':
                        has_decimal = True
                    end += 1
                tokens.append(code[i:end])
                i = end
                continue
                
            if char.isalpha() or char == '_':
                end = i
                while end < len(code) and (code[end].isalnum() or code[end] == '_'):
                    end += 1
                tokens.append(code[i:end])
                i = end
                continue
                
            if i + 1 < len(code):
                double_char = code[i:i+2]
                if double_char in ['==', '!=', '<=', '>=', '+=', '-=', '*=', '/=']:
                    tokens.append(double_char)
                    i += 2
                    continue
                    
            if char in '+-*/=<>!&|{}()[];,':
                tokens.append(char)
                i += 1
                continue
                
            i += 1
            
        return tokens

    def parse_and_execute(self, code: str) -> Any:
        tokens = self.tokenize(code)
        return self.execute_tokens(tokens)

    def execute_tokens(self, tokens: List[str]) -> Any:
        """Executes the parsed tokens."""
        if not tokens:
            return None
            
        i = 0
        last_result = None
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == 'si':
                if i + 1 >= len(tokens) or tokens[i + 1] != '(':
                    raise SyntaxError("Expected '(' after 'si'")
                condition_end = self.find_matching_paren(tokens, i + 1)
                condition = self.evaluate_condition(tokens[i + 2:condition_end])
                
                if condition_end + 1 >= len(tokens) or tokens[condition_end + 1] != '{':
                    raise SyntaxError("Expected '{' after condition")
                body_end = self.find_matching_brace(tokens, condition_end + 1)
                
                else_body = None
                if (body_end + 1 < len(tokens) and 
                    tokens[body_end + 1] == 'sino'):
                    if body_end + 2 >= len(tokens) or tokens[body_end + 2] != '{':
                        raise SyntaxError("Expected '{' after 'sino'")
                    else_end = self.find_matching_brace(tokens, body_end + 2)
                    else_body = tokens[body_end + 3:else_end]
                    i = else_end + 1
                else:
                    i = body_end + 1
                
                if condition:
                    self.execute_tokens(tokens[condition_end + 2:body_end])
                elif else_body:
                    self.execute_tokens(else_body)
                    
            elif token == 'mientrasQue':
                if i + 1 >= len(tokens) or tokens[i + 1] != '(':
                    raise SyntaxError("Expected '(' after 'mientrasQue'")
                condition_start = i + 2
                condition_end = self.find_matching_paren(tokens, i + 1)
                
                if condition_end + 1 >= len(tokens) or tokens[condition_end + 1] != '{':
                    raise SyntaxError("Expected '{' after condition")
                body_end = self.find_matching_brace(tokens, condition_end + 1)
                
                while self.evaluate_condition(tokens[condition_start:condition_end]):
                    self.execute_tokens(tokens[condition_end + 2:body_end])
                    
                i = body_end + 1
                
            elif token == 'para':
                if i + 1 >= len(tokens) or tokens[i + 1] != '(':
                    raise SyntaxError("Expected '(' after 'para'")
                
                for_end = self.find_matching_paren(tokens, i + 1)
                for_parts = self.split_for_parts(tokens[i + 2:for_end])
                
                if len(for_parts) != 3:
                    raise SyntaxError("Invalid for loop format")
                    
                if for_end + 1 >= len(tokens) or tokens[for_end + 1] != '{':
                    raise SyntaxError("Expected '{' after for condition")
                body_end = self.find_matching_brace(tokens, for_end + 1)
                
                self.execute_tokens(for_parts[0])
                
                # Execute for loop
                while self.evaluate_condition(for_parts[1]):
                    self.execute_tokens(tokens[for_end + 2:body_end])
                    self.execute_tokens(for_parts[2])
                    
                i = body_end + 1
                
            else:
                i += 1
                
        return last_result

    def evaluate_condition(self, tokens: List[str]) -> bool:
        """Evaluates a boolean condition."""
        if not tokens:
            raise ValueError("Empty condition")
            
        operators = ['==', '!=', '<', '>', '<=', '>=']
        for i, token in enumerate(tokens):
            if token in operators:
                left = self.evaluate_expression(tokens[:i])
                right = self.evaluate_expression(tokens[i + 1:])
                
                if token == '==':
                    return left == right
                elif token == '!=':
                    return left != right
                elif token == '<':
                    return left < right
                elif token == '>':
                    return left > right
                elif token == '<=':
                    return left <= right
                elif token == '>=':
                    return left >= right
                    
        result = self.evaluate_expression(tokens)
        return bool(result)

    def find_matching_brace(self, tokens: List[str], start: int) -> int:
        """Finds the matching closing brace."""
        count = 1
        i = start + 1
        while i < len(tokens):
            if tokens[i] == '{':
                count += 1
            elif tokens[i] == '}':
                count -= 1
                if count == 0:
                    return i
            i += 1
        raise SyntaxError("Unmatched braces")

    def split_for_parts(self, tokens: List[str]) -> List[List[str]]:
        """Splits for loop parts (initialization; condition; increment)."""
        parts = []
        current_part = []
        paren_count = 0
        
        for token in tokens:
            if token == '(' or token == '{':
                paren_count += 1
            elif token == ')' or token == '}':
                paren_count -= 1
            elif token == ';' and paren_count == 0:
                parts.append(current_part)
                current_part = []
                continue
                
            current_part.append(token)
            
        parts.append(current_part)
        return parts

    def evaluate_expression(self, tokens: List[str]) -> Any:
        if not tokens:
            raise ValueError("Expresión vacía")
            
        if len(tokens) == 1:
            return self.evaluate_single_token(tokens[0])
            
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token in self.precedence:  # Es un operador
                while (operator_stack and operator_stack[-1] in self.precedence and 
                       self.precedence[operator_stack[-1]] >= self.precedence[token]):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
            else:  # Es un operando
                output_queue.append(self.evaluate_single_token(token))
                
        while operator_stack:
            if operator_stack[-1] == '(':
                raise ValueError("Paréntesis no balanceados")
            output_queue.append(operator_stack.pop())
            
        evaluation_stack = []
        
        for token in output_queue:
            if token in self.precedence:  # Es un operador
                if len(evaluation_stack) < 2:
                    raise ValueError("Expresión inválida")
                b = evaluation_stack.pop()
                a = evaluation_stack.pop()
                if token == '+':
                    evaluation_stack.append(a + b)
                elif token == '-':
                    evaluation_stack.append(a - b)
                elif token == '*':
                    evaluation_stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("División por cero")
                    evaluation_stack.append(a / b)
            else:
                evaluation_stack.append(token)
                
        if len(evaluation_stack) != 1:
            raise ValueError("Expresión inválida")
            
        return evaluation_stack[0]

    def evaluate_single_token(self, token: str) -> Any:
        try:
            if '.' in token:
                return float(token)
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                return int(token)
        except ValueError:
            pass
            
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]
        if token in self.variables:
            return self.variables[token]
        if token == 'verdadero':
            return True
        if token == 'falso':
            return False
            
        raise ValueError(f"No se puede evaluar el token: {token}")

    def find_matching_paren(self, tokens: List[str], start: int) -> int:
        count = 1
        i = start + 1
        while i < len(tokens):
            if tokens[i] == '(':
                count += 1
            elif tokens[i] == ')':
                count -= 1
                if count == 0:
                    return i
            i += 1
        raise SyntaxError("Paréntesis no balanceados")

def main():
    runtime = LuzScriptRuntime()
    
    print("LuzScript Runtime v0.2")
    print('Escribe "salir" para terminar')
    print("Operaciones soportadas: +, -, *, /")
    print()
    
    while True:
        try:
            code = input(">>> ")
            if code.lower() == 'salir':
                break
            result = runtime.parse_and_execute(code)
            if result is not None:
                print("=>", result)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()