import math
import random

import numpy as np


# Create settings const
from settings import Settings

default_settings = Settings()

# INTERVAL unplanned
EXPO_VARIABLE_UNPLANNED = 6.402049279835394  # mean of delta time data
EXPO_VARIABLE_UNPLANNED_W_DENIED = 5.9849999051952985  # mean of delta time data with unplanned and denied patients

# INTERVAL planned by weekday
EXPO_VARIABLE_PLANNED = {'Monday': 7.149544444444361,
                         'Tuesday': 8.849943094135723,
                         'Wednesday': 10.240050154321109,
                         'Thursday': 7.494862298195766,
                         'Friday': 12.161566901408305,
                         'Saturday': 28.055376344085566,
                         'Sunday': 19.7370454545469488}  # means of delta time data by weekday


def new_patient_interval(isPlanned, weekday):
    if isPlanned:
        return np.random.exponential(EXPO_VARIABLE_PLANNED[weekday])
    else:
        return np.random.exponential(EXPO_VARIABLE_UNPLANNED_W_DENIED)


def new_COVID_patient_interval(EXPO_VARIABLE_COVID):
    return np.random.exponential(EXPO_VARIABLE_COVID)


# Time on ICU
# Return value in HOURS
SPECIALISM_MU_SIGMA = {'CAPU': [3.115982878864364, 1.060593768052976],
                       'CHIR': [3.6608192784174287, 1.3846954607518251],
                       'CARD': [3.8800439044710857, 1.2214170976049434],
                       'INT': [3.6670020007750534, 1.4417975989081482],
                       'NEC': [1.2260060537089816, 3.8992934240491044],
                       'NEU': [3.5704887322586423, 1.4195116678759554],
                       'OTHER': [3.3772253052032912, 1.2894040353499023]}


def new_prodecure_length(specialism):
    return np.random.lognormal(SPECIALISM_MU_SIGMA[specialism][0], SPECIALISM_MU_SIGMA[specialism][1])


COVID_MU_SIGMA = [8]


def new_prodecure_COVID_length():
    return np.random.exponential(COVID_MU_SIGMA)


# Planned patient illness distribution by weekday
EXPO_VARIABLE_PLANNED_ILLNESS = {
    'Monday': {'CAPU': 281, 'CHIR': 28, 'CARD': 0, 'INT': 2, 'NEC': 11, 'NEU': 3, 'OTHER': 0},
    'Tuesday': {'CAPU': 240, 'CHIR': 41, 'CARD': 0, 'INT': 4, 'NEC': 2, 'NEU': 1, 'OTHER': 0},
    'Wednesday': {'CAPU': 186, 'CHIR': 11, 'CARD': 1, 'INT': 4, 'NEC': 12, 'NEU': 1, 'OTHER': 1},
    'Thursday': {'CAPU': 327, 'CHIR': 19, 'CARD': 0, 'INT': 0, 'NEC': 4, 'NEU': 1, 'OTHER': 0},
    'Friday': {'CAPU': 252, 'CHIR': 14, 'CARD': 2, 'INT': 3, 'NEC': 12, 'NEU': 1, 'OTHER': 0},
    'Saturday': {'CAPU': 18, 'CHIR': 4, 'CARD': 1, 'INT': 4, 'NEC': 3, 'NEU': 1, 'OTHER': 0},
    'Sunday': {'CAPU': 11, 'CHIR': 3, 'CARD': 2, 'INT': 2, 'NEC': 3, 'NEU': 1, 'OTHER': 0}}


# Generate specialism
def new_specialism(isPlanned, weekday):
    if isPlanned:
        distribution = EXPO_VARIABLE_PLANNED_ILLNESS[weekday]
        return random.choices(list(distribution.keys()), weights=tuple(distribution.values()))[0]
    else:
        return random.choices(['CAPU', 'CHIR', 'NEC', 'INT', 'NEU', 'CARD', 'OTHER'],
                              weights=(997, 448, 426, 317, 309, 150, 53))[0]


# RANDOM
PATIENT_AMOUNT = 4399
PATIENT_IS_PLANNED_AMOUNT = 1499


# Define patients to reschedule
class ScheduledPatient:

    def __init__(self, patient, hours):
        # Patient
        self.patient = patient

        # Waiting time
        self.hoursToGo = hours

        # Is rescheduled
        self.has_been_rescheduled = False
        self.patient_waiting_time = 0

        # Rescheduling
        self.attempts = 0
        self.remove_me = False

    def reschedule(self, when):
        if self.hoursToGo > 0:
            raise Exception("Schedule has not passed execution point yet")
        self.attempts += 1
        self.has_been_rescheduled = True
        self.hoursToGo = when

    def hours_has_passed(self, hours):
        self.hoursToGo -= hours

    def should_be_executed(self):
        return self.hoursToGo <= 0

    def should_be_removed(self):
        return self.remove_me


# PATIENT CLASS
class Patient:
    def __init__(self, isPlanned, hoursToGo, specialism):
        self.isPlanned = isPlanned

        self.origHoursToGo = hoursToGo
        self.hoursToGo = hoursToGo
        self.specialism = specialism

    def get_specialism(self):
        return self.specialism

    def hours_has_passed(self, hours):
        self.hoursToGo -= hours

    def hours_on_icu(self):
        return self.origHoursToGo - self.hoursToGo

    def should_be_discharged(self):
        return self.hoursToGo < 0

    def department(self):
        for dep in default_settings.department_distribution.keys():
            if self.specialism in dep:
                return dep

    def print_self(self):
        print('patient is planned ' + str(self.isPlanned))
        print('patient stay length ' + str(self.hoursToGo) + " hours")
        print('patient specialism ' + str(self.specialism))


# generates a list of scheduled patients
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def new_patient_schedule_stack():
    # calc hours
    total_hours_togo = default_settings.simulator_days * 24
    current_hour = 0

    # define list
    patient_stack = []
    while total_hours_togo >= 0:
        # determine weekday
        n_days = math.floor(current_hour / 24)
        weekday = weekdays[n_days % 7]

        # ff time
        hour_delta = new_patient_interval(True, weekday)
        current_hour += hour_delta
        total_hours_togo -= hour_delta

        # create schedule
        patient = new_patient(True, weekday)
        scheduled = ScheduledPatient(patient, current_hour)
        patient_stack.append(scheduled)

    # return stack
    return patient_stack


def new_patient_schedule_stack_new():
    # define list
    patient_stack = []

    # for each day
    for day in weekdays:

        # calc hours
        day_hours_togo = default_settings.simulator_days * 24 / 7
        current_hour = 0

        while day_hours_togo >= 0:
            # ff time
            hour_delta = new_patient_interval(True, day)
            current_hour += hour_delta
            day_hours_togo -= hour_delta

            # create schedule
            patient = new_patient(True, day)
            scheduled = ScheduledPatient(patient, current_hour)
            patient_stack.append(scheduled)

    #

    # return stack
    return patient_stack


# PATIENT FACTORY METHOD
def new_patient(isPlanned, weekday) -> Patient:
    # Get specialism
    specialism = new_specialism(isPlanned, weekday)

    # Get stay length
    hoursToGo = new_prodecure_length(specialism)

    # Create patient
    patient = Patient(isPlanned, hoursToGo, specialism)

    # Return patient
    return patient


# COVID PATIENT FACTORY METHOD
def new_COVID_patient():
    # Set specialism
    specialism = 'COVID'

    # Get stay length
    hoursToGo = new_prodecure_COVID_length()

    # Create patient
    patient = Patient(False, hoursToGo, specialism)

    # Return patient
    return patient
