#!/usr/bin/env python3
"""Read public compositor state; never read credentials or print window titles."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys


CLASS = 'org.omarchy.screensaver'


def query(what):
    result = subprocess.run(['hyprctl', '-j', what], capture_output=True, text=True,
                            check=True, timeout=2)
    data = json.loads(result.stdout)
    if not isinstance(data, list) or len(data) > 2000:
        raise ValueError('Invalid compositor response')
    return data


def covers_outputs(monitors, clients):
    outputs = [m for m in monitors if not m.get('disabled') and m.get('width', 0) > 0 and m.get('height', 0) > 0]
    if not outputs:
        return False
    for output in outputs:
        special = output.get('specialWorkspace', {}).get('id', 0)
        workspace = special or output.get('activeWorkspace', {}).get('id')
        if workspace is None:
            return False
        matching = [w for w in clients if w.get('class') == CLASS and w.get('mapped') is True
                    and not w.get('hidden') and w.get('monitor') == output.get('id')
                    and w.get('workspace', {}).get('id') == workspace
                    and w.get('fullscreen') == 2]
        if not matching:
            return False
    return True


def snapshot():
    empty = dict(stateKnown=False, stayAwake=False, lidClosed=True,
                 screensaverRunning=False, screensaverCovered=False)
    try:
        clients, monitors = query('clients'), query('monitors')
        lid = subprocess.run(['omarchy-hw-laptop-closed'], capture_output=True, timeout=2)
        if lid.returncode not in (0, 1):
            return empty
        return dict(stateKnown=True,
                    stayAwake=(Path.home()/'.local/state/omarchy/indicators/stay-awake').is_file(),
                    lidClosed=lid.returncode == 0,
                    screensaverRunning=any(w.get('class') == CLASS and w.get('mapped') for w in clients),
                    screensaverCovered=covers_outputs(monitors, clients))
    except (OSError, ValueError, subprocess.SubprocessError):
        return empty


def stop_owned_screensavers():
    try:
        clients = query('clients')
    except (OSError, ValueError, subprocess.SubprocessError):
        return 1
    for window in clients:
        if window.get('class') != CLASS:
            continue
        pid = window.get('pid')
        if not isinstance(pid, int) or pid < 2:
            continue
        process = Path('/proc')/str(pid)
        try:
            if process.stat().st_uid == os.getuid() and CLASS.encode() in (process/'cmdline').read_bytes():
                os.kill(pid, signal.SIGTERM)
        except (OSError, ProcessLookupError):
            pass
    return 0


if __name__ == '__main__':
    action = sys.argv[1] if len(sys.argv) == 2 else 'state'
    if action == 'state':
        print(json.dumps(snapshot()))
    elif action == 'stop':
        raise SystemExit(stop_owned_screensavers())
    else:
        raise SystemExit('Usage: runtime_state.py [state|stop]')
