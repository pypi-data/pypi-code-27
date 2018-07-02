#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import shutil
import subprocess
import sys
import unittest

from sos.hosts import Host
from sos.parser import SoS_Script
from sos.targets import file_target, sos_targets
from sos.utils import env
# if the test is imported under sos/test, test interacive executor
if 'sos-notebook' in os.path.abspath(__file__).split(os.sep):
    from sos_notebook.workflow_executor import Interactive_Executor as Base_Executor
    test_interactive = True
else:
    from sos.workflow_executor import Base_Executor
    test_interactive = False


class TestSignature(unittest.TestCase):
    def setUp(self):
        env.reset()
        subprocess.call('sos remove -s', shell=True)
        # self.resetDir('~/.sos')
        self.temp_files = []
        self.resetDir('temp')
        Host.reset()

    def tearDown(self):
        for f in self.temp_files:
            file_target(f).remove('both')

    def touch(self, files):
        '''create temporary files'''
        if isinstance(files, str):
            files = [files]
        #
        for f in files:
            with open(f, 'w') as tmp:
                tmp.write('test')
        #
        self.temp_files.extend(files)

    def resetDir(self, dirname):
        if os.path.isdir(os.path.expanduser(dirname)):
            shutil.rmtree(os.path.expanduser(dirname))
        os.mkdir(os.path.expanduser(dirname))

    def testSignature(self):
        self._testSignature(r"""
[*_0]
output: 'temp/a.txt', 'temp/b.txt'
task:
run('''echo "a.txt" > temp/a.txt ''')
run('''echo "b.txt" > temp/b.txt ''')

[1: shared={'oa':'step_output'}]
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

run(f" cp {_input} {_dest[0]} ")
""", 2)

    def testSignature1(self):
        self._testSignature(r"""
[*_0]
output: 'temp/a.txt', 'temp/b.txt'

task:
run('''echo "a.txt" > temp/a.txt ''')
run('''echo "b.txt" > temp/b.txt ''')

[1: shared={'oa':'step_output'}]
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

run(f" cp {_input} {_dest[0]} ")
""", 2)
        # script format

    def testSignature2(self):
        self._testSignature(r"""
[*_0]
output: 'temp/a.txt', 'temp/b.txt'

run:
echo "a.txt" > temp/a.txt

run:

echo "b.txt" > temp/b.txt

[1: shared={'oa':'step_output'}]
dest = ['temp/c.txt', 'temp/d.txt']
input: group_by='single', paired_with='dest'
output: _dest

task:
run: expand=True
echo cp {_input} {_dest[0]}
cp {_input} {_dest[0]}
""", 2)

    @unittest.skipIf('TRAVIS' in os.environ and test_interactive, 'This test fails for unknown reason under travis and interactive mode')
    def testSignatureWithSharedVariable(self):
        '''Test restoration of signature from variables.'''
        file_target('a.txt').remove('both')
        # shared
        script = SoS_Script(r"""
[0: shared='a']
output: 'a.txt'
run:
   touch a.txt

a= 5

[1]
print(a)

""")
        # alias should also be recovered.
        wf = script.workflow('default')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 2)
        # rerun
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        file_target('a.txt').remove('both')

    def testSignatureWithoutOutput(self):
        # signature without output file
        self._testSignature(r"""
[*_0]
output: []

run:
[ -d temp ] || mkdir temp
echo "a.txt" > temp/a.txt

run:

echo "b.txt" > temp/b.txt

[1: shared={'oa':'step_output'}]
dest = ['temp/c.txt', 'temp/d.txt']
input: 'temp/a.txt', 'temp/b.txt', group_by='single', paired_with='dest'
output: _dest

run: expand=True
cp {_input} {_dest[0]}
""", 2)
        # reset env mode
        env.config['sig_mode'] = 'default'
        shutil.rmtree('temp')

    def _testSignature(self, text, steps):
        '''Test recognizing the format of SoS script'''
        env.config['wait_for_task'] = True
        script = SoS_Script(text)
        for f in ['temp/a.txt', 'temp/b.txt']:
            file_target(f).remove('both')
        #
        # only the first step
        wf = script.workflow('default:0')
        env.config['sig_mode'] = 'force'
        res = Base_Executor(wf).run()
        self.assertTrue(os.path.isfile('temp/a.txt'))
        self.assertTrue(os.path.isfile('temp/b.txt'))
        self.assertTrue(res['__completed__']['__step_completed__'], steps)
        with open('temp/a.txt') as ta:
            self.assertTrue(ta.read(), 'a.txt')
        with open('temp/b.txt') as tb:
            self.assertTrue(tb.read(), 'b.txt')
        env.config['sig_mode'] = 'assert'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        # all of them
        wf = script.workflow()
        env.config['sig_mode'] = 'default'
        # generate files (default step 0 and 1)
        Base_Executor(wf).run()
        # now, rerun in build mode
        env.config['sig_mode'] = 'build'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        #
        self.assertTrue(os.path.isfile('temp/c.txt'))
        self.assertTrue(os.path.isfile('temp/d.txt'))
        with open('temp/c.txt') as tc:
            self.assertTrue(tc.read(), 'a.txt')
        with open('temp/d.txt') as td:
            self.assertTrue(td.read(), 'b.txt')
        self.assertEqual(env.sos_dict['oa'], sos_targets(
            'temp/c.txt', 'temp/d.txt'))
        #
        # now in assert mode, the signature should be there
        env.config['sig_mode'] = 'assert'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)

        #
        env.config['sig_mode'] = 'default'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)

        #
        # change script a little bit
        script = SoS_Script('# comment\n' + text)
        wf = script.workflow()
        env.config['sig_mode'] = 'assert'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)

        # add some other variable?
        #script = SoS_Script('comment = 1\n' + text)
        #wf = script.workflow()
        #env.config['sig_mode'] = 'assert'
        #self.assertRaises(Exception, Base_Executor(wf).run)

    def testReexecution(self):
        '''Test -f option of sos run'''
        script = SoS_Script('''

[0]
output: 'a.txt'
run(f"touch {_output}")
''')
        wf = script.workflow()
        try:
            # remove existing output if exists
            file_target('a.txt').remove('both')
        except Exception:
            pass
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        # now, rerun should be much faster
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        # rerun takes less than 1 second
        #
        # force rerun mode
        env.config['sig_mode'] = 'ignore'
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        # regularly take more than 5 seconds to execute
        try:
            # remove existing output if exists
            os.remove('a.txt')
        except Exception:
            pass

    @unittest.skipIf(sys.platform == 'win32', 'Windows executable cannot execute bash loop.')
    def testSignatureAfterRemovalOfFiles(self):
        '''test action shrink'''
        if os.path.isfile('largefile.txt'):
            os.remove('largefile.txt')
        script = SoS_Script(r'''
[10]

# generate a file
output: 'largefile.txt'

run: expand='${ }'
    for x in {1..1000}
    do
        echo $x >> ${_output}
    done

''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        # rerun, because this is the final target, it has to be
        # re-generated
        os.remove('largefile.txt')
        res = Base_Executor(wf).run()
        self.assertTrue(os.path.isfile('largefile.txt'))
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        #
        # we discard the signature, the step would still be
        # skipped because file signature will be calculated
        # during verification
        file_target('largefile.txt').remove('signature')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        #
        # now if we touch the file, it needs to be regenerated
        with open('largefile.txt', 'a') as lf:
            lf.write('something')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        file_target('largefile.txt').remove('both')

    @unittest.skipIf(sys.platform == 'win32', 'Windows executable cannot be created with chmod.')
    def testRemovalOfIntermediateFiles(self):
        # if we zap the file, it
        if os.path.isfile('midfile.txt'):
            os.remove('midfile.txt')
        if os.path.isfile('midfile.txt.zapped'):
            os.remove('midfile.txt.zapped')
        script = SoS_Script(r'''
[10]

# generate a file
output: 'midfile.txt'

run: expand='${ }'
    for x in {1..1000}
    do
        echo $x >> ${_output}
    done

[20]
output: 'finalfile.txt'
run: expand=True
    cp {_input} {_output}
    echo "MORE" >> {_output}
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 2)
        #
        # remove middle file, rerun
        os.remove('midfile.txt')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        self.assertTrue(os.path.isfile('midfile.txt'))
        #
        # we discard the signature, and change midfile rerun
        file_target('midfile.txt').remove('signature')
        with open('midfile.txt', 'a') as mf:
            mf.write('extra')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 2)
        #
        # now if we touch the mid file, it needs to be regenerated
        with open('midfile.txt', 'a') as lf:
            lf.write('something')
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 2)
        #
        # if we zap the mid file, it does not need to be rerun
        subprocess.call('sos remove midfile.txt --zap -y', shell=True)
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        file_target('midfile.txt').remove('both')
        file_target('midfile.txt.zapped').remove('both')
        file_target('final.txt').remove('both')

    def testSignatureWithParameter(self):
        '''Test signature'''
        file_target('myfile.txt').remove('both')
        #
        script = SoS_Script(r'''
parameter: gvar = 10

[10]
# generate a file
output: 'myfile.txt'
# additional comment
run: expand=True
    echo {gvar} > {_output:q}

''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '10')
        #
        # now if we change parameter, the step should be rerun
        wf = script.workflow()
        res = Base_Executor(wf, args=['--gvar', '20']).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '20')
        #
        # do it again, signature should be effective
        wf = script.workflow()
        res = Base_Executor(wf, args=['--gvar', '20']).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '20')

        #
        script = SoS_Script(r'''
parameter: gvar = 10

[10]
# generate a file
output: 'myfile.txt'
# additional comment
run: expand=True
    echo {gvar} > {_output:q}
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '10')
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        #
        # now if we change parameter, the step should be rerun
        wf = script.workflow()
        res = Base_Executor(wf, args=['--gvar', '20']).run()
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '20')
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        #
        # do it again, signature should be effective
        wf = script.workflow()
        res = Base_Executor(wf, args=['--gvar', '20']).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        with open('myfile.txt') as tmp:
            self.assertEqual(tmp.read().strip(), '20')
        file_target('myfile.txt').remove('both')

    def testLoopWiseSignature(self):
        '''Test partial signature'''
        for i in range(10, 12):
            file_target('myfile_{}.txt'.format(i)).remove('both')
        #
        script = SoS_Script(r'''
parameter: gvar = 10

[10]
tt = [gvar]
input: for_each='tt'
output: f"myfile_{_tt}.txt"
run: expand=True
    echo "DO {_tt}"
    echo {_tt} > {_output:q}
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        ts = os.path.getmtime('myfile_10.txt')
        #
        # now we modify the script
        script = SoS_Script(r'''
parameter: gvar = 10

[10]
tt = [gvar, gvar + 1]
input: for_each='tt'
output: f"myfile_{_tt}.txt"
run: expand=True
    echo "DO {_tt}"
    echo {_tt} > {_output:q}
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0.5)
        # this file is not regenerated
        self.assertEqual(ts, os.path.getmtime('myfile_10.txt'))
        ts1 = os.path.getmtime('myfile_11.txt')
        #
        # run it again, neither needs to be rerun
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        self.assertEqual(ts, os.path.getmtime('myfile_10.txt'))
        self.assertEqual(ts1, os.path.getmtime('myfile_11.txt'))
        #
        # change again, the second one is already there.
        script = SoS_Script(r'''
parameter: gvar = 10

[10]
tt = [gvar + 1]
input: for_each='tt'
output: f"myfile_{_tt}.txt"
run: expand=True
    echo "DO {_tt}"
    echo {_tt} > {_output:q}
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        self.assertEqual(ts1, os.path.getmtime('myfile_11.txt'))
        #
        for t in range(10, 12):
            with open('myfile_{}.txt'.format(t)) as tmp:
                self.assertEqual(tmp.read().strip(), str(t))
            file_target('myfile_{}.txt'.format(t)).remove('both')

    def testOutputFromSignature(self):
        'Test restoration of output from signature'''
        self.touch(['1.txt', '2.txt'])
        script = SoS_Script('''
parameter: K = [2,3]

[work_1]
input: "1.txt", "2.txt", group_by = 'single', pattern = '{name}.{ext}'
output: expand_pattern('{_name}.out')
run: expand=True
  touch {_output}

[work_2]

input: group_by = 'single', pattern = '{name}.{ext}', paired_with = ['K']
output: expand_pattern('{_name}.{_K}.out')
run: expand=True
  touch {_output}
    ''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 2)
        # for the second run, output should be correctly constructed
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)
        for file in ['1.out', '2.out', '1.2.out', '2.3.out']:
            file_target(file).remove('both')

    def testSignatureWithVars(self):
        '''Test revaluation with variable change'''
        self.touch(('a1.out', 'a2.out'))
        file_target('b1.out').remove('both')
        file_target('b2.out').remove('both')
        script = SoS_Script('''
parameter: DB = {'input': ['a1.out'], 'output': ['b1.out']}
parameter: input_file = DB['input']
parameter: output_file =  DB['output']

[2]
input: input_file, group_by = 1
output: output_file[_index]
run: expand=True
  touch {_output}
  ''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)
        ts = os.path.getmtime('b1.out')
        #
        script = SoS_Script('''
parameter: DB = {'input': ['a1.out', 'a2.out'], 'output': ['b1.out', 'b2.out']}
parameter: input_file = DB['input']
parameter: output_file =  DB['output']

[2]
input: input_file, group_by = 1
output: output_file[_index]
run: expand=True
  touch {_output}
  ''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0.5)
        self.assertEqual(ts,  os.path.getmtime('b1.out'))

    def testActionSignature(self):
        '''Test action signature'''
        with open('test_action.txt', 'w') as ta:
            ta.write('#something\n')
        script = SoS_Script(r'''
[1]
input: 'test_action.txt'
run: input='test_action.txt', output='lc.txt', expand=True
    wc -l {_input[0]} > lc.txt
''')
        wf = script.workflow()
        Base_Executor(wf).run()
        # the second time, should skip
        Base_Executor(wf).run()
        # force
        env.config['sig_mode'] = 'build'
        Base_Executor(wf).run()

    def testSignatureWithWithoutTask(self):
        '''Test the inclusion of task would not trigger rerun'''
        script = SoS_Script(r'''[1]
output: 'aa'

sh:
  echo aa > aa
''')
        file_target('aa').remove('both')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 1)

        script = SoS_Script(r'''[1]
output: 'aa'

task:



sh:
  echo aa > aa
''')
        wf = script.workflow()
        res = Base_Executor(wf).run()
        self.assertEqual(res['__completed__']['__step_completed__'], 0)


if __name__ == '__main__':
    unittest.main()
