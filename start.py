from op_codes import list as op_codes
from op_codes import list_loc as list_loc
from op_codes import sys_call_flags as sys_call_flags
from op_codes import meta_type_proc as meta_type_proc

import re

def print_op_code():
    print(op_codes)

def read_section_cmd(sec):
    result = []
    n = 0
    
    sec_list = re.findall(r'\w+', sec)
    
    for index, item in enumerate(sec_list):
        if index % 2 == 0:
            op = op_codes.get(int(sec_list[index]))
            result.append({'o': sec_list[index], 'op': op, 'p': sec_list[index+1], 'op_raw': sec_list[index], 'p_raw': sec_list[index+1], 'n': n})
            n += 1

    return result

def read_section_proc(sec):
    result = {'list_proc': [],
              'pointer_cmd': {}
              }

    sec_list = re.split(r'[\n]', sec)

    for x in sec_list:
        proc_str = re.findall(r'\w+', x)

        if len(proc_str) == 0:
            continue

        proc = {'name_proc': proc_str[0],
                'type_proc': proc_str[1],
                'type_proc2': proc_str[2],
                'num_sec_cmd': proc_str[3],
                'par_proc': [],
                'len_par_proc': 0,
                }

        if len(proc_str)>4:
            len_par_proc = int(proc_str[5])
            proc['len_par_proc'] = len_par_proc

            base = 6

            i = 0
            while i <= len_par_proc-1:
                proc['par_proc'].append(proc_str[base+i*3])
                i += 1

        result['list_proc'].append(proc)
        if not proc_is_sys_call(proc_str[1]):
            result['pointer_cmd'][int(proc['num_sec_cmd'])] = proc

    return result

def read_section_const(sec):
    result = []
    
    sec_list = re.split(r'[\n]', sec)
    
    for x in sec_list:
        x = x.replace('{', '')
        x = x.replace('},', '')
        
        result.append({'value': x[4:], 'type': x[0:3]})

    return result

def read_section_var(sec):
    result = []
    
    sec_list = re.split(r'[\n]', sec)
    
    for x in sec_list:
        x = x.replace('{', '')
        x = x.replace('},', '')

        x = x.split(',')
        if len(x) != 3:
            continue
        
        result.append({'value': x[0], 'par1': x[1], 'par2': x[2]})

    return result

def proc_is_sys_call(flag):
    return int(flag) in sys_call_flags

def get_list_xref(sec):
    result = {}

    for x in sec:
        if x['op'] in list_loc:
            result[int(x['p'])] = 'loc_'+x['p']
            x['p'] = 'loc_'+x['p']

    return result

def disasm(**data):
    section_cmd = read_section_cmd(data['sec_cmd'])
    section_proc = read_section_proc(data['sec_proc'])
    section_const = read_section_const(data['sec_const'])
    section_var = read_section_var(data['sec_var'])

    list_xref = get_list_xref(section_cmd)

    lines = []
    
    line = f"""section .cmd\n"""
    lines.append(line)
    
    for x in section_cmd:
        n = str(x['n']).rjust(8, '0')
        op = x['op'].ljust(20, ' ')
        p = x['p'].ljust(5, ' ')
        
        proc = section_proc['pointer_cmd'].get(x['n'])

        line = ''

        if not proc is None:
            type_proc = int(proc['type_proc'])

            type_proc = meta_type_proc.get(type_proc)

            line += f""".cmd:{n}; =============== S U B R O U T I N E =======================================\n"""

            line += f""".cmd:{n};flags: {proc['type_proc']}, {proc['type_proc2']}\n"""
            line += f""".cmd:{n}\n"""
            line += f""".cmd:{n} {type_proc['meta_type']}\n"""
            line += f""".cmd:{n} {proc['name_proc']} {type_proc['dir_proc']}\n"""
            line += f""".cmd:{n}\n"""

            for index, item in enumerate(proc['par_proc']):
                 line += f""".cmd:{n} arg{index} = {item}\n"""

            line += f""".cmd:{n} \n"""

        xref = list_xref.get(x['n'])
        if not xref is None:
            line += f""".cmd:{n} {xref}\n"""

        if x['op'] == 'Call':
            proc = section_proc['list_proc'][int(x['p'])]
            p = proc['name_proc']

            type_proc = proc['type_proc']

            if proc_is_sys_call(type_proc):
                p = 'sys_call: ' + p
        
        elif x['op'] == 'PushConst':
            value = section_const[int(p)]['value'] 
            #p = f"""{p} ; {value} """ 
            p = f"""{value} ; .const*{p} """ 

        elif x['op'] == 'New':
            value = section_const[int(p)]['value'] 
            #p = f"""{p} ; Новый {value}""" 
            p = f"""Новый {value} ; .const*{p} """ 
        
        elif x['op'] == 'CallObjectProcedure':
            value = section_const[int(p)]['value'] 
            #p = f"""{p} ; {value}""" 
            p = f"""{value} ; .const*{p} """ 
        
        elif x['op'] == 'CallObjectFunction':
            value = section_const[int(p)]['value'] 
            #p = f"""{p} ; {value}""" 
            p = f"""{value} ; .const*{p} """ 

        elif x['op'] == 'PushStatic':
            value = section_var[int(p)]['value'] 
            #p = f"""{p} ; {value}""" 
            p = f"""{value} ; .var*{p} """ 

        line += f""".cmd:{n}            {op} {p}          """
        #line += f"""[{x['op_raw']}, {x['p_raw']}] \n"""

        line += """\n""" 

        lines.append(line)

    line = f"""section .const\n"""
    lines.append(line)

    for index, item in enumerate(section_const):
        n = str(index).rjust(8, '0')
      
        line = f""".const:{n} {item['value']} ; type = {item['type']}\n"""

        lines.append(line)
    
    line = f"""section .var:\n"""
    lines.append(line)   
    
    for index, item in enumerate(section_var):
        n = str(index).rjust(8, '0')
      
        line = f""".var:{n} {item['value']} ; {item['par1']}, {item['par1']}\n"""

        lines.append(line)
    
    line = f"""section .proc:\n"""
    lines.append(line)   
    
    for index, item in enumerate(section_proc['list_proc']):
        n = str(index).rjust(8, '0')
      
        par_proc = ''
        for x in item['par_proc']:
            par_proc += x
            par_proc += ', '

        line = f""".proc:{n} name = {item['name_proc']}; args = {par_proc} \n"""

        lines.append(line)    
              
    return lines


if __name__ == "__main__":
    #print_op_code()

    from test_section_cmd import section_cmd as sec_cmd
    from test_section_proc import section_proc as sec_proc
    from test_section_const import section_const as sec_const
    from test_section_var import section_var as sec_var
    
    lines = disasm(sec_cmd=sec_cmd, sec_proc=sec_proc, sec_const=sec_const, sec_var=sec_var)

    f = open('result.txt', 'w', encoding='utf-8')

    for line in lines:
        f.write(line)
    
    f.close()
    
    print("")

