# Mini-LISP Interpreter

Author: Po Yen, Wu  
Email: leo33917888@gmail.com

This project implements a Mini-LISP interpreter in Python using the Lark parser library. It supports basic operations such as arithmetic and logical expressions, variable definitions, and printing. The interpreter also handles `if` expressions and allows variable assignment.

## Requirements
- `Python 3.9.x`
- `lark-parser==0.12.0`
- `colorama==0.4.6`

## Setting Up the Environment

To run this project, follow these steps:

1. Create a virtual environment (replace `.venv` with your preferred environment name):

    ```bash
    python -m venv .venv
    ```

2. Activate the virtual environment:

    - On Windows:

      ```bash
      ./.venv/Scripts/activate
      ```

    - On macOS/Linux:

      ```bash
      source .venv/bin/activate
      ```

3. Install the required dependencies (choose one method):

    ```bash
    pip install .
    ```

    Alternatively, you can manually install the required dependencies:

    ```bash
    pip install lark-parser==0.12.0
    pip install colorama==0.4.6
    ```

4. Execute the Python script:

   Once the dependencies are installed, you can run the Mini-LISP interpreter by executing the following command:

    ```bash
    python main.py
    ```

   This will start the interpreter and execute the test `.lsp` files specified in the `test_files` list in `main.py`.

5. Add your own `.lsp` files for testing:

    - To test your own Mini-LISP code, place `.lsp` files in the `public_test_data` folder.
    - Update the `test_files` list in `main.py` to include the path to your custom `.lsp` files.
  
6. Deactivate the virtual environment:

    - When you're done, you can deactivate the virtual environment by running the following command:

      ```bash
      deactivate
      ```

This will return you to your global environment.

## Files in this Project

This project includes the following files:

- **main.py**: The main Python script that implements the Mini-LISP interpreter.
- **lisp_grammar.lark**: The grammar file used by Lark to parse the Mini-LISP syntax.
- **pyproject.toml**: The Python project configuration file, which contains dependency and build information.
- **README.md**: The documentation for setting up and using the project.

There is also a folder for test `.lsp` files, `public_test_data`, where you can place your own `.lsp` files to test the interpreter.

You can add your own `.lsp` files in the `public_test_data` folder and modify the `test_files` list in `main.py` to include them.

## Example Lisp Code

Here is an example of a simple Lisp program:

```lisp
(define a (* 1 2 3 4))

(define b (+ 10 -5 -2 -1))

(print-num (+ a b))
```

This program defines a variable `a` by multiplying `1`, `2`, `3`, and `4`. It also defines a variable `b` by summing `10`, `-5`, `-2`, and `-1`, and then prints the sum of `a` and `b`.

The output of the example will be like `26`.

## Supported Features

### Basic Features

| Feature                | Description                                          | Points | Completed |
|------------------------|------------------------------------------------------|--------|-----------|
| 1. Syntax Validation    | Print “syntax error” when parsing invalid syntax    | 10     | ✔       |
| 2. Print                | Implement `print-num` statement                      | 10     | ✔       |
| 3. Numerical Operations | Implement all numerical operations                   | 25     | ✔       |
| 4. Logical Operations   | Implement all logical operations                     | 25     | ✔       |
| 5. `if` Expression      | Implement `if` expression                           | 8      | ✔       |
| 6. Variable Definition  | Able to define a variable                           | 8      | ✔       |
| 7. Function             | Able to declare and call an anonymous function      | 8      |         |
| 8. Named Function       | Able to declare and call a named function           | 6      |         |

### Bonus Features

| Feature                | Description                                          | Points | Completed |
|------------------------|------------------------------------------------------|--------|-----------|
| 1. Recursion            | Support recursive function call                     | 5      |         |
| 2. Type Checking        | Print error messages for type errors                | 5      |         |
| 3. Nested Function      | Nested function (static scope)                      | 5      |         |
| 4. First-class Function | Able to pass functions, support closure             | 5      |         |

## License
This project is licensed under the MIT License - see the LICENSE file for details.
