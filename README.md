# LuzScript v0.1
## Spanish programming language

LuzScript is a minimalist programming language inspired by C# and javascript, designed to be intuitive and accessible for spanish speakers. It includes a basic runtime implemented in Python that allows interactive execution of LuzScript code. 

## Features

- Simple
- Basic type system (integers, decimals, text, booleans)
- Mathematical operations with operator precedence
- Variables and assignments
- Built-in print function
- Interactive REPL (Read-Eval-Print Loop)

## Requirements

- Python 3.6 or higher

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/luzscript.git
cd luzscript
```

2. Run the runtime:
```bash
python luzscript.py
```

## Basic Syntax

### Variables and Data Types

```python
var name = "John"       // text
var age = 25           // integer
var price = 19.99      // decimal
var active = true      // boolean
```

### Mathematical Operations

LuzScript supports basic mathematical operations:
- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)

```python
var x = 5
var y = 3
var sum = x + y         // 8
var product = x * y     // 15
var complex = (x + y) * 2  // 16
```

### Operator Precedence

1. Parentheses `()`
2. Multiplication `*` and Division `/`
3. Addition `+` and Subtraction `-`

### Print Function

```python
imprimir("Hello World")
imprimir(2 + 2)
imprimir(name)
```

## Examples

### Basic Calculations
```python
>>> var x = 10
>>> var y = 5
>>> imprimir(x + y)
15
>>> imprimir(x * y)
50
```

### Complex Expressions
```python
>>> var result = (10 + 5) * (20 - 15) / 2
>>> imprimir(result)
37.5
```

### Text Handling
```python
>>> var firstName = "John"
>>> var lastName = "Doe"
>>> imprimir(firstName)
John
```

## Current Limitations

- No control structures (if, while, for)
- No user-defined functions
- No classes or objects
- Mathematical operations limited to +, -, *, /
- No support for arrays or collections

## Internal Working

The LuzScript runtime works in three main steps:

1. **Tokenization**: Converts source code into a list of tokens
2. **Analysis**: Processes tokens to understand code structure
3. **Execution**: Executes the identified instructions

### Expression Evaluation Process

Mathematical expressions are evaluated using the Shunting Yard algorithm, which:
1. Converts the expression to reverse Polish notation
2. Respects operator precedence
3. Handles parentheses and grouping
4. Evaluates the resulting expression

## Next steps

1. Implement control structures
2. Add function support
3. Expand mathematical operations
4. Implement more robust error handling
5. Add collection support

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Inspired by C# syntax and structure
- Developed as an educational project to demonstrate compiler and interpreter concepts