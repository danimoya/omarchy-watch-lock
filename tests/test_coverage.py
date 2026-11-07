import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('runtime', Path(__file__).resolve().parents[1]/'scripts/runtime_state.py')
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.monitors = [{'id':0,'width':1920,'height':1080,'activeWorkspace':{'id':2},'specialWorkspace':{'id':-99}}]
        self.client = {'class':runtime.CLASS,'mapped':True,'hidden':False,'monitor':0,'workspace':{'id':-99},'fullscreen':2}

    def test_visible_fullscreen_saver_covers_output(self):
        self.assertTrue(runtime.covers_outputs(self.monitors,[self.client]))

    def test_each_active_output_requires_coverage(self):
        self.monitors.append({'id':1,'width':1920,'height':1080,'activeWorkspace':{'id':3},'specialWorkspace':{'id':0}})
        self.assertFalse(runtime.covers_outputs(self.monitors,[self.client]))
        other = {**self.client,'monitor':1,'workspace':{'id':3}}
        self.assertTrue(runtime.covers_outputs(self.monitors,[self.client,other]))

    def test_hidden_unmapped_wrong_workspace_and_nonfullscreen_refused(self):
        for changes in ({'mapped':False},{'hidden':True},{'class':'ordinary-app'},{'monitor':3},{'workspace':{'id':2}},{'fullscreen':0}):
            with self.subTest(changes=changes):
                self.assertFalse(runtime.covers_outputs(self.monitors,[{**self.client,**changes}]))

    def test_missing_outputs_and_hotplug_fail_closed(self):
        self.assertFalse(runtime.covers_outputs([],[]))
        self.assertFalse(runtime.covers_outputs(self.monitors,[]))


if __name__ == '__main__':
    unittest.main()
