from lark import Lark, exceptions, Tree
from colorama import init, Fore

class LispTransformer:
    def __init__(self):
        self.variables = {}

    def define_func(self, args):
        var_name, value = args
        self.variables[var_name] = value
        return f"{var_name} 定義為 {value}"

    def print_num(self, args):
        value = int(args[0])
        print(Fore.LIGHTGREEN_EX + f"{value}")
        return value

    def print_bool(self, args):
        if args[0] == "#t" or args[0] == True:
            value = "#t"
        elif args[0] == "#f" or args[0] == False:
            value = "#f"
        print(Fore.LIGHTGREEN_EX + f"{value}")
        return value

    def plus(self, args):
        return sum(args)

    def minus(self, args):
        result = args[0]
        for arg in args[1:]:
            result -= arg
        return result

    def mult(self, args):
        result = 1
        for arg in args:
            result *= arg
        return result

    def div(self, args):
        result = args[0]
        for arg in args[1:]:
            if arg == 0:
                raise ZeroDivisionError("除以零")
            result //= arg
        return result

    def mod(self, args):
        return args[0] % args[1]

    def greater(self, args):
        return args[0] > args[1]

    def smaller(self, args):
        return args[0] < args[1]

    def equal(self, args):
        return args[0] == args[1]

    def and_op(self, args):
        return all(args)

    def or_op(self, args):
        return any(args)

    def not_op(self, args):
        return not args[0]

    def if_expr(self, args):
        condition, true_branch, false_branch = args
        return true_branch if condition else false_branch

    def number(self, value):
        return int(value)

    def boolean(self, value):
        if value == "#t":
            return True
        elif value == "#f":
            return False

def load_parser():
    with open("lisp_grammar.lark", "r", encoding="utf-8") as file:
        grammar = file.read()
    parser = Lark(grammar, start='program', parser='lalr')
    return parser

def eval_expr(tree, transformer):
    if isinstance(tree, Tree):
        if tree.data == "program":
            results = []
            for child in tree.children:
                result = eval_expr(child, transformer)
                if result is not None:
                    results.append(result)
            return results

        elif tree.data == "eval_expr":
            return eval_expr(tree.children[0], transformer)

        elif tree.data == "define_func":
            var_name = tree.children[0].value
            value = eval_expr(tree.children[1], transformer)
            return transformer.define_func([var_name, value])

        elif tree.data == "print_num":
            value = eval_expr(tree.children[0], transformer)
            return transformer.print_num([value])

        elif tree.data == "print_bool":
            value = eval_expr(tree.children[0], transformer)
            return transformer.print_bool([value])

        elif tree.data == "plus":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.plus(args)

        elif tree.data == "minus":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.minus(args)

        elif tree.data == "mult":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.mult(args)

        elif tree.data == "div":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.div(args)

        elif tree.data == "mod":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.mod(args)

        elif tree.data == "greater":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.greater(args)

        elif tree.data == "smaller":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.smaller(args)

        elif tree.data == "equal":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.equal(args)

        elif tree.data == "and_op":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.and_op(args)

        elif tree.data == "or_op":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.or_op(args)

        elif tree.data == "not_op":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.not_op(args)

        elif tree.data == "if_expr":
            args = [eval_expr(child, transformer) for child in tree.children]
            return transformer.if_expr(args)

        elif tree.data == "number":
            return transformer.number(tree.children[0].value)

        elif tree.data == "boolean":
            return transformer.boolean(tree.children[0].value)

        elif tree.data == "variable":
            var_name = tree.children[0].value
            if var_name in transformer.variables:
                return transformer.variables[var_name]
            else:
                raise ValueError(f"未定義的變數: {var_name}")

        else:
            raise ValueError(f"未知的節點類型: {tree.data}")
    else:
        raise ValueError(f"無法處理的節點類型: {type(tree)}")

def interpret_lisp(code: str):
    parser = load_parser()
    try:
        tree = parser.parse(code)
    except exceptions.LarkError as e:
        print(Fore.RED + f"語法錯誤: {e}")
        return None

    transformer = LispTransformer()
    try:
        result = eval_expr(tree, transformer)
    except ValueError as e:
        print(Fore.RED + f"執行錯誤: {e}")
        return None

    return result

if __name__ == "__main__":
    init(autoreset=True)
    test_files = []

    for i in range(1, 7):
        test_files.append(f"public_test_data/0{i}_1.lsp")
        test_files.append(f"public_test_data/0{i}_2.lsp")

    for file_path in test_files:
        print(Fore.LIGHTBLUE_EX + f"執行檔案: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        interpret_lisp(code)
