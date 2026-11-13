"""小资料集合表达式的规范键与计数解释。"""
from collections import Counter
from .storage import encode

def canonical(row,schema,collation='binary'):
    if len(row)!=len(schema):raise ValueError('关系宽度不符')
    out=[]
    for value,kind in zip(row,schema):
        if kind not in ('int64','string','bool'):raise ValueError('集合类型非法')
        if value is None:out.append([kind,None]);continue
        valid=(kind=='int64' and type(value) is int and -(2**63)<=value<2**63) or (kind=='string' and type(value) is str) or (kind=='bool' and type(value) is bool)
        if not valid:raise ValueError('集合值类型不符')
        out.append([kind,value.casefold() if kind=='string' and collation=='casefold' else value])
    return encode(out)

def reference(expr,inputs,schema,collation='binary'):
    if 'input' in expr:return Counter(canonical(row,schema,collation) for row in inputs[expr['input']])
    a=reference(expr['left'],inputs,schema,collation);b=reference(expr['right'],inputs,schema,collation);out=Counter()
    for key in set(a)|set(b):
        x,y=a[key],b[key];op=expr['op']
        if expr['all']:
            n={'union':lambda:x+y,'intersect':lambda:min(x,y),'except':lambda:max(x-y,0)}[op]()
        else:n=int({'union':lambda:bool(x or y),'intersect':lambda:bool(x and y),'except':lambda:bool(x and not y)}[op]())
        if n:out[key]=n
    return out
