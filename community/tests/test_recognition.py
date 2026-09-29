import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from recognition import decide,dry_run,apply_with_adapter
class RecognitionTests(unittest.TestCase):
    def record(self):return dict(consent=True,github_proof={'verified':True,'immutable_id':7},reddit_proof={'verified':True,'immutable_id':'r7'},contributions=[{'repository':'grok-gadgets','merged':True,'author_id':7,'kind':'docs'}])
    def test_docs_and_idempotency(self):
        d=decide(self.record());self.assertEqual(d.outcome,'would_award');self.assertEqual(decide(self.record(),{d.award_key}).outcome,'already_awarded')
    def test_reject_unmerged_wrong_repo_identity_and_no_consent(self):
        for change in [dict(consent=False),dict(revoked=True),dict(github_proof={}),dict(contributions=[{'repository':'elsewhere','merged':True,'author_id':7}]),dict(contributions=[{'repository':'grok-gadgets','merged':False,'author_id':7}]),dict(contributions=[{'repository':'grok-gadgets','merged':True,'author_id':99}])]:
            with self.subTest(change=change):self.assertEqual(decide({**self.record(),**change}).outcome,'ineligible')
    def test_changed_accounts_flairs_and_override(self):
        for k in ['renamed','deleted']:self.assertEqual(decide({**self.record(),k:True}).outcome,'review')
        self.assertEqual(decide({**self.record(),'current_flair':'Maintainer'}).outcome,'preserve')
        self.assertEqual(decide({**self.record(),'manual_override':'deny'}).outcome,'ineligible')
    def test_dry_run_privacy(self):
        r=dry_run([self.record()]);self.assertNotIn('github_proof',str(r));self.assertNotIn('r7',str(r));self.assertTrue(r[0]['dry_run'])
    def test_bounded_retry_and_unknown_outcome(self):
        class Adapter:
            def award(self,key):raise TimeoutError()
            def was_awarded(self,key):return False
        d=decide(self.record());self.assertEqual(apply_with_adapter(d,Adapter())['attempts'],0);self.assertEqual(apply_with_adapter(d,Adapter(),dry_run=False)['attempts'],3)
        class Already(Adapter):
            def was_awarded(self,key):return True
        self.assertEqual(apply_with_adapter(d,Already(),dry_run=False)['attempts'],1)
    def test_revoked_adapter(self):
        class Adapter:
            def award(self,key):raise PermissionError()
        self.assertEqual(apply_with_adapter(decide(self.record()),Adapter(),dry_run=False)['outcome'],'authorization_revoked')
if __name__=='__main__':unittest.main()
