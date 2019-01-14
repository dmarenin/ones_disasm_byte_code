import os
import eel

import sections


def do_disasm(file):
    dir = os.path.abspath(os.curdir)

    eel.init(dir + '//app//web') 

    eel.start('main.html', size=(300, 200))  

@eel.expose                     
def handleinput(x):
    if x == 'connected!':
        from test1.test_section_cmd import section_cmd as sec_cmd
        from test1.test_section_proc import section_proc as sec_proc
        from test1.test_section_const import section_const as sec_const
        from test1.test_section_var import section_var as sec_var

        line = ''

        lines = sections.disasm(sec_cmd=sec_cmd, sec_proc=sec_proc, sec_const=sec_const, sec_var=sec_var)

        for l in lines:
            line += l

        eel.post(line) 


    print('%s' % x)

