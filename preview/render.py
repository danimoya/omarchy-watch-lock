#!/usr/bin/env python3
"""Render real plugin QML over invented data; never capture the user's desktop."""
import os
from pathlib import Path
import subprocess
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
SHELL = Path(os.environ.get('OMARCHY_PATH', '/usr/share/omarchy'))/'shell'


def render():
    output = PROJECT/'screenshots'
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='watch-lock-preview-') as folder:
        root = Path(folder)
        for child in SHELL.iterdir():
            if child.is_dir():
                (root/child.name).symlink_to(child, target_is_directory=True)
        (root/'Plugin').symlink_to(PROJECT, target_is_directory=True)
        (root/'shell.qml').write_text('''import QtQuick
import Quickshell
ShellRoot {
  FloatingWindow {
    implicitWidth: 1600; implicitHeight: 900; visible: true
    Loader { id: scene; anchors.fill: parent; source: "Plugin/preview/Capture.qml"; onLoaded: start.start() }
  }
  Timer { id: start; interval: 250; onTriggered: scene.item.when = true }
}
''')
        env = {**os.environ, 'QT_QPA_PLATFORM': 'offscreen', 'QT_QUICK_BACKEND': 'software', 'WATCH_LOCK_OUTPUT': str(output)}
        try:
            result = subprocess.run(['quickshell','-p',str(root/'shell.qml'),'--no-color'],
                                    env=env, capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired as error:
            raise RuntimeError(str(error.stdout) + str(error.stderr)) from error
        log = result.stdout + result.stderr
        if result.returncode or 'SAFE_PREVIEW_CAPTURED' not in log or 'TypeError' in log or 'ReferenceError' in log:
            raise RuntimeError(log)
        for name in ('watch-lock.png','watch-lock-faded.png'):
            file = output/name
            if not file.exists() or file.stat().st_size < 10000:
                raise RuntimeError('Preview image missing: '+name)
            print(file)


if __name__ == '__main__':
    render()
