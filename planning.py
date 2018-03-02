#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 2015-2016 Programacao 1 (LTI)
# 46593 Patrícia Jesus

from consultStatus import *
from timeTT import *
from constants import *
from copy import deepcopy
from operator import itemgetter

def charges(services):
    '''
    Changes driver status from charges to standby
    Requires: A list with the service
    Ensures: The same list actualized
    '''
    services[INDEXDriverStatus] = STATUSStandBy
    services[INDEXClientName] = NOCLIENT
    services[INDEXDepartureHour] = MinIntHourString(HoursMinInt(services[INDEXArrivalHour])+60)
    services[INDEXArrivalHour] = MinIntHourString(HoursMinInt(services[INDEXArrivalHour])+60)
    services[INDEXCircuitId] = NOCIRCUIT
    services[INDEXCircuitKms] = 0
    services[INDEXAccumulatedKms] = 0
    return services

def updateTime(services):
    '''
    Adds the time that it takes to do the circuit to the driver accumulated time
    Requires: Drivers services with the reservation updated
    Ensures: The update of the accumulated time of the driver
    '''
    timeMinDiff = HoursMinInt(services[INDEXArrivalHour])-HoursMinInt(services[INDEXDepartureHour])
    timeMinAdd = timeMinDiff + HoursMinInt(services[INDEXAccumulatedTime])
    time = MinIntHourString(timeMinAdd)
    return time

def reservationTime(reservation):
    '''
    Diference between the time of the reservation
    Requires: A reservation list
    Ensures: The diference between the beginning and the end of the reservation
    '''
    time = HoursMinInt(reservation[INDEXRequestedEndHour])-HoursMinInt(reservation[INDEXRequestedStartHour])
    return time

def differenceTime(service,reservation):
    '''
    Diference between the time of the service arrival and the reservation started
    Requires: A reservation list and a service list
    Ensures: The diference between the beginning of the next reservation and the end of the previous service
    '''
    time = HoursMinInt(service[INDEXArrivalHour]) - HoursMinInt(reservation[INDEXRequestedStartHour])
    return time

def updateServices(reservations_p, waiting4ServicesList_prevp):

    """Assigns drivers with their vehicles to services that were reserved.
    
    Requires:
    reservations_p is a list with a structure as in the output of
    consultStatus.readReservationsFile; waiting4ServicesList_prevp is a list
    with the structure as in the output of consultStatus.waiting4ServicesList;
    objects in reservations_p concern a period p, and objects in
    waiting4ServicesList_prevp concern a period immediately preceding p.
    Ensures:
    list L of lists, where each list has the structure of
    consultStatus.readServicesFile, representing the services to be provided
    in a period starting in the beginning of the period p upon they having
    been reserved as they are represented in reservations_p;
    Reservations with earlier booking times are served first (lexicographic
    order of clients' names is used to resolve eventual ties);
    Drivers available earlier are assigned services first (lexicographic
    order of their names is used to resolve eventual ties) under
    the following conditions:
    If a driver has less than 30 minutes left to reach their 5 hour
    daily limit of accumulated activity, he is given no further service
    in that day (this is represented with a service entry marhed with
    "terminates");
    Else if a vehicle has less than 15 kms autonomy, it is recharged
    (this is represented with a service entry marked with "charges") and
    is available 1 hour later, after recharging (this is represented with
    another service entry, marked with "standby").
    in this list L:
    drivers terminating their services earlier have priority over the ones
    terminating later;
    in case of eventual ties, drivers with less accumulated time have
    priority over the ones with more accumulated time;
    lexicographic order of drivers's names decides eventual ties
    in each case above.
    """

    newList = []
    update = deepcopy(waiting4ServicesList_prevp)
    reservations = deepcopy(reservations_p)
    count = 0
    
    while len(reservations) > 0:
        same = deepcopy(reservations[0])
        while count < len(update):
            reserv=deepcopy(count)
            if update[count][INDEXDriverStatus] == STATUSCharging:
                    charges(update[count])
                    count+=1
                    
            elif update[count][INDEXDriverStatus] == STATUSTerminated:
                    count+=1
                    
            if reservations == []:
                count = len(update)
                
            else:
                timeLeft = HoursMinInt(TIMELimit) - HoursMinInt(update[count][INDEXAccumulatedTime])
                if (reservationTime(reservations[0]) <= timeLeft):
                    if (int(update[count][INDEXINDEXVehicAutonomy])-int(update[count][INDEXAccumulatedKms])) > int(reservations[0][INDEXCircuitKmsInReservation]):
                        update[count][INDEXClientName] = reservations[0][INDEXClientNameInReservation] #cliente
                        
                        if HoursMinInt(update[count][INDEXArrivalHour]) <= HoursMinInt(reservations[0][INDEXRequestedStartHour]):
                            update[count][INDEXDepartureHour] = reservations[0][INDEXRequestedStartHour] #inicio
                            update[count][INDEXArrivalHour] = reservations[0][INDEXRequestedEndHour] #fim
                        else:
                            update[count][INDEXDepartureHour] = MinIntHourString(differenceTime(update[count],reservations[0]) + HoursMinInt(reservations[0][INDEXRequestedStartHour]))
                            update[count][INDEXArrivalHour] = MinIntHourString(differenceTime(update[count],reservations[0]) + HoursMinInt(reservations[0][INDEXRequestedEndHour]))
                            
                        update[count][INDEXCircuitId] = reservations[0][INDEXCircuitInReservation] #circuito
                        update[count][INDEXCircuitKms] = reservations[0][INDEXCircuitKmsInReservation] #km circuito
                        update[count][INDEXAccumulatedTime] = updateTime(update[count]) #tempo condutor
                        update[count][INDEXAccumulatedKms] = str(int(update[count][INDEXAccumulatedKms]) + int(update[count][INDEXCircuitKms])) #km feitos
                        reservations.remove(reservations[0])
                        timeLeft = HoursMinInt(TIMELimit) - HoursMinInt(update[count][INDEXAccumulatedTime])
                        
                        if timeLeft < HoursMinInt(TIMEThreshold):
                            update[count][INDEXDriverStatus] = STATUSTerminated
                            
                        if (int(update[count][INDEXINDEXVehicAutonomy])-int(update[count][INDEXAccumulatedKms]) < AUTONThreshold):
                            update[count][INDEXDriverStatus] = STATUSCharging
                elif (same == reservations[0]) and ((reserv == (count-1) or ((reserv ==0) and count == (len(update)-1)))):
                    reservations.remove(reservations[0])
                count += 1
        for lista in update:
            lista[INDEXArrivalHour] = lista[INDEXArrivalHour].strip(' ')
                    
        update = sorted(update, \
                         key=itemgetter(INDEXArrivalHour, \
                                        INDEXAccumulatedTime, \
                                        INDEXDriverName))
        for i in update:
            if newList.count(i) == 0 and waiting4ServicesList_prevp.count(i) == 0:
                newList.append(deepcopy(i))
        count = 0
        
    for lista in update:
        if lista[INDEXDriverStatus] == STATUSCharging:
            charges(lista)

    for i in update:
            if newList.count(i) == 0 and waiting4ServicesList_prevp.count(i) == 0:
                newList.append(deepcopy(i))

    for lista in newList:
        lista[INDEXArrivalHour] = lista[INDEXArrivalHour].strip(' ')
    
    newList = sorted(newList, \
                     key=itemgetter(INDEXArrivalHour, \
                                    INDEXDriverName))
        
    for i in newList:
        i.pop()
        i.pop()
        i.pop()
    return newList
