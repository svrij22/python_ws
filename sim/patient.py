
import numpy as np
import random
from settings import Settings

#Create settings const
SETTINGS = Settings()

#INTERVAL
EXPO_VARIABLE_UNPLANNED = 6.402049279835394 # mean of delta time data
EXPO_VARIABLE_PLANNED = 11.659628456007704 # mean of delta time data
def new_patient_interval(isPlanned):
    if (isPlanned):
        return np.random.exponential(EXPO_VARIABLE_PLANNED)
    else:
        return np.random.exponential(EXPO_VARIABLE_UNPLANNED)

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
class ScheduledPatient:

    def __init__(self, patient, hours):

        #Patient
        self.patient = patient
        
        #Waiting time
        self.hoursToGo = hours
        
        #Is rescheduled
        self.has_been_rescheduled = False

        #Rescheduling
        self.attempts = 0
        self.remove_me = False

    def reschedule(self, when):
        self.attempts += 1
        self.has_been_rescheduled = True
        self.hoursToGo = when
        
    def hours_has_passed(self, hours):
        self.hoursToGo -= hours

    def should_be_executed(self):
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

#generates a list of scheduled patients
def new_patient_schedule_stack():

    #calc hours
    total_hours_togo = SETTINGS.simulator_days * 24
    current_hour = 0

    #define list
    patient_stack = []
    while(total_hours_togo >= 0):
        
        #ff time
        hour_delta = new_patient_interval(True)
        current_hour += hour_delta
        total_hours_togo -= hour_delta

        #create schedule
        patient = new_patient(True)
        scheduled = ScheduledPatient(patient, current_hour)
        patient_stack.append(scheduled)
    
    #return stack
    return patient_stack

#PATIENT FACTORY METHOD
def new_patient(isPlanned):
    
    #Get stay length
    hoursToGo = new_prodecure_length()

    #Get specialism
    specialism = new_specialism(isPlanned)

    #Create patient
    patient = Patient(isPlanned, hoursToGo, specialism)

    #Return patient
    return patient;
