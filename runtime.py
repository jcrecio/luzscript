from typing import Any, Dict, List
"""
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
        if not tokens:
            return None
            
        i = 0
        last_result = None
        
        while i < len(tokens):
            token = tokens[i]
            
            if token == 'var':
                if i + 1 >= len(tokens):
                    raise SyntaxError("Se esperaba un nombre de variable después de 'var'")
                name = tokens[i + 1]
                if i + 2 < len(tokens) and tokens[i + 2] == '=':
                    if i + 3 >= len(tokens):
                        raise SyntaxError("Se esperaba un valor después del '='")
                    expr_end = i + 4
                    while expr_end < len(tokens) and tokens[expr_end] != ';':
                        expr_end += 1
                    value = self.evaluate_expression(tokens[i + 3:expr_end])
                    self.variables[name] = value
                    i = expr_end
                else:
                    self.variables[name] = None
                    i += 2
                    
            elif token in self.variables and i + 1 < len(tokens) and tokens[i + 1] == '=':
                expr_end = i + 3
                while expr_end < len(tokens) and tokens[expr_end] != ';':
                    expr_end += 1
                value = self.evaluate_expression(tokens[i + 2:expr_end])
                self.variables[token] = value
                i = expr_end
                
            elif token == 'imprimir':
                if i + 1 >= len(tokens) or tokens[i + 1] != '(':
                    raise SyntaxError("Se esperaba '(' después de 'imprimir'")
                end_paren = self.find_matching_paren(tokens, i + 1)
                if i + 2 >= end_paren:
                    print()
                else:
                    result = self.evaluate_expression(tokens[i + 2:end_paren])
                    print(result)
                i = end_paren + 1
                    
            else:
                i += 1
                
        return last_result

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