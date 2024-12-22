import logging
from lark import Lark, exceptions
from lisp_transformer import LispTransformer

# 設定日志
logger = logging.getLogger("mlisp")

# 加載 Lark 解析器
def load_parser():
    with open("lisp_grammer.lark", "r", encoding="utf-8") as file:
        grammar = file.read()
    parser = Lark(grammar, start='program', parser='lalr')
    return parser

# 解釋器主程序
def interpret_lisp(code: str):
    # 讀取並解析程式碼
    parser = load_parser()
    
    try:
        tree = parser.parse(code)
    except exceptions.LarkError as e:
        print(f"Syntax Error: {e}")
        if isinstance(e, exceptions.UnexpectedToken):
            print(f"Unexpected token: {e.token}")
            print(f"Expected: {e.expected}")
            print(f"Location: Line {e.line}, Column {e.column}")
            print(f"Previous tokens: {e.token_history}")
        return

    # 顯示解析的語法樹 (debug 用)
    # print("Parsed Tree:", tree)

    # 使用 Transformer 執行 LISP 程式
    transformer = LispTransformer()
    result = eval_expr(tree, transformer)  # 傳遞語法樹和 transformer 物件
    return result

def eval_expr(tree, transformer):
    # 如果是 program 節點，遞迴處理其子節點
    if tree.data == 'program':
        results = []
        for child in tree.children:
            result = eval_expr(child, transformer)
            if result is not None:
                results.append(result)
        return results

    # 如果是 eval_expr 節點，處理其中的子節點
    elif tree.data == 'eval_expr':
        # eval_expr 的子節點是 print_num 或其他表達式
        return eval_expr(tree.children[0], transformer)

    # 處理 print_num 節點
    elif tree.data == 'print_num':
        num_val = eval_expr(tree.children[0], transformer)
        return transformer.print_num([num_val])

    # 處理 print_bool 節點
    elif tree.data == 'print_bool':
        bool_val = eval_expr(tree.children[0], transformer)
        return transformer.print_bool([bool_val])

    # 處理布林值
    elif tree.data == 'boolean':
        return transformer.boolean(tree.children[0])

    # 處理 number 節點
    elif tree.data == 'number':
        return transformer.number(tree.children[0])

    # 處理加法
    elif tree.data == 'plus':
        return transformer.plus([eval_expr(child, transformer) for child in tree.children])

    # 處理減法
    elif tree.data == 'minus':
        return transformer.minus([eval_expr(child, transformer) for child in tree.children])

    # 處理乘法
    elif tree.data == 'mult':
        return transformer.mult([eval_expr(child, transformer) for child in tree.children])

    # 處理除法
    elif tree.data == 'div':
        return transformer.div([eval_expr(child, transformer) for child in tree.children])

    # 處理取餘
    elif tree.data == 'mod':
        return transformer.mod([eval_expr(child, transformer) for child in tree.children])

    # 處理大於
    elif tree.data == 'greater':
        return transformer.greater([eval_expr(child, transformer) for child in tree.children])

    # 處理小於
    elif tree.data == 'smaller':
        return transformer.smaller([eval_expr(child, transformer) for child in tree.children])

    # 處理等於
    elif tree.data == 'equal':
        return transformer.equal([eval_expr(child, transformer) for child in tree.children])

    # 處理邏輯運算
    elif tree.data == 'and_op':
        return transformer.and_op([eval_expr(child, transformer) for child in tree.children])

    elif tree.data == 'or_op':
        return transformer.or_op([eval_expr(child, transformer) for child in tree.children])

    elif tree.data == 'not_op':
        return transformer.not_op([eval_expr(child, transformer) for child in tree.children])

    # 處理 if 表達式
    elif tree.data == 'if_expr':
        args = [eval_expr(child, transformer) for child in tree.children]
        return transformer.if_expr(args)

    # 其他情況
    else:
        print(f"Unknown expression: {tree.data}")
        return None

# 測試範例
if __name__ == "__main__":
    with open("public_test_data/05_2.lsp", "r", encoding="utf-8") as file:
        code = file.read()

    interpret_lisp(code)
