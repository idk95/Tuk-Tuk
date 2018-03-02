#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 2015-2016 Programacao 1 (LTI)
# 46593 Patrícia Jesus

from consultStatus import *
from outputStatus import *
from timeTT import *
from constants import *
from planning import *
from sys import argv

def update(nextPeriod, driversFileName, vehiclesFileName, servicesFileName, reservationsFileName):
    """Obtains the planning for a period of activity.

    Requires:
     - nextPeriod is a str from the set 0911, 1113, ..., 1921 indicating the 2 hour period to be planned;
     - driversFileName is a str with the name of a .txt file containing a list of drivers organized as in the examples provided;
     - vehiclesFileName is a str with the name of a .txt file containing a list of vehicles organized as in the examples provided;
     - servicesFileName is a str with the name of a .txt file containing a list of services organized as in the examples provided;
     - reservationsFileName is a str with the name of a .txt file containing a list of reserved services organized as in the examples provided;
     - the files whose names are driversFileName, vehiclesFileName, servicesFileName and reservationsFileName concern the same company and the same day;
     - the file whose name is reservationsFileName concerns the period indicated by nextPeriod;
     - the files whose names are driversFileName, vehiclesFileName, servicesFileName concern the period immediately preceding the period indicated by nextPeriod;
     - the file name reservationsFileName ends (before the .txt extension) with the string nextPeriod;
     - the file names driversFileName, vehiclesFileName and servicesFileName end (before their .txt extension) with the string representing
     - the period immediately preceding the one indicated by nextPeriod, from the set 0709, 0911, ..., 1719;
    Ensures:
     - writing of .txt file containing the updated list of services for the period nextPeriod according to the requirements in the general specifications provided (omitted here for the sake of readability);
     - the name of that file is outputXXYY.txt where XXYY represents the nextPeriod.
    """
    
    driversFileName = driversFileName+'.txt'
    vehiclesFileName = vehiclesFileName+'.txt'
    servicesFileName = servicesFileName+'.txt'
    reservationsFileName = reservationsFileName+'.txt'
    file_name_p = 'output'+nextPeriod+'.txt'
    header_p = []

    try:
        assert driversFileName.find(nextPeriod) == -1
    except(AssertionError):
        raise Exception('Drivers file as the same period as the nextPeriod')

    try:
        assert vehiclesFileName.find(nextPeriod) == -1
    except(AssertionError):
        raise Exception('Vehicles file as the same period as the nextPeriod')

    try:
        assert servicesFileName.find(nextPeriod) == -1
    except(AssertionError):
        raise Exception('Services file as the same period as the nextPeriod')

    try:
        assert reservationsFileName.find(nextPeriod) != -1
    except(AssertionError):
        raise Exception('Reservations file as a diferent period as the nextPeriod')
    
    reservations = open(reservationsFileName,'r')
    for i in range(NUMBEROfLinesInHeader-1):
        header_p.append(deepcopy(reservations.readline()))
    reservations.close()
    
    waiting = waiting4ServicesList(readDriversFile(driversFileName), readVehiclesFile(vehiclesFileName),readServicesFile(servicesFileName))
    update = updateServices(readReservationsFile(reservationsFileName), waiting)    
    output = writeServicesFile(update, file_name_p, header_p)
    
    return output

#update(argv[1], argv[2], argv[3], argv[4], argv[5])

if __name__ == "__main__":
    update(argv[1], argv[2], argv[3], argv[4], argv[5])
