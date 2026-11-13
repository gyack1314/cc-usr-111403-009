"""读取现有资料摘要，不执行新的仓查询。"""
import json
from .storage import read_source,digest
if __name__=='__main__':
    value=read_source()
    print(json.dumps({'sections':list(value),'digest':digest(value)},ensure_ascii=False))
