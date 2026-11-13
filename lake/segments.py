"""带摘要的有序计数段持久格式。"""
from .storage import Objects

def write_segment(root,items):
    rows=[];last=None
    for key,count in items:
        if type(count) is not int or count<=0 or not isinstance(key,bytes):raise ValueError('计数段条目非法')
        if last is not None and key<=last:raise ValueError('计数键非严格递增')
        rows.append([key.hex(),str(count)]);last=key
    return Objects(root).put(rows)

def read_segment(root,key):
    for k,n in Objects(root).get(key):yield bytes.fromhex(k),int(n)
