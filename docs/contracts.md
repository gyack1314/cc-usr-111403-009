# 资料语义与接口边界

AST节点为input、union/intersect/except，各运算含all布尔；union all计数a+b，intersect all=min(a,b)，except all=max(a-b,0)；distinct模式分别为存在并/存在交/仅左存在，结果计数至多1。无隐式交换或结合except，intersect/except输入计数按子表达式结果。schema按位置对齐，列名来自左侧，类型为int64/string/bool及nullable，同位置不同基本类型先拒绝。null在集合等价中相等，string按binary或casefold比较，输出代表值由规范编码定义而非到达顺序：casefold输出折叠字符串。rows.py提供规范有类型行键与小规模Counter解释器，segments.py提供带摘要的有序计数段读写，不提供外存计划。输入只能消费一次；哈希碰撞需比较完整键，计数使用任意精度非负整数；大重数可用(row,count)块返回但展开接口仍保留准确袋。

rows.py仅是内存Counter参考解释器；segments.py提供有序计数段格式，尚无受预算约束的一次性流执行器。

正文摘要绑定完整值，样例数据不限定输入规模；错误不等同空结果，接口使用中文错误说明。
