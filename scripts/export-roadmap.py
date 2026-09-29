from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
issues=json.loads((R/'planning/issues.json').read_text())
for i in issues:
    text='# '+i['id']+' — '+i['problem']+'\n\nOwner: '+i['repository']+'\n\nStage: '+i['stage']+' · '+i['milestone']+'\n\nLabels: '+', '.join(i['labels'])+'\n\nIntended behaviour: '+i['intended_behaviour']+'\n\nAcceptance:\n\n'+''.join('- '+x+'\n' for x in i['acceptance'])+'\nDependencies: '+(', '.join(i['dependencies']) or 'None')+'\n\nCommits: '+(', '.join(i['commits']) or 'Pending')+'\n\nEvidence:\n\n'+''.join('- '+x+'\n' for x in i['evidence'])+'\nBlocker: '+(i.get('blocker') or 'None')+'\n'
    (R/'planning/issues'/f"{i['id']}.md").write_text(text)
print('Exported canonical coordination issue files')
