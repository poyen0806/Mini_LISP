import logging

logger = logging.getLogger("mlisp")

class LispTransformer:
    def __init__(self):
        self.variables = {}

    # 定義變數
    def define_func(self, args):
        var_name = args[0]  # 變數名稱
        value = args[1]  # 表達式的值
        self.variables[var_name] = value
        return value

    # 解析數字
    def number(self, token):
        return int(token)

    # 解析布林值
    def boolean(self, token):
        if isinstance(token, str):
            return token == "#t"  # 字串 "#t" 轉換為 True，"#f" 轉換為 False
        return token  # 如果已經是布林值，直接返回
    
    # 查詢變數
    def variable(self, var_name):
        if var_name in self.variables:
            return self.variables[var_name]
        else:
            raise ValueError(f"未定義變數: {var_name}")
    
    # 數字運算
    def plus(self, args):
        return sum(args)

    def minus(self, args):
        return args[0] - sum(args[1:])

    def mult(self, args):
        result = 1
        for arg in args:
            result *= arg
        return result

    def div(self, args):
        if args[1] == 0:
            raise ValueError("除數不能為零")
        return args[0] // args[1]

    def mod(self, args):
        return args[0] % args[1]

    def greater(self, args):
        return args[0] > args[1]

    def smaller(self, args):
        return args[0] < args[1]

    def equal(self, args):
        return args[0] == args[1]

    # 邏輯運算
    def and_op(self, args):
        # 將每個參數轉換為布林值進行運算
        return all(self.boolean(arg) for arg in args)

    def or_op(self, args):
        # 將每個參數轉換為布林值進行運算
        return any(self.boolean(arg) for arg in args)

    def not_op(self, args):
        # 轉換為布林值後進行邏輯運算
        return not self.boolean(args[0])

    # if 表達式
    def if_expr(self, args):
        condition, true_expr, false_expr = args
        return true_expr if condition else false_expr

    # 打印語句
    def print_num(self, args):
        print(args[0])
        return args[0]

    def print_bool(self, args):
        print('#t' if self.boolean(args[0]) else '#f')  # 確保布林值正確處理
        return args[0]

    # 評估表達式
    def eval_expr(self, args):
        if isinstance(args, str):  # 假設是變數名稱
            return self.variable(args)
        elif isinstance(args, int):  # 數字
            return args
        else:
            raise ValueError(f"無法處理此表達式: {args}")
