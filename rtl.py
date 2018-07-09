#!/usr/bin/env python3
#
# Author: cbdev <cb@cbcdn.com>
# Reference: https://github.com/cbdevnet/rtl2dot 
#
#This program is free software. It comes without any warranty, to
#the extent permitted by applicable law. You can redistribute it
#and/or modify it under the terms of the Do What The Fuck You Want
#To Public License, Version 2, as published by Sam Hocevar and 
#reproduced below.
#
#DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#Version 2, December 2004 
#
#Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
#	Everyone is permitted to copy and distribute verbatim or modified 
#	copies of this license document, and changing it is allowed as long 
#	as the name is changed. 
#
#DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#	0. You just DO WHAT THE FUCK YOU WANT TO.
#

import fileinput
import re
import sys

root = "main"
ignore = None
infiles = []

local = False
indirects = False

infiles.append(sys.argv[1])
current = ""
calls = {}

func_old = re.compile("^;; Function (?P<func>\S+)\s*$")
func_new = re.compile("^;; Function (?P<mangle>.*)\s+\((?P<func>\S+)(,.*)?\).*$")
funcall = re.compile("^.*\(call.*\"(?P<target>.*)\".*$")
symref = re.compile("^.*\(symbol_ref.*\"(?P<target>.*)\".*$")

def enter(func):
    global current, calls
    current = func
    if calls.get(current, None) is not None:
        print("Ambiguous function name " + current, file=sys.stderr)
    else:
        calls[current] = {}

def call(func, facility):
    global calls
    if calls[current].get(func, None) is not None and calls[current][func] != facility:
        print("Ambiguous calling reference to " + func, file=sys.stderr)
    calls[current][func] = facility

def dump(func):
    global calls
    if calls.get(func, None) is None:
        # edge node
        return
    for ref in calls[func].keys():
        if calls[func][ref] is not None:
            style = "" if calls[func][ref] == "call" else ' [style="dashed"]'
            if local and calls.get(ref, None) is None:
                # non-local function
                continue
            if not indirects and calls[func][ref] == "ref":
                # indirect reference, but not requested
                continue
            if ignore is None or re.match(ignore, ref) is None:
                # Invalidate the reference to avoid loops
                calls[func][ref] = None
                print('"' + func + '" -> "' + ref + '"' + style + ';')
                dump(ref)

# Scan the rtl dump into the dict
for line in fileinput.input(infiles):
    if re.match(func_old, line) is not None:
        # print "OLD", re.match(func_old, line).group("func")
        enter(re.match(func_old, line).group("func"))
    elif re.match(func_new, line) is not None:
        # print "NEW", re.match(func_new, line).group("func"), "Mangled:", re.match(func_new, line).group("mangle")
        enter(re.match(func_new, line).group("func"))
    elif re.match(funcall, line) is not None:
        # print "CALL", re.match(funcall, line).group("target")
        call(re.match(funcall, line).group("target"), "call")
    elif re.match(symref, line) is not None:
        # print "REF", re.match(symref, line).group("target")
        call(re.match(symref, line).group("target"), "ref")

print("digraph callgraph {")
dump(root)
print("}")

graph =[]
for i in calls:
    for j in calls[i]:
        print(j[0])
        if(j[0] == '*'):
            continue
        elif(j[0] == '_'):
            print("here ",j)
            continue
        else:
            graph.append([i,str(j)])
        #print(i[0]+"->"+str(j))

fp = open('funcalls.txt','w')
for i in graph:
    fp.write(i[0]+'->'+i[1]+'\n')
fp.close()