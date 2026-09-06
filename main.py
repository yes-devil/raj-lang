import sys
import re
import subprocess
import os

source_file = sys.argv[1]
target_file = "output.cpp"

if not(source_file[-3:]==".my"):
    print("Not a .my file")

def convertIt(line):
    match = re.match(r'\s*say\((.*)\)\s*', line)

    if not match:
        return line

    args = match.group(1)

    args = re.sub(
        r'sum\(\s*([^,]+)\s*,\s*([^)]+)\)',
        r'(\1 + \2)',
        args
    )

    parts = re.findall(r'"[^"]*"|\'[^\']*\'|[^;;]+', args)

    return '\t' + 'cout << ' + ' << '.join(p.strip() for p in parts) + ';' + '\n'


with open(source_file, "r") as sf, open(target_file, "w") as tf:
    tf.write("#include<iostream>\n")
    tf.write("using namespace std;\n")
    for line in sf:
        if "  say(" in line:
            result = convertIt(line)
            # print(result)
            tf.write(result)
            # tf.write("\tline with say\n")
        else:
            tf.write(line)


subprocess.run(['g++', 'output.cpp', '-o', 'output'])
os.remove('output.cpp')
subprocess.run(['./output'])