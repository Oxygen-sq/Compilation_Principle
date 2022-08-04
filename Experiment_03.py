#!/user/bin/env python3
# -*- coding: utf-8 -*-

'''
E->E+T | E-T | T
T->T*F | T/F | F
F->(E) | num
'''

import sys

# 终结字符种别编码:+ - * / ( ) num
Final = ["+", "-", "*", "/", "(", ")", "n", "#"]

# 非终结字符
NotFinal = ['E', 'T', 'F']

# 模拟符号栈
s = []

# 保存所有字符
strAll = []

# 数字计数
Index = 0
Temp_Arr = []
N_Index = 100

# 输入算术表达式
InputStr = []

# 结果
Result = [[], []]

# 保存词法分析后的字符及种别编码
Result_Lex = [[], []]

# 空格或换行
Blank = {" ", "\n"}

# 表达式的种别编码
Num = []

# 算符优先关系
Data = [["0" for i in range(8)] for i in range(8)]

# firstvt集合
firstvt = [[], [], []]

# lastvt集合
lastvt = [[], [], []]

# 文法
text = ["E~>E+T|E-T|T", "T~>T*F|T/F|F", "F~>(E)|n"]
text_2 = ["E~>E+T", "E~>E-T", "E~>T", "T~>T*F",
          "T~>T/F", "T~>F", "F~>(E)", "F~>n"]
In_Str = []

# 保留关键字及种别编码
Static_word = {"begin": 1, "end": 2, "if": 3, "then": 4, "while": 5,
               "do": 6, "const": 7, "var": 8, "call": 9, "procedure": 10}

# 中文说明
Explanation = ["保留字标识符", "加号", "减号", "乘号", "除号", "odd运算符", "等于号", "不等于号", "小于号",
               "大于号", "小于等于号", "大于等于", "赋值符号", "左括号", "右括号", "点号", "逗号", "分号", 
               "常数", "非保留字标识符"]

# 算符和界符及种别编码
Punctuation_marks = {"+": 11, "-": 12, "*": 13, "/": 14, "odd": 15, "=": 16, "<>": 17, "<": 18, ">": 19,
                     "<=": 20, ">=": 21, ":=": 22, "(": 23, ")": 24, ".": 25, ",": 26, ";": 27}


# 求FIRSTVT集
def FirstVt(ch):
    i = 0
    while i < len(text):
        if text[i][0] == ch:
            break
        else:
            i += 1

    # 获取文法的所指部分
    gs = text[i].split("~>")[1]
    gs = gs.split("|")
    for j in gs:
        if (j[0] in Final) and (j[0] not in firstvt[i]):
            firstvt[i].append(j[0])
        elif len(j) > 1 and (j[0] == ch) and (j[1] in Final) and (j[1] not in firstvt[i]):
            firstvt[i].append(j[1])
        else:
            i += 1
            FirstVt(j[0])
            for n in firstvt[i]:
                if n not in firstvt[i - 1]:
                    firstvt[i - 1].append(n)
                else:
                    continue


# 求LASTVT集
def LastVt(ch):
    i = 0
    while i < len(text):
        if text[i][0] == ch:
            break
        else:
            i += 1

    # 获取文法的所指部分
    gs = text[i].split("~>")[1]
    gs = gs.split("|")
    for j in gs:
        if (j[-1] in Final) and (j[-1] not in lastvt[i]):
            lastvt[i].append(j[-1])
        elif len(j) > 1 and (j[-2] in Final) and j[-1] not in Final:
            if j[-2] not in lastvt[i]:
                lastvt[i].append(j[-2])
            else:
                continue
            x = i
            x += 1
            LastVt(j[-1])
            for n in lastvt[x]:
                if n not in lastvt[x - 1]:
                    lastvt[x - 1].append(n)
                else:
                    continue


