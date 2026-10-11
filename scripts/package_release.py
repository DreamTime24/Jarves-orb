"""Package distributable source/runtime with SHA256 inventory; exclude user data."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
EXCLUDED={'__pycache__','.git','.venv','.runtime'}
LEGACY={'NEXUS-Start.dll','NEXUS-Start.runtimeconfig.json','NEXUS.pdb','launcher/Program.cs','launcher/NexusLauncher.csproj'}

def files():
    for path in sorted(ROOT.rglob('*')):
        relative=path.relative_to(ROOT)
        if relative.as_posix() in LEGACY:continue
        if relative.parts[0] in {'build','data','logs','bootstrap-runtime'}:continue
        if any(part in EXCLUDED or part.endswith('.egg-info') for part in relative.parts):continue
        if relative.parts[0]=='docs' and path.suffix.lower() in {'.jpg','.png'}:continue
        if path.is_symlink():raise ValueError('Release file must not be a symbolic link: '+str(relative))
        if not path.is_file() or path.suffix in {'.pyc','.sqlite','.log'} or path.name=='.env':continue
        if relative.parts[0]=='workspace' and relative.as_posix()!='workspace/README.md':continue
        yield path

def digest(path):
    value=hashlib.sha256()
    with path.open('rb') as stream:
        while chunk:=stream.read(1024*1024):value.update(chunk)
    return value.hexdigest()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT.parent/'NEXUS-v0.5.zip'));args=parser.parse_args()
    output=Path(args.output).resolve()
    if output.is_relative_to(ROOT):raise ValueError('Write the archive outside its source directory')
    manifest=ROOT/'docs'/'FILE-MANIFEST.json'
    inventory=[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files() if p!=manifest]
    manifest.write_text(json.dumps({'version':'0.5.0','scope':'Release files; this manifest excludes its own bytes','files':inventory},indent=2)+'\n')
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for path in files():archive.write(path,'NEXUS/'+path.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as archive:
        failure=archive.testzip()
        if failure:raise ValueError('ZIP CRC failed: '+failure)
    print(json.dumps({'archive':str(output),'bytes':output.stat().st_size,'sha256':digest(output),'files':len(inventory)+1,'zip_integrity':True}))

if __name__=='__main__':main()
