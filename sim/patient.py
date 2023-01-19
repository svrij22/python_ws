
import numpy as np
import random

#INTERVAL
EXPO_VARIABLE_UNPLANNED = 4.510619958847755
EXPO_VARIABLE_PLANNED = 3.5689520791638496
def new_patient_interval(isPlanned):
    if (isPlanned):
        return np.random.exponential(EXPO_VARIABLE)
    else:
        return np.random.exponential(EXPO_VARIABLE)

#Time on ICU
#Return value in HOURS
CALC_MU = 3.50502901187668
CALC_SIGMA = 1.3165461050924663
def new_prodecure_length():
    return np.random.lognormal(CALC_MU, CALC_SIGMA)

#Generate specialism
def new_specialism(isPlanned):
    if (isPlanned):
        return random.choices(['CAPU', 'CHIR', 'NEC', 'INT', 'NEU', 'CARD', 'OTHER'], weights=(1301, 118, 45, 19, 9, 6, 1))[0]
    else:
        return random.choices(['CAPU', 'CHIR', 'NEC', 'INT', 'NEU', 'CARD', 'OTHER'], weights=(997, 448, 426, 317, 309, 150, 53))[0]

#RANDOM
PATIENT_AMOUNT = 4199
PATIENT_IS_PLANNED_AMOUNT = 1499

#Return is planned
#Return value in BOOL
def rand_is_planned():
    if (random.randrange(0, 4199) < 1499):
        return True
    return False

#Define patients to reschedule
class Reschedule:

    def __init__(self, patient, hours):
        self.patient = patient
        self.hoursToGo = hours
        
        self.attempts = 0
        self.remove_me = False
        
    def hours_has_passed(self, hours):
        self.hoursToGo -= hours

    def should_be_replanned(self):
        return (self.hoursToGo < 0)

    def should_be_removed(self):
        return self.remove_me
        
#PATIENT CLASS
class Patient:
    def __init__(self, isPlanned, hoursToGo, specialism):
        self.isPlanned = isPlanned
        self.hoursToGo = hoursToGo
        self.specialism = specialism

    def hours_has_passed(self, hours):
        self.hoursToGo -= hours

    def should_be_discharged(self):
        return (self.hoursToGo < 0)

    def print_self(self):
        print('patient is planned ' + str(self.isPlanned))
        print('patient stay length ' + str(self.hoursToGo) + " hours")
        print('patient specialism ' + str(self.specialism))
 

#PATIENT FACTORY METHOD
def new_patient():

    #Get if is planned
    isPlanned = rand_is_planned()
    
    #Get stay length
    hoursToGo = new_prodecure_length()

    #Get specialism
    specialism = new_specialism(isPlanned)

    #Create patient
    patient = Patient(isPlanned, hoursToGo, specialism)

    #Return patient
    return patient;