# 求算术优先表
def table():
    # 获取独立文法的个数
    x = len(text_2)

    # 给各个非终结字符的FirstVt和LastVt集合添加对应长度
    for i in range(3):
        firstvt[i].insert(0, len(firstvt[i]))
        lastvt[i].insert(0, len(lastvt[i]))

    # 求每个终结符的推导结果(去掉"~>"后的转化文法，用于最后的归约
    for i in text_2:
        s = i.split("~>")
        s = s[0] + s[1]
        In_Str.append(s)


    i = 0
    # 循环每个单独文法
    while i < x:
        j = 1
        # 循环单独文法的第一至最后一个字符
        while j + 1 < len(text_2[i]):
            # 如果当前字符是终结字符且下一个字符也是终结字符
            if Terminator(text_2[i][j]) and Terminator(text_2[i][j + 1]):
                m = getIndex(text_2[i][j])
                n = getIndex(text_2[i][j + 1])
                Data[m][n] = "="
            # 如果当前字符是终结字符且下一个字符也不是终结字符且下下个字符是终结字符
            if ((j + 2 < len(text_2[i])) and Terminator(text_2[i][j]) and Terminator(text_2[i][j + 2]) and (
                    text_2[i][j + 1] not in Final)):
                m = getIndex(text_2[i][j])
                n = getIndex(text_2[i][j + 2])
                Data[m][n] = '='
            # 如果当前字符是终结字符且下一个字符不是终结字符
            if Terminator(text_2[i][j]) and (text_2[i][j + 1] not in Final):
                k = 0
                while k < 3:
                    aa = NotFinal[k]
                    bb = text_2[i][j + 1]
                    if aa == bb:
                        break
                    k += 1
                m = getIndex(text_2[i][j])
                t = 0
                # if k == 3: break
                while t < firstvt[k][0]:
                    n = getIndex(firstvt[k][t + 1])
                    Data[m][n] = '<'
                    t += 1
            # 如果当前字符不是终结字符且下一个字符也不是终结字符
            if (text_2[i][j] not in Final) and Terminator(text_2[i][j + 1]):
                k = 0
                # 判断是哪一个非终结字符
                while k < 3:
                    if NotFinal[k] == text_2[i][j]:
                        break
                    k += 1
                n = getIndex(text_2[i][j + 1])
                t = 0
                if k != 3:
                    while t < lastvt[k][0]:
                        m = getIndex(lastvt[k][t + 1])
                        Data[m][n] = '>'
                        t += 1
            j += 1
        i += 1
    # 将  #E#开始文法也加上去求出其对应的firstvt和lastvt集。
    m = getIndex('#')
    t = 0
    while t < firstvt[0][0]:
        n = getIndex(firstvt[0][t + 1])
        Data[m][n] = '<'
        t += 1
    n = getIndex('#')
    t = 0
    while t < lastvt[0][0]:
        m = getIndex(lastvt[0][t + 1])
        Data[m][n] = '>'
        t += 1
    Data[n][n] = '='


# 移进归约操作
def deal():
    k = 1
    s[k] = '#'
    # 输入算术表达式长度
    z = len(InputStr)
    i = 0

    # 循环输入算术表达式的每个字符
    while i < z:
        # 读取对应字符
        a = InputStr[i]

        if Terminator(s[k]):
            j = k
        else:
            j = k - 1
        x = getIndex(s[j])  # 获取最接近栈顶的终极符在终极符表中位置
        if Result_Lex[0][Result_Lex[1].index(a)] == 28:
            y = getIndex('n')  # 获取第一个输入符号在终极符表中位置
        else:
            y = getIndex(a)
        # 归约
        if Data[x][y] == ">":
            out(1, k, s, 1)
            print(a, end='')
            out(i + 1, z, InputStr, 0)
            print("归约", Result)
            sign = 0
            while sign == 0:
                q = s[j]
                if Terminator(s[j - 1]):
                    j = j - 1
                else:
                    j = j - 2
                x = getIndex(s[j])
                y = getIndex(q)
                if Data[x][y] == '<':
                    sign = 1
            m = j + 1
            while m <= k:
                N = 0
                while N < len(text_2):
                    n = 1
                    while n < len(In_Str[N]):
                        if (s[m] not in Final) and (In_Str[N][n] not in Final):
                            if Terminator(s[m + 1]) and (n + 1 < len(In_Str[N])) and Terminator(In_Str[N][n + 1]) and (
                                    s[m + 1] == In_Str[N][n + 1]):
                                # print("1: ",In_Str[N][0])
                                s[j + 1] = In_Str[N][0]
                                break
                        else:
                            if Terminator(s[m]):
                                if s[m] == In_Str[N][n]:
                                    # print("2: ",In_Str[N][0])
                                    s[j + 1] = In_Str[N][0]
                                    break
                        n += 1
                    N += 1
                m += 1
            k = j + 1
            if (k == 2 and a == '#'):
                out(1, k, s, 1)
                print(a, end='')
                out(i + 1, z, InputStr, 0)
                print("结束", Result)
                print("\n该算术表达式符合文法的定义！")
                print("计算结果为：", Result[0][0])
                return 1  # 输入串符合文法的定义
        else:
            #  移进
            if (Data[x][y] == '<' or Data[x][y] == '='):
                out(1, k, s, 1)
                print(a, end='')
                out(i + 1, z, InputStr, 0)
                print("移进", Result)
                k += 1
                if Result_Lex[0][Result_Lex[1].index(a)] == 28:
                    a = 'n'
                s[k] = a
                i += 1
            else:
                print("\n该算术表达式不符合文法的定义！")
                return 0
    print("\n该算术表达式不符合文法的定义！")
    return 0


