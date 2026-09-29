import sys
import re
import subprocess
import os
from pathlib import Path

source_file = sys.argv[1]
target_file = str(Path("~/raj-language/temp/output.cpp").expanduser())
# print(target_file)

if not(source_file[-4:]==".raj"):
    print("Not a .raj file")
    sys.exit(0)

def _say(line):
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

    return '\t' + 'std::cout << ' + ' << '.join(p.strip() for p in parts) + ';' + '\n'

def _sayln(line):
    match = re.match(r'\s*sayln\((.*)\)\s*', line)

    if not match:
        return line

    args = match.group(1)
    if len(args) == 0:
        return '\t' + 'std::cout << std::endl;' + '\n'

    args = re.sub(
        r'sum\(\s*([^,]+)\s*,\s*([^)]+)\)',
        r'(\1 + \2)',
        args
    )

    parts = re.findall(r'"[^"]*"|\'[^\']*\'|[^;;]+', args)

    return '\t' + 'std::cout << ' + ' << '.join(p.strip() for p in parts) + ' << std::endl;' + '\n'


def _ask(line):
    match = re.match(r'\s*ask\((.*)\)\s*', line)

    if not match:
        return line

    args = match.group(1)

    args = re.sub(
        r'sum\(\s*([^,]+)\s*,\s*([^)]+)\)',
        r'(\1 + \2)',
        args
    )

    parts = re.findall(r'"[^"]*"|\'[^\']*\'|[^;;]+', args)

    return '\t' + 'std::cin >> ' + ' >> '.join(p.strip() for p in parts) + ';' + '\n'

def _use(line):
    words = line.split()
    if words[1] == "raj":
        path = str(Path("~/raj-language/utils").expanduser())
        # print("got the expanded path ", path, type(path))
        return "#include \"" + path + "/" + words[2]+ ".h\"" + "\n"
    else:
        return "#include<" + words[1] + '>'  + "\n"

def _let(line):
    words = line.split()
    return "#define " + words[1] + " " + words[2]  + "\n"


with open(source_file, "r") as sf, open(target_file, "w") as tf:
    tf.write("#include<iostream>\n")
    # tf.write("using namespace std;\n")
    for line in sf:
        # result = ""
        if "   say(" in line:
            result = _say(line)
            # print(result)
            tf.write(result)
            # tf.write("\tline with say\n")
        elif "   ask(" in line:
            result = _ask(line)
            # print(result)
            tf.write(result)
            # tf.write("\tline with say\n")
        elif "   sayln(" in line:
            result = _sayln(line)
            tf.write(result)
        elif line[0:3] == "use":
            result = _use(line)
            tf.write(result)
        elif line[0:3] == "let":
            result = _let(line)
            tf.write(result)

        else:
            tf.write(line)


subprocess.run(['g++', target_file, '-o', 'output'])
# os.remove(tf)
subprocess.run(['./output'])
