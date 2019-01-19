import os
import eel

import json

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

        nodes = []
        edges = []

        d = None
        for l in lines:
            line += l

            if '= S U B R O U T I N E =' in l:
                if not d is None:
                    nodes.append(d)

                d = {}
                d['id'] = l[4:15]
                d['size'] = 150
                d['label'] = l
                d['color'] = "#003030"
                d['shape'] = 'box'
                d['font'] = {'color': '#ffffff', 'face': 'monospace', 'align': 'left'}
                
            if not d is None:
                  d['label'] = d['label'] + l
            #if 'Ret' in l:
            #    nodes.append(d)




#        edges = [
#{'from': "cfg_0x00405a2e", 'to': "cfg_0x00405a39", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a2e", 'to': "cfg_0x00405a49", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a49", 'to': "cfg_0x00405a4e", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a49", 'to': "cfg_0x00405a62", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a55", 'to': "cfg_0x00405a5f", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a55", 'to': "cfg_0x004095c6", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x004095c6", 'to': "cfg_0x00417563", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a39", 'to': "cfg_0x00403450", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a39", 'to': "cfg_0x00405a49", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00403450", 'to': "cfg_0x00403489", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00403450", 'to': "cfg_0x0042f03f", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a4e", 'to': "cfg_0x00405a55", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a4e", 'to': "cfg_0x00405a62", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#{'from': "cfg_0x00405a5f", 'to': "cfg_0x00405a62", 'arrows': 'to', 'physics': False, 'smooth': {'type': 'cubicBezier'}},
#];


        data = {'edges':edges, 'nodes':nodes}

        eel.post(json.dumps(data)) 
        
        #line = ''

        #for l in sec_proc:
        #    line += l
        
        #eel.post2(line) 


    print('%s' % x)

