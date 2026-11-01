import unittest
import copy
import struct
import xml.etree.ElementTree as ET
from .app import State, svg
from fastapi.testclient import TestClient
from .app import app, CATALOG

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.c=TestClient(app); cls.state=CATALOG['default_state']
    def test_catalog_counts(self):
        x=self.c.get('/api/catalog').json(); self.assertEqual((len(x['expressions']),len(x['decorations']),len(x['palettes'])),(21,17,8))
    def test_compose_xml(self):
        r=self.c.post('/api/compose',json=self.state); self.assertEqual(r.status_code,200); self.assertIn('xmlns="http://www.w3.org/2000/svg"',r.text)
    def test_all_assets(self):
        for e in CATALOG['expressions']:
            for p in CATALOG['palettes']:
                for d in [None]+CATALOG['decorations']:
                    output=svg(State(expression=e['id'],palette=p,decorations=[] if d is None else [d['id']]))
                    self.assertNotIn('{{',output)
                    self.assertTrue(all(n.tag.startswith('{http://www.w3.org/2000/svg}') for n in ET.fromstring(output).iter()))
    def test_geometry(self):
        root=ET.fromstring(svg(State(**self.state)))
        ns={'s':'http://www.w3.org/2000/svg'}
        group=root.find('s:g',ns)
        self.assertEqual(group.attrib['transform'],'translate(90 90)')
        eyes=[n for n in group.findall('s:rect',ns) if n.get('height')=='130']
        self.assertEqual(len(eyes),2)
        self.assertEqual(len(root.findall('s:defs/s:filter',ns)),2)
    def test_png_sizes(self):
        for n in (240,512,1024):
            r=self.c.post(f'/api/export?format=png&size={n}',json=self.state); self.assertEqual(r.status_code,200); self.assertEqual(r.content[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II',r.content[16:24]),(n,round(n*560/780)))
    def test_invalid(self):
        x=dict(self.state); x['expression']='bad'; self.assertEqual(self.c.post('/api/compose',json=x).status_code,422)
        x=dict(self.state); x['palette']=dict(x['palette']); x['palette']['body']='red'; self.assertEqual(self.c.post('/api/compose',json=x).status_code,422)
    def test_random(self):
        for _ in range(100):
            r=self.c.post('/api/random'); self.assertEqual(r.status_code,200); self.assertEqual(self.c.post('/api/validate',json=r.json()).json()['warnings'],[])
    def test_attachment_conflict(self):
        state=copy.deepcopy(self.state);state['decorations']=['deco-hat-beanie','deco-hat-cap']
        self.assertEqual(self.c.post('/api/compose',json=state).status_code,422)

if __name__=='__main__': unittest.main()
