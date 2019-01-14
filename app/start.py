import sys
import os

import app
import sections


def do_disasm(file):
    from test1.test_section_cmd import section_cmd as sec_cmd
    from test1.test_section_proc import section_proc as sec_proc
    from test1.test_section_const import section_const as sec_const
    from test1.test_section_var import section_var as sec_var
    
    f = open('test1\\result.txt', 'w', encoding='utf-8')

    lines = sections.disasm(sec_cmd=sec_cmd, sec_proc=sec_proc, sec_const=sec_const, sec_var=sec_var)

    for line in lines:
        f.write(line)
    
    f.close()


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) != 2:
        print(f"""args:
        c or g 
        file name""")

    type = args[0]
    file = args[1]

    if type == 'c':
        do_disasm(file)
    elif type == 'g':
        app.do_disasm(file)
    
