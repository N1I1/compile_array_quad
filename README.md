# 编译原理课设

## 题目

题目：将包含数组引用的赋值语句转换成四元式的程序实现设计内容及要求：设计一个语法制导翻译器，将包含数组引用的赋值语句 翻译成四元式。要求：先确定一个定义包含数组引用的赋值语句的文法，为其设计一个语法分析程序，为每条产生式配备一个语义子程序，按照一遍扫描的语法 制导翻译方法，实现翻译程序。对用户输入的任意一个正确的包含数组引用的赋值语句，程序将其转换成四元式输出(可按一定格式输出到指定文件中)。

## 翻译模式

```paintext
S -> A { S.code = A.code }

A -> LHS '=' E ';'
{
    A.code = LHS.code || E.code || gen("=", LHS.addr, E.addr)
}

LHS -> id '[' E_list ']' 
{
    LHS.addr = newtemp(); 
    LHS.code = E_list.code || gen("[]", id, E_list.addr, LHS.addr)
}
    | id 
{
    LHS.addr = id; 
    LHS.code = ""
}

E_list -> E ',' E_list_tail 
{
    E_list.addr = newtemp(); 
    E_list.code = E.code || E_list_tail.code || gen("idx", E.addr, E_list_tail.addr, E_list.addr)
}
    | E 
{
    E_list.addr = E.addr; 
    E_list.code = E.code
}

E -> E1 '+' T 
{
    E.addr = newtemp(); 
    E.code = E1.code || T.code || gen("+", E1.addr, T.addr, E.addr)
}
   | E1 '-' T 
{
    E.addr = newtemp(); 
    E.code = E1.code || T.code || gen("-", E1.addr, T.addr, E.addr)
}
   | T 
{
    E.addr = T.addr; 
    E.code = T.code
}

T -> T1 '*' F 
{
    T.addr = newtemp(); 
    T.code = T1.code || F.code || gen("*", T1.addr, F.addr, T.addr)
}
   | T1 '/' F 
{
    T.addr = newtemp(); 
    T.code = T1.code || F.code || gen("/", T1.addr, F.addr, T.addr)
}
   | F 
{
    T.addr = F.addr; 
    T.code = F.code
}

F -> '(' E ')' 
{
    F.addr = E.addr; 
    F.code = E.code
}
   | id '[' E_list ']' 
{
    F.addr = newtemp(); 
    F.code = E_list.code || gen("[]", id, E_list.addr, F.addr)
}
   | id 
{
    F.addr = id; 
    F.code = ""
}
   | num 
{
    F.addr = num; 
    F.code = ""
}

```
---


```rust
S -> A { S.code = A.code }

A -> LHS '=' E ';'
{
    A.code = LHS.code || E.code || gen("=", LHS.addr, E.addr)
}

LHS -> id '[' E_list ']' 
{
    LHS.addr = newtemp();
    LHS.ndim = E_list.ndim + 1;  // 记录维度数
    LHS.offset = newtemp();      // 记录偏移量计算的临时变量
    LHS.code = E_list.code || 
               gen("*", E_list.addr, width(LHS.ndim), LHS.offset) ||  // 计算偏移量
               gen("+", id, LHS.offset, LHS.addr);  // 计算最终地址
}
    | id 
{
    LHS.addr = id; 
    LHS.ndim = 0;  // 标量的维度数为0
    LHS.code = ""
}

E_list -> E ',' E_list_tail 
{
    E_list.addr = newtemp(); 
    E_list.ndim = E_list_tail.ndim + 1;  // 计算维度数
    E_list.code = E.code || E_list_tail.code ||
                  gen("+", gen("*", E_list_tail.addr, width(E_list.ndim - 1)), E.addr, E_list.addr);  // 计算多维数组的索引地址
}
    | E 
{
    E_list.addr = E.addr; 
    E_list.ndim = 1;  // 单个表达式的维度数为1
    E_list.code = E.code
}

E -> E1 '+' T 
{
    E.addr = newtemp(); 
    E.code = E1.code || T.code || gen("+", E1.addr, T.addr, E.addr)
}
   | E1 '-' T 
{
    E.addr = newtemp(); 
    E.code = E1.code || T.code || gen("-", E1.addr, T.addr, E.addr)
}
   | T 
{
    E.addr = T.addr; 
    E.code = T.code
}

T -> T1 '*' F 
{
    T.addr = newtemp(); 
    T.code = T1.code || F.code || gen("*", T1.addr, F.addr, T.addr)
}
   | T1 '/' F 
{
    T.addr = newtemp(); 
    T.code = T1.code || F.code || gen("/", T1.addr, F.addr, T.addr)
}
   | F 
{
    T.addr = F.addr; 
    T.code = F.code
}

F -> '(' E ')' 
{
    F.addr = E.addr; 
    F.code = E.code
}
   | id '[' E_list ']' 
{
    F.addr = newtemp(); 
    F.code = E_list.code || gen("[]", id, E_list.addr, F.addr)
}
   | id 
{
    F.addr = id; 
    F.code = ""
}
   | num 
{
    F.addr = num; 
    F.code = ""
}
```

## TODO

- [ ] 左递归消除
- [ ] E -> (E) | E + E | E - E
- [ ] T -> (T) | T + T| T - T 
后两个似乎不需要？？？
E -> (E)
E -> T -> F -> (E)
好像是的
