import os
from pathlib import Path
import subprocess
import tempfile
from soak import start,finish
import argparse
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--orb',action='store_true');args=parser.parse_args()
with tempfile.TemporaryDirectory(prefix='nexus-ui-') as d:
 proc,base,token=start(Path(d))
 try:
  env=os.environ.copy();env['NEXUS_SESSION_URL']=base+('/' if args.orb else '/dashboard')+'#token='+token
  result=subprocess.run(['node','tests/orb_ui.cjs' if args.orb else 'tests/ui_smoke.cjs'],cwd=root,env=env)
 finally:finish(proc)
raise SystemExit(result.returncode)
