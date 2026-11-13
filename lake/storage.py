"""不可变正文及带摘要的资料读取。"""
from pathlib import Path
import hashlib,json,os,tempfile

def encode(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')

def digest(value):return hashlib.sha256(encode(value)).hexdigest()

def read_source(path='data/source.json'):
    return json.loads(Path(path).read_text(encoding='utf-8'))

class Objects:
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
    def put(self,value):
        raw=encode(value);key=hashlib.sha256(raw).hexdigest();path=self.root/key
        if path.exists():
            self.get(key);return key
        fd,tmp=tempfile.mkstemp(dir=self.root,prefix='.writing-')
        try:
            with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
        return key
    def get(self,key):
        if len(key)!=64 or any(c not in '0123456789abcdef' for c in key):raise ValueError('非法正文身份')
        raw=(self.root/key).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=key:raise ValueError('正文摘要不符')
        return json.loads(raw)
