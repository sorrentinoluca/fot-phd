"""Only rerun X06/X07 after fixing the reviewer subprocess cwd, not candidate code."""
import extended_probes as m
import json, unittest
m.E=m.E/'concurrency_rerun';m.E.mkdir(exist_ok=False)
names=['test_X06_real_concurrent_base_reservation_12_writers','test_X07_outcome_transaction_excludes_writer_while_closing']
with (m.E/'concurrency.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.TestSuite(m.Extended(n) for n in names))
(m.E/'concurrency.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[{'id':t.id(),'traceback':s} for t,s in r.failures],errors=[{'id':t.id(),'traceback':s} for t,s in r.errors],observations=m.OBS),indent=2)+'\n')
print(r.testsRun,len(r.failures),len(r.errors))
