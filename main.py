import logging
from lark import Lark, exceptions, Tree
from colorama import init, Fore
from lisp_transformer import LispTransformer

# 設定日誌
logger = logging.getLogger("mlisp")

# 加載 Lark 解析器
def load_parser():
    with open("lisp_grammar.lark", "r", encoding="utf-8") as file:
        grammar = file.read()
    parser = Lark(grammar, start='program', parser='lalr')
    return parser

# 遞歸執行語法樹節點
def eval_expr(tree, transformer):
    if isinstance(tree, Tree):
        # 根據節點類型分派處理
        if tree.data == "program":
            # 遍歷每個子節點，執行並收集結果
            results = []
            for child in tree.children:
                result = eval_expr(child, transformer)
                if result is not None:
                    results.append(result)
            return results

        elif tree.data == "eval_expr":
            # 對 `eval_expr` 節點進行遞歸處理
            return eval_expr(tree.children[0], transformer)

        elif tree.data == "define_func":
            var_name = tree.children[0].value  # 第一個子節點是變數名稱
            value = eval_expr(tree.children[1], transformer)  # 第二個子節點是變數值
            return transformer.define_func([var_name, value])

        elif tree.data == "print_num":
            value = eval_expr(tree.children[0], transformer)  # 評估子節點
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

# 解釋器主程序
def interpret_lisp(code: str):
    parser = load_parser()

    try:
        # 解析程式碼
        tree = parser.parse(code)
    except exceptions.LarkError as e:
        print(f"Syntax Error: {e}")
        if isinstance(e, exceptions.UnexpectedToken):
            print(f"Unexpected token: {e.token}")
            print(f"Expected: {e.expected}")
            print(f"Location: Line {e.line}, Column {e.column}")
            print(f"Previous tokens: {e.token_history}")
        return None

    # 顯示解析的語法樹 (Debug 用)
    # print("Parsed Tree:")
    # print(tree.pretty())

    # 使用 Transformer 執行 LISP 程式
    transformer = LispTransformer()
    try:
        result = eval_expr(tree, transformer)  # 傳遞語法樹和 Transformer
    except ValueError as e:
        print(f"Runtime Error: {e}")
        return None

    return result

# 初始化 colorama
init(autoreset=True)

if __name__ == "__main__":
    # 要執行的檔案
    test_files = [
        "public_test_data/01_1.lsp",
        "public_test_data/01_2.lsp",
        "public_test_data/02_1.lsp",
        "public_test_data/02_2.lsp",
        "public_test_data/03_1.lsp",
        "public_test_data/03_2.lsp",
        "public_test_data/04_1.lsp",
        "public_test_data/04_2.lsp",
        "public_test_data/05_1.lsp",
        "public_test_data/05_2.lsp",
        "public_test_data/06_1.lsp",
        "public_test_data/06_2.lsp"
    ]

    # 依序執行每個檔案
    for file_path in test_files:
        print(Fore.LIGHTBLUE_EX + f"執行檔案: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        interpret_lisp(code)
