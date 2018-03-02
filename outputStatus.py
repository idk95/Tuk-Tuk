#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 2015-2016 Programacao 1 (LTI)
# 46593 Patrícia Jesus

from planning import *
from consultStatus import *
from copy import deepcopy

def writeServicesFile(services_p, file_name_p, header_p):
    """Writes a collection of services into a file.

    Requires:
    services_p is a list with the structure as in the output of
    updateServices representing the services in a period p;
    file_name_p is a str with the name of a .txt file whose end (before
    the .txt suffix) indicates the period p, as in the examples provided in
    the general specification (omitted here for the sake of readability);
    and header is a string with a header concerning period p, as in
    the examples provided in the general specification (omitted here for
    the sake of readability).
    Ensures:
    writing of file named file_name_p representing the collection of
    services in services_p and organized as in the examples provided in
    the general specification (omitted here for the sake of readability);
    in the listing in this file keep the ordering of services in services_p.
    """
    header = ''
    line = ''
    
    for i in header_p:
        header += i
           
    header += 'Services:\n'
    
    f=open(file_name_p,'w')
    f.write(header)
    for linha in services_p:
        for j in linha:
            line+=(str(j)+', ')
        line = line[:-2]
        line += '\n'
        f.write(line)
        line = ''
    f.close()
    return file_name_p
    

