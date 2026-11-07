"""Exercise the real CLI with synthetic IPC; no desktop is locked."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1]/'scripts/omarchy-watch-lock'
MOCK = '''#!/usr/bin/python3
import os,pathlib,sys
name=pathlib.Path(sys.argv[0]).name
with open(os.environ["CALL_LOG"],"a") as log: log.write(name+" "+" ".join(sys.argv[1:])+"\\n")
if name=="omarchy" and sys.argv[1:]==["toggle","idle","status"]: print(os.environ.get("AWAKE",'{"enabled":true}'))
elif name=="hyprctl" and "getoption" in sys.argv: print(os.environ.get("XRAY",'{"bool":true}'))
elif name=="omarchy-shell":
    if sys.argv[1:]==["lock","watch"]: print(os.environ.get("WATCH","ok"))
    elif sys.argv[1:]==["lock","status"]: print(os.environ.get("STATUS",'{"secure":true,"sessionLocked":true}'))
    else: print("ok")
elif name=="pgrep": sys.exit(1)
'''


class CliTests(unittest.TestCase):
    def run_cli(self,*args,**settings):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name in ('omarchy','omarchy-shell','hyprctl','pgrep','sleep'):
                path=root/name;path.write_text(MOCK);path.chmod(0o755)
            log=root/'calls'
            result=subprocess.run(['bash',str(SCRIPT),*args],env={**os.environ,'PATH':f'{root}:/usr/bin','CALL_LOG':str(log),**settings},capture_output=True,text=True,timeout=15)
            return result,log.read_text() if log.exists() else ''

    def test_secure_acknowledgement(self):
        result,calls=self.run_cli()
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('Session lock confirmed',result.stdout)
        self.assertIn('omarchy-shell lock watch',calls)
        self.assertNotIn('omarchy system lock',calls)

    def test_unknown_or_disabled_state_falls_back(self):
        for settings in ({'AWAKE':'{"enabled":false}'},{'AWAKE':'invalid'},{'XRAY':'{"bool":false}'},{'WATCH':'already-locked'},{'WATCH':'Function not found.'}):
            with self.subTest(settings=settings):
                result,calls=self.run_cli(**settings)
                self.assertIn('omarchy system lock',calls)
                self.assertNotIn('Session lock confirmed',result.stdout)

    def test_unacknowledged_lock_is_never_reported_confirmed(self):
        result,calls=self.run_cli(STATUS='{"secure":false,"sessionLocked":true}')
        self.assertEqual(result.returncode,1)
        self.assertNotIn('Session lock confirmed',result.stdout)
        self.assertIn('omarchy system lock',calls)

    def test_preview_and_help_do_not_authenticate(self):
        result,calls=self.run_cli('--preview')
        self.assertEqual(result.returncode,0)
        self.assertEqual(calls.strip(),'omarchy-shell lock previewWatch')
        result,calls=self.run_cli('--help')
        self.assertEqual(result.returncode,0)
        self.assertEqual(calls,'')