# 判断字符是否是终结字符
def Terminator(c):
    if c in Final:
        return 1
    return 0


# 字符如果是终结字符 求其在终结字符列表中的下标
def getIndex(c):
    if c in Final:
        return Final.index(c)
    return -1


# 移进和归约格式化输出
def out(j, k, arr, l):
    global Index, Result, N_Index
    tmp = []
    i = j
    n = 0
    while i <= k:
        if arr == s:
            if arr[i] == 'n':
                Result[0].append(int(Num[Index]))
                print(Num[Index], end='')
                tmp.append(Num[Index])
                Index += 1
            else:
                print(arr[i], end='')
                tmp.append(arr[i])
        else:
            if len(arr) == len(InputStr) and i == len(InputStr):
                print(" ", end='')
            else:
                print(arr[i], end='')
        n += 1
        i += 1

    # 读入算符
    if len(tmp) > 0 and tmp[-1] in ["+", "-", "*", "/", "(", ")"]:
        Result[1].append(tmp[-1])

    # 循环计算
    if l == 1 and k == N_Index - 2:
        if Result[1][-1] == '+':
            Result[0][-2] = Result[0][-2] + Result[0][-1]
            del Result[0][-1]
            del Result[1][-1]
        elif Result[1][-1] == '-':
            Result[0][-2] = Result[0][-2] - Result[0][-1]
            del Result[0][-1]
            del Result[1][-1]
        elif Result[1][-1] == '*':
            Result[0][-2] = Result[0][-2] * Result[0][-1]
            del Result[0][-1]
            del Result[1][-1]
        elif Result[1][-1] == '/':
            if Result[0][-1] != 0:
                Result[0][-2] = Result[0][-2] / Result[0][-1]
                del Result[0][-1]
                del Result[1][-1]
            else:
                print("\n该算术表达式错误，除数不能为0！")
                sys.exit()
        elif Result[1][-1] == ')':
            del Result[1][-1]
            del Result[1][-1]

    if l == 1:
        N_Index = k

    # 格式对齐
    while n < 15:
        print(" ", end='')
        n += 1


# 输出所使用文法及文法中所有非终结字符的FIRSTVT和LASTVT集合
def Prt_VT():
    print("| 使用文法为:")
    for i in text:
        print('|\t', i)
    for i in [firstvt, lastvt]:
        if i == firstvt:
            print("| 所有非终结字符的FIRSTVT集为:")
        else:
            print("| 所有非终结字符的LASTVT集为:")
        for j in range(3):
            if j == 0:
                print("|\tE: ", end='')
            elif j == 1:
                print("|\tT: ", end='')
            else:
                print("|\tF: ", end='')
            for p in i[j]:
                print(p, end=" ")
            print()


# 输出算符优先分析表
def Prt_Table():
    print("| 算符优先分析表如下:")
    print('| \t', end='')
    for i in Final:
        print('\t', end='')
        print(i, end='')
    print()
    for i in range(8):
        print('| \t', Final[i], end='\t')
        for j in range(8):
            print(Data[i][j], end='\t')
        print()


# 获取算术表达式中所有的常数值
def R_Num(arr):
    arr2 = arr
    arr3 = []
    for i in range(len(arr2[0])):
        if arr2[0][i] == 28:
            arr3.append(arr2[1][i])
    return arr3

# 判断是不是空格或者换行


def Is_blank(string):
    if string in Blank:
        return True
    else:
        return False

# 结束


def End(id):
    if id >= len(strAll):
        return True

# 判断字符数否为保留关键字


def Is_static(string):
    if string in Static_word:
        return True
    else:
        return False

# 多次重复的操作语句


def Option2(num, temp, explanation):
    Result_Lex[0].append(int(num))
    Result_Lex[1].append(temp)

# 判断字符是否为算符或者界符


def Is_marks(string):
    if string in Punctuation_marks:
        return True
    else:
        return False


