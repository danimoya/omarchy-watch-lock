"""Load the full service on Wayland with fake compositor/stranded-lock commands."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PROJECT=Path(__file__).resolve().parents[1]
SHELL=Path(os.environ.get('OMARCHY_PATH','/usr/share/omarchy'))/'shell'


@unittest.skipUnless(shutil.which('quickshell') and SHELL.is_dir() and os.environ.get('WATCH_LOCK_NATIVE_CHECK') == '1',
                     'Set WATCH_LOCK_NATIVE_CHECK=1 on Wayland; the service has a native PanelWindow')
class NativeLoadTests(unittest.TestCase):
    def test_full_service_loads_without_locking_or_authenticating(self):
        with tempfile.TemporaryDirectory(prefix='watch-lock-load-') as folder:
            root=Path(folder)
            for child in SHELL.iterdir():
                if child.is_dir(): (root/child.name).symlink_to(child,target_is_directory=True)
            (root/'Plugin').symlink_to(PROJECT,target_is_directory=True)
            (root/'bin').mkdir()
            for name,body in {
                'hyprctl':'''#!/usr/bin/python3
import json,sys
print(json.dumps([{"id":0,"width":1600,"height":900,"activeWorkspace":{"id":1},"specialWorkspace":{"id":0}}] if sys.argv[-1]=="monitors" else []))
''',
                'omarchy-hw-laptop-closed':'#!/bin/sh\nexit 1\n',
                'omarchy-hyprland-session-lock-stranded':'#!/bin/sh\nexit 1\n',
                'fprintd-list':'#!/bin/sh\necho no\n',
            }.items():
                path=root/'bin'/name;path.write_text(body);path.chmod(0o755)
            (root/'shell.qml').write_text('''import QtQuick
import Quickshell
import "Plugin" as Watch
ShellRoot {
  Watch.Service { id: service }
  Timer { interval: 1000; running: true; onTriggered: {
    if (service.lockRequested || service.authenticating || !service.stateKnown) {
      console.error("SERVICE_LOAD_FAILED"); Qt.exit(1); return
    }
    console.log("SERVICE_LOAD_PASSED"); Qt.quit()
  } }
}
''')
            env={**os.environ,'PATH':str(root/'bin')+':'+os.environ['PATH'],'QT_QPA_PLATFORM':'wayland'}
            result=subprocess.run(['quickshell','-p',str(root/'shell.qml'),'--no-color'],env=env,capture_output=True,text=True,timeout=10)
            log=result.stdout+result.stderr
            self.assertEqual(result.returncode,0,log)
            self.assertIn('SERVICE_LOAD_PASSED',log)
            self.assertNotIn('TypeError',log)
            self.assertNotIn('ReferenceError',log)
