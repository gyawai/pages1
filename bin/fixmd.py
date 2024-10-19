#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re
import argparse

def parse_argument():
    ap = argparse.ArgumentParser(description='Fix non-standard markdown expressions.')
    ap.add_argument('-i', '--infile', required = True)
    ap.add_argument('-d', '--debug', action = 'store_true')
    args = ap.parse_args()
    return args                            

def read_lines(fname):
    if fname:
        f = open(fname, errors='ignore')
    else:
        f = sys.stdin
    lines = f.readlines()
    f.close()
    return lines

def fix_line(line, next_line):
    line = line.rstrip()
    line = fix_anchor(line)
    res = fix_image(line, next_line.rstrip())
    line = res[1]
    if res[0] == 2:
        next_line = res[2]
    return line, next_line

def fix_anchor(line):
    m = re.search(r'(.*)\[\]{(\#.+?)}(.*)', line)
    if not m: return line
    line = m.group(1) + m.group(3)
    anchor = m.group(2)
    m = re.match(r'(.*)\s+{\#.+}', line)
    if m:
        line = m.group(1)
    line = line + f' {{{anchor}}}'
    return line

#
# xxx ![](/url/of/the/image.png){width="128" height="64"}
# =>
# xxx <img src="/url/of/the/image.png" width="128" height="64" />
#
# Embedded image line can be very long and thus it might be wrapped into two lines.
# We need to take care of such cases.
# We don't think about very very long line wrapped into three or more lines, though.
#
def fix_image(line, next_line):
    m = re.search(r'(.*)\!\[\]\((.+?)\)\{(.*)\}(.*)', line + next_line)
    if not m: return (1, line)

    preamble = m.group(1)
    url = m.group(2)
    css = m.group(3)
    remnant = m.group(4)

    w = ''
    m = re.search(r'width="(\d+)"', css)
    if m:
        w = f'width="{m.group(1)}"'

    h = ''
    m = re.search(r'height="(\d+)"', css)
    if m:
        h = f'height="{m.group(1)}"'

    html = f'<img src="{url}" {w} {h} />'
    return (2, html, remnant)

def main(args=None):
    if args is None:
        args = parse_argument()
    lines = read_lines(args.infile)
    '''
    for line in lines:
        line1 = fix_line(line)
        print(line1, file=sys.stdout)
    '''

    i = 0
    while i < len(lines):
        line0 = lines[i]
        if i < len(lines) - 1:
            line1 = lines[i+1]
        else:
            line1 = ''
        line_fixed, next_line = fix_line(line0, line1)
        if i < len(lines) - 1:
            lines[i+1] = next_line
        print(line_fixed, file=sys.stdout)
        i += 1

    
if __name__ == "__main__":
    import sys
    sys.exit(main())