# 词法分析主方法
def Analysis_Lex():
    # 索引值
    id = 0

    # 忽略代码段开头的空格或换行
    while Is_blank(strAll[id]):
        id += 1

    # 从第一个有意义的字符开始循环识别直至最后一个字符
    while id < len(strAll):
        # 保存临时结果
        temporary = ""

        # 判断是否为保留字或者标识符
        if ('a' <= strAll[id] <= 'z') or ('A' <= strAll[id] <= 'Z'):
            while ('0' <= strAll[id] <= '9') or ('a' <= strAll[id] <= 'z') or (
                    'A' <= strAll[id] <= 'Z'):
                temporary += strAll[id]
                id += 1
                if End(id):
                    break
            # 判断是否未保留字
            if Is_static(temporary):
                num = Static_word[temporary]
                Option2(num, temporary, Explanation[0])

            # 判断是否为特殊运算符odd
            elif temporary == "odd":
                num = Punctuation_marks[temporary]
                Option2(num, temporary, Explanation[num - 10])
            # 否则为非保留字标识符
            else:
                Option2("29", temporary, Explanation[-1])
        # 判断是否为常数（正数或小数）
        elif '0' <= strAll[id] <= '9':
            while ('0' <= strAll[id] <= '9') or strAll[id] == ".":
                if strAll[id] != ".":
                    temporary += strAll[id]
                    id += 1
                    if End(id):
                        break
                elif strAll[id] == "." and ('0' <= strAll[id + 1] <= '9'):
                    temporary += strAll[id]
                    id += 1
                    if End(id):
                        break
                else:
                    break
            Option2("28", temporary, Explanation[-2])
        # 判断是否为运算符或界符
        elif Is_marks(strAll[id]) or strAll[id] == ":":
            temporary += strAll[id]
            # 判断小于号三种情况：小于、小于等于、不等于
            if strAll[id] == "<":
                if strAll[id + 1] == ">" or strAll[id + 1] == "=":
                    temporary += strAll[id + 1]
                    id += 2
                    num = Punctuation_marks[temporary]
                    Option2(num, temporary, Explanation[num - 10])
                else:
                    id += 1
                    num = Punctuation_marks[temporary]
                    Option2(num, temporary, Explanation[num - 10])
            # 判断大于号两种情况：大于、大于等于
            elif strAll[id] == ">":
                if strAll[id + 1] == "=":
                    temporary += strAll[id + 1]
                    id += 2
                    num = Punctuation_marks[temporary]
                    Option2(num, temporary, Explanation[num - 10])
                else:
                    id += 1
                    num = Punctuation_marks[temporary]
                    Option2(num, temporary, Explanation[num - 10])
            # 判断赋值符号特殊情况
            elif strAll[id] == ":":
                if strAll[id + 1] == "=":
                    temporary += strAll[id + 1]
                    id += 2
                    num = Punctuation_marks[temporary]
                    Option2(num, temporary, Explanation[num - 10])
                # 单独的冒号不是运算符或界符，当非法字符处理
                else:
                    id += 1
                    Option2("30", temporary, "非法字符")
            # 其他运算法或界符
            else:
                id += 1
                num = Punctuation_marks[temporary]
                Option2(num, temporary, Explanation[num - 10])
        # 对空格、换行过滤
        elif Is_blank(strAll[id]):
            id += 1
            continue
        # 对非法字符的处理
        else:
            temporary += strAll[id]
            id += 1
            Option2("30", temporary, "非法字符")


def Scanner2(InputStr):
    for i in InputStr:
        strAll.append(i)


# 主体函数
def Cp_main():
    global Num, s, InputStr

    print("请输入待计算的算术表达式(以#结尾)：", end='')
    InputStr = input()

    # 调用实验一分析词法
    Scanner2(InputStr)
    Analysis_Lex()

    # 获取所有常数
    Num = R_Num(Result_Lex)

    # 将输入算术表达式转化为经过实验一分析的结果
    InputStr = Result_Lex[1]

    # 创建对应的模拟栈
    s = ["null" for i in range(len(InputStr) + 2)]

    # 开始分析
    deal()


if __name__ == '__main__':
    # 求文法对应的FIRSTVT和LASTVT集合
    FirstVt("E")
    LastVt("E")

    # 输出文法及对应的FIRSTVT和LASTVT集合
    Prt_VT()

    # 构建对应的算符优先关系表
    table()

    # 输出算符优先关系表
    Prt_Table()

    # 开始计算器运行
    Cp_main()
