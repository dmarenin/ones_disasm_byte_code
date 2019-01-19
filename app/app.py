import os
import eel

import json
from operator import itemgetter

import sections


def do_disasm(file):
    dir = os.path.abspath(os.curdir)

    eel.init(dir + '//app//web') 

    try:
        eel.start('main.html', size=(800, 1200)) 
    except:
        pass

@eel.expose                     
def handleinput(x):
    if x == 'connected!':
        from test1.test_section_cmd import section_cmd as sec_cmd
        from test1.test_section_proc import section_proc as sec_proc
        from test1.test_section_const import section_const as sec_const
        from test1.test_section_var import section_var as sec_var

        line = ''

        lines = sections.disasm(sec_cmd=sec_cmd, sec_proc=sec_proc, sec_const=sec_const, sec_var=sec_var)

        size = 3500
        color = "#003030"
        font = {'color': '#ffffff', 'face': 'monospace', 'align': 'left'}
        shape = 'box'
        
        nodes = []
        edges = []

        stack = None
        for index, l in enumerate(lines):

            if '= S U B R O U T I N E =' in l:
                if not stack is None:
                    nodes.append(stack)
                    edges.append({'from': stack['id'], 'to': l[5:13], 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier', 'enabled': False}})

                stack = {'id': l[5:13], 'size': size, 'label': l, 'color': color, 'shape': shape, 'font': font}

            elif l[14:17]=='loc':
                nodes.append(stack)
               
                if last_op == 'Jmp':
                    edges.append({'to': stack['id'], 'from': lines[index-1][50:61].rstrip().rjust(8, '0'), 'arrows': 'from', 'physics': False, 'smooth': {'type': 'cubicBezier', 'enabled': False}})
                else:
                    edges.append({'from': stack['id'], 'to': l[5:13], 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier', 'enabled': False}})
                
                stack = {'id': l[5:13], 'size': size, 'label': l, 'color': color, 'shape': shape, 'font': font}
            
            elif l[25:27]=='JZ' or l[25:28]=='JNZ':
                stack['label'] = stack['label'] + l
                nodes.append(stack)
                edges.append({'from': stack['id'], 'to': l[50:61].rstrip().rjust(8, '0'), 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier', 'enabled': False}})
                edges.append({'from': stack['id'], 'to': lines[index+1][5:13], 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier', 'enabled': False}})

                stack = {'id': lines[index+1][5:13], 'size': size, 'label': '', 'color': color, 'shape': shape, 'font': font}

            elif not stack is None:
                stack['label'] = stack['label'] + l

            last_op = l[25:28]


        edges = sorted(edges, key=lambda k: k['from']) 
        edges = sorted(edges, key=lambda k: k['to']) 

        nodes = sorted(nodes, key=lambda k: k['id']) 

        data = {'edges':edges, 'nodes':nodes}

        eel.post(json.dumps(data)) 
        
    print('%s' % x)

