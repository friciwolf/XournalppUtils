#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 21:56:21 2020

@author: mate
"""

# Known Bugs, TODO, FIXME:
#	1, Only the first layer on each page will be copied

import subprocess
import sys
import xml.etree.ElementTree as ET
import time

args = sys.argv

#Testing whether enough arguments are provided
if len(args)<4:
    print("ERROR: please call via Xournalpputils.py --input_file1 --input_file2 ... --output_file")
    exit()

input_files = args[1:-1]
output_file = args[-1]
output_xml = output_file[:output_file.index(".")]+".xml"

xml_files = []

for file in input_files:
    xmlName = file[:file.index(".")]+".xml"
    archiveName = xmlName+".gz"
    subprocess.os.popen("cp "+file+" "+archiveName)
    print("Unpacking "+archiveName+"...")
    print(subprocess.os.popen("gunzip "+archiveName).read())
    time.sleep(1)
    while True:
        try:
            xml_files.append(ET.parse(xmlName))
            break
        except FileNotFoundError: pass
    subprocess.os.popen("rm "+xmlName)


#We'll merge file2 with file1, then call the resulting file file1, and
#  merge this one with file2 .... up to fileN
xml_merged = xml_files[0]
for xml_file2 in xml_files[1:]:
    for elements in xml_file2.getroot():
        if elements.tag!="page": continue
        pageNb = elements[0].attrib["pageno"]
        imatchedElementInMerged = None
        #Finding the same page page in the file to be merged with
        for e in xml_merged.getroot():
            try:
                if e[0].attrib["pageno"]==pageNb:
                    matchedElementInMerged = e[1] #select the <layer> tag -- FIXME always selects the first layer, even if there are multiple layers on the same page!
                    break
            except IndexError:
                continue
        if matchedElementInMerged!=None:
            try:
                for child in elements[1]:
                    ET.SubElement(matchedElementInMerged, child.tag,attrib=child.attrib).text = child.text
            except IndexError:
                continue
        else:
            print(pageNb, "Not found")

xml_merged.getroot().remove(xml_merged.getroot().find("preview"))
xml_merged.write(output_xml)
print("Packing temporary file "+output_xml+"...")
print(subprocess.os.popen("gzip "+output_xml).read())
time.sleep(1)
subprocess.os.popen("mv "+output_xml+".gz "+ output_file)

#printing the tree:

# for xml in xml_files:
#     root = xml.getroot()
#     print(root.tag,root.attrib,root.text)
#     for child in root:
#         print("--"+child.tag,child.attrib,child.text)
#         for child2 in child:
#             print("----"+child2.tag,child2.attrib,child2.text)
#             for child3 in child2:
#                  print("------"+child3.tag, child3.attrib,"+"+str(len(child2)))
#                  break
#     print("-----------")
