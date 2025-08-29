# deobfuscator.py
import re
import ast
import execjs

backup_code = ""
def hex_to_int(match):
    return str(int(match.group(0), 16))

def replacer(match, offset, arr):
    val = int(match.group(1))
    m_index = val - offset
    return f"'{arr[m_index]}'"

def join_strings(match):
    parts = re.findall(r"'([^']*)'", match.group(0))
    return "'" + ''.join(parts) + "'"

def deobfuscate(code):
    backup_code = code # Save original

    # Replace Hex Values
    code = re.sub(r'0[xX][0-9a-fA-F]+', hex_to_int, code)

    # Get offset
    pattern = r"function\s*[\w$]+\([\w$]+,[\w$]+\){.*?return.*?[\w$]+=[\w$]+-(.*?);.*?}"
    match = re.search(pattern, code)
    if match:
        offset = eval(match.group(1))

    # Get target shift and start value
    pattern = r"\(function\(.*?\)\{.*?var\s([\w$]+)=.*?while.*?var\s\w+=(.*?);.*?\}\([\w$]+,(.*?)\)\)";
    match = re.search(pattern, code)
    if match:
        fun_name = match.group(1)
        start_value = match.group(2)
        target = eval(match.group(3))
        code = re.sub(pattern, "", code, count=1)

    # Get array values
    pattern = r"function\s[\w$]+\(\){var\s[\w$]+=(\[.*?\])\;.*?}.*?}"
    match = re.search(pattern, code)
    if match:
        array = match.group(1)

    # Rotate Array
    eval_code = f"arr={array};function {fun_name}(i){{ offset={offset};return arr[i - offset]}};while(true){{ s_val={start_value};if(s_val==={target}){{break;}};arr.push(arr.shift()) }}arr;"
    ctx = execjs.compile(eval_code)
    rotated_array = ctx.eval("arr")

    # Deobfuscate 
    pattern = r"[\w$]+\((\d+)\)"
    code = re.sub(pattern, lambda m: replacer(m, offset, rotated_array), code)

    # Resolve values
    pattern = r"'(?:[^']*)'(?:\s*\+\s*'[^']*')+"
    code = re.sub(pattern, join_strings, code)

    return code