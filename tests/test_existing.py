"""已有接口的核心、边界及错误路径。"""
import unittest,tempfile
from pathlib import Path
from lake.storage import read_source,Objects,digest

class StorageTests(unittest.TestCase):
    def test_source_and_corruption(self):
        value=read_source()
        with tempfile.TemporaryDirectory() as d:
            o=Objects(d);key=o.put(value);self.assertEqual(o.get(key),value)
            self.assertEqual(o.put(value),key)
            Path(d,key).write_bytes(b'bad')
            with self.assertRaises(ValueError):o.get(key)
    def test_bad_object_identity(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):Objects(d).get('../bad')

from lake.rows import canonical,reference
from lake.segments import write_segment,read_segment

class FeatureTests(unittest.TestCase):
    def test_all_vs_distinct(self):
        expr={'op':'except','all':True,'left':{'input':'a'},'right':{'input':'b'}}
        d={'a':[[None],[None],[1]],'b':[[None]]};self.assertEqual(sum(reference(expr,d,['int64']).values()),2)
        expr['all']=False;self.assertEqual(sum(reference(expr,d,['int64']).values()),1)
        self.assertEqual(canonical(['A'],['string'],'casefold'),canonical(['a'],['string'],'casefold'))
    def test_type_error(self):
        with self.assertRaises(ValueError):canonical([True],['int64'])
    def test_segment_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            key=write_segment(d,[(b'a',2**80)]);self.assertEqual(list(read_segment(d,key)),[(b'a',2**80)])
            Path(d,key).write_bytes(b'broken')
            with self.assertRaises(ValueError):list(read_segment(d,key))
