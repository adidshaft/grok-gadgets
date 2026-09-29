"""Run local component checks, preserving output and exact source commits."""
from pathlib import Path
import subprocess,json,time,sys
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/verification';out.mkdir(parents=True,exist_ok=True)
jobs=[('hub',root,['python3','scripts/check.py']),('website',root,['python3','website/build.py']),('activity',root,['python3','-m','unittest','discover','-s','website','-p','test_*.py']),('community',root,['python3','-m','unittest','discover','-s','community/tests']),('gateway',root.parent/'grok-gadgets-gateway',['uv','run','pytest']),('mcp-demo',root.parent/'grok-gadgets-gateway',['uv','run','python','-m','grok_gadgets_gateway.demo']),('linux',root.parent/'grok-gadgets-linux-sdk',['uv','run','python','-m','unittest','discover','-s','tests','-v']),('home-assistant',root.parent/'grok-gadgets-home-assistant',['uv','run','python','-m','unittest','discover','-s','tests','-v']),('esp32-host',root.parent/'grok-gadgets-esp32-sdk',['sh','tools/check.sh']),('esp32-contract',root.parent/'grok-gadgets-esp32-sdk',['.venv/bin/python','tools/check_contract.py']),('esp32-usb-integration',root.parent/'grok-gadgets-esp32-sdk',['../grok-gadgets-gateway/.venv/bin/python','tools/check_gateway.py'])]
import os
results=[]
for name,cwd,command in jobs:
    env=os.environ.copy();env['GROK_GATEWAY_SOURCE']=str(root.parent/'grok-gadgets-gateway/src')
    start=time.monotonic();r=subprocess.run(command,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    (out/(name+'.log')).write_text(r.stdout)
    commit=subprocess.check_output(['git','-C',str(cwd),'rev-parse','HEAD'],text=True).strip()
    results.append(dict(check=name,repository=cwd.name,commit=commit,command=command,exit_code=r.returncode,seconds=round(time.monotonic()-start,2),log=str((out/(name+'.log')).relative_to(root))))
    print(f'{name}: '+('PASS' if r.returncode==0 else 'FAIL'),flush=True)
    if r.returncode:print(r.stdout)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
sys.exit(any(x['exit_code'] for x in results))
