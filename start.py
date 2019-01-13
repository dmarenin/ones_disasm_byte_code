from op_codes import list as op_codes
from op_codes import list_loc as list_loc
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
        result['pointer_cmd'][int(proc['num_sec_cmd'])] = proc

    return result

def get_list_xref(sec):
    result = {}

    for x in sec:
        if x['op'] in list_loc:
            result[int(x['p'])] = 'loc_'+x['p']
            x['p'] = 'loc_'+x['p']

    return result

if __name__ == "__main__":
    #print_op_code()

    from test_section_cmd import section_cmd as sec_cmd
    from test_section_proc import section_proc as sec_proc

    section_cmd = read_section_cmd(sec_cmd)
    section_proc = read_section_proc(sec_proc)
    section_const = None
    section_var = None

    list_xref = get_list_xref(section_cmd)

    for x in section_cmd:
        n = str(x['n']).rjust(8, '0')
        op = x['op'].ljust(20, ' ')
        p = x['p'].ljust(5, ' ')
        
        proc = section_proc['pointer_cmd'].get(x['n'])

        if not proc is None:
            print(f""".cmd:{n}; =============== S U B R O U T I N E =======================================""")
            print(f""".cmd:{n}""")
            print(f""".cmd:{n} proc type={proc['type_proc']} type2={proc['type_proc2']}""")
            print(f""".cmd:{n} {proc['name_proc']}""")

            for index, item in enumerate(proc['par_proc']):
                 print(f""".cmd:{n} arg{index} = {item}""")

            print(f""".cmd:{n}""")

        xref = list_xref.get(x['n'])
        if not xref is None:
            print(f""".cmd:{n} {xref}""")

        if x['op'] == 'Call':
            proc = section_proc['list_proc'][int(x['p'])]
            p = proc['name_proc']

        print(f""".cmd:{n}            {op} {p}    ;[{x['op_raw']}, {x['p_raw']}]""")



    print("")

