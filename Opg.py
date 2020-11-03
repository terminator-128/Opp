# Operator-Precedence Parser

# 语法G定义规则集合
# E -> E'+'T | T
# E -> T'*'F | F
# F -> '('E')' | i

# 终结符符号集
Vt = ('+','*','(',')','i',' ')

# 定义符号的位置整数
Opt = {
    '+':0,
    '*':1,
    '(':2,
    ')':3,
    'i':4,
    ' ':5
}

#  出错 小于 等于 大于 分别用 0, 1，2，3 表示
Cmp = {
    0: 'error',
    1: '<',
    2: '=',
    3: '>',
}

# 根据给定文法由算法写出优先级矩阵
# 分析各非终结符的FIRSTVT集和LASTVT集
#
#     FIRSTVT   LASTVT
#  E {+,*,(,i} {+,*,),i}
#  T {*,(,i}   {*,),i}
#  F {(,i}     {),i}

# 符合文法规则 W->...aU...
# +T => + < FIRSTVT(T)
# *F => * < FIRSTVT(F)
# (E => ( < FIRSTVT(E)
# #E => # < FIRSTVT(E)

# 符合文法规则 W-> ...Ub...
# E+ => LASTVT(E) > +
# T* => LASTVT(T) > *
# E) => LASTVT(E) > )
# E# => LASTVT(E) > #

#  优先级矩阵（竖排为栈顶字符(左,先)，横排为输入字符(右,后)）
#      +  *  (  )  i  #
#   +  >  <  <  >  <  >
#   *  >  >  <  >  <  >
#   (  <  <  <  =  <  0
#   )  >  >  0  >  0  >
#   i  >  >  0  >  0  >
#   #  <  <  <  0  <  =

PM = [
    [ 3, 1, 1, 3, 1, 3],
    [ 3, 3, 1, 3, 1, 3],
    [ 1, 1, 1, 2, 1, 0],
    [ 3, 3, 0, 3, 0, 3],
    [ 3, 3, 0, 3, 0, 3],
    [ 1, 1, 1, 0, 1, 2],
]

# 输入参数为文件名
# 显示输入文件中的字节流
# 输入不超过 1000字节，且只含非空白 ASCII 字符，以\r\n结束
# 从参数文件名中获取输入字符串
import sys
try:
    f = open(sys.argv[1])
    sentence = f.read()
    f.close()
except:
    exit(-1)

# 初始化算法准备函数

# 操作符栈 O
O = [' ']

# 符号栈S
S = [' '] # 初始栈内含有 '#'

# 输入字符串T
T = list(sentence[:-2]+' #') # 输入字符末尾删'\r\n'添'#'

# 栈顶字符 tp
tp = O[-1]

# 读入符号的读头 tk
tk = T[0]

# 根据算符优先算法进行分析
# 算符优先算法不区分非终结符，所有非终结符统一视作N
# 即 N -> N+N | N*N | (N) |i

# 成功示例：输入串T：i*(i+i)
# 步骤 符号栈S  栈顶符号  优先关系  读入符号   输入符号串T 动作
#  0   #           #         <         i       i*(i+i)#    初始化 
#  1   #i          i         >         *       *(i+i)#     向前移位
#  2   #N          #         <         *       *(i+i)#     归约
#  3   #N*         *         <         (       i+i)#       向前移位
#  4   #N*(        (         <         i       +i)#        向前移位
#  5   #N*(i       i         >         +       i)#         向前移位
#  6   #N*(N       (         <         +       i)#         归约
#  7   #N*(N+      +         <         i       )#          向前移位
#  8   #N*(N+i     i         >         )       #           向前移位       
#  9   #N*(N+N     +         >         )       #           归约
# 10   #N*(N       (         =         )       #           归约
# 11   #N*(N)      )         >         #                   归约
# 12   #N*N        *         >         #                   归约
# 13   #N          #         =         #                   归约
# 14   #N#                                                 向前移位
# 15   我是开始字符 yep！

while tk!='#':
    # 新的栈顶操作符
    tp = O[-1]
    # 进行新的优先级判断
    pk = Cmp[PM[Opt[tp]][Opt[tk]]]
    if pk=='>':
        if tp=='+' or tp=='*':
            if S[-3:]==['N',tp,'N']:
                print('R')
                S = S[:-3]
                S.append('N')
                O.pop()
            else:
                print('RE')
                break
        elif tp==')':
            if S[-3:]==['(','N',')']:
                print('R')
                S = S[:-3]
                S.append('N')
                O = O[:-2]
            else:
                print('RE')
                break
        elif tp=='i':
            print('R')
            S.pop()
            S.append('N')
            O.pop()
            
    elif pk=='<' or pk=='=':
        # 读入符号入栈
        S.append(tk)
        O.append(tk)
        T.pop(0)
        # 判断读入字符是否为结尾符
        if tk!= ' ':
            print('I'+tk)
        
        # 新的读入字符
        tk = T[0]
        # 输入字符是否为识别符号
        if tk not in Vt:
            break
    elif pk=='error':
        print('E')
        break