import json
import unittest
from pathlib import Path
from product.app import Application


class BusinessBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.app=Application()
        self.app.replay(json.loads((Path(__file__).parent.parent/'data'/'demo.json').read_text()))

    def tearDown(self):
        self.app.store.close()
    def test_transfer_and_pause_boundaries(self):
        self.assertFalse(self.app.execute('memberships.status',dict(id='m1',at='2026-11-10'))['active'])
        self.assertEqual(self.app.execute('memberships.status',dict(id='m1',at='2026-12-10')),
            dict(active=True,venue='south',household='f1'))

    def test_finished_contact_retries_are_stable(self):
        before=self.app.store.get('care_plan','c1')
        self.app.execute('care.finish',dict(id='c1',membership='m1',outcome='failed'))
        self.assertEqual(self.app.store.get('care_plan','c1'),before)
