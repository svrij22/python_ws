from patient import Reschedule
from settings import Settings

#PATIENT CLASS
class IcuBed:
    def __init__(self):
        self.patient = {}
        self.occupied = False

    #check if is occupied
    def is_occupied(self):
        return self.occupied

    #get patient
    def get_patient(self):
        if not (self.occupied):
            raise Exception("Bed is empty")
        return self.patient

    #clear bed
    def clear(self):
        self.patient = {}
        self.occupied = False
        
    #set patient
    def set_patient(self, patient):
        if (self.occupied):
            raise Exception("Bed is occupied")

        self.patient = patient
        self.occupied = True

    #print self
    def print_self(self):
        print('icu bed is is occupied ' + str(self.occupied))

class IcuDepartment:

    #Init
    def __init__(self):
        
        #INIT Reschedules
        self.reschedules_stack = []

        #INIT settings
        self.settings = Settings()

        #INIT BEDS
        self.ICUBeds = []
        for x in range(self.settings.amount_of_icu_beds):
            self.ICUBeds.append(IcuBed())

        #INIT STATS
        self.stat_total_waiting_time = 0 # hours
        self.stat_patients_RESCHEDULED = 0
        self.stat_patients_DENIED = 0
        self.stat_patients_ADMISSIONED = 0
        self.stat_failed_RESCHEDULES = 0
        self.stat_succesful_RESCHEDULES = 0

    #Check if has space
    def has_space(self):
        for x in self.ICUBeds:
            if not (x.is_occupied()):
                return True
        return False

    # return percentage available
    def perc_avail(self):
        avail = [x for x in self.ICUBeds if not x.is_occupied()]
        return avail.count() / AMOUNT_OF_BEDS


    #subtract hours from patients and remove from beds
    def hours_has_passed(self):

        # for each bed -> is occup -> get patient -> subtract
        for bed in self.ICUBeds:
            if (bed.is_occupied()):

                #get patient and subtract
                patient = bed.get_patient()
                patient.hours_has_passed(self.settings.step_size_hour)

                #disc if needed
                if (patient.should_be_discharged()):
                    bed.clear()


    #print the icu dept. state
    def describe_state(self):

        #for each bed print
        for index, bed  in enumerate(self.ICUBeds):
            print('bed ' + str(index + 1))
            if (bed.is_occupied()):
                bed.get_patient().print_self()
            else:
                print('empty')

    #describe a short state
    def describe_state_short(self):
        occup = [x for x in self.ICUBeds if x.is_occupied()]
        print("{} of {} beds occupied".format(str(len(occup)), str(self.settings.amount_of_icu_beds)))

#
# ADDING PATIENTS
#
#

    #add patient
    def add_patient(self, patient):

        #Sanity' has space
        if not self.has_space():
            raise Exception('No space available')

        #Add patient
        for bed in self.ICUBeds:
            if not (bed.is_occupied()):
                bed.set_patient(patient)
                return;
                
    def try_adm_patient(self, patient, shouldRescheduleIfPlanned):

        #Has space?
        if (self.has_space()):

            #add patient
            self.add_patient(patient)
            self.stat_patients_ADMISSIONED += 1
            return True
        else:

            # if its planned add to reschedule stack
            if (shouldRescheduleIfPlanned and patient.isPlanned):
                self.reschedule_patient(patient)
            else:
                self.stat_patients_DENIED +=1
            return False

    #reschedule patient
    def reschedule_patient(self, patient):
        self.reschedules_stack.append(Reschedule(patient, self.settings.hours_between_reschedule))
        self.stat_patients_RESCHEDULED += 1;

#
# RESCHEDULING
#
#
    #work reschedule stack
    def work_reschedule_stack(self):
        
        #Work reschedule stack
        for res in self.reschedules_stack:

            #add to total waiting time / subtract hours
            self.stat_total_waiting_time += res.hoursToGo           
            res.hours_has_passed(self.settings.step_size_hour)

            #check if should be replanned
            if (res.should_be_replanned()):                         

                #add attempts and try
                res.attempts += 1;
                self.try_reschedule(res)

        #Remove patients that have been replanned
        self.reschedules_stack = [x for x in self.reschedules_stack if not x.should_be_removed()]

    #attempt to reschedule
    def try_reschedule(self, reschedule):

        #try add patient
        is_succesful = self.try_adm_patient(reschedule.patient, False)  
        if (is_succesful):

            #remove and add var
            reschedule.remove_me = True;
            self.stat_succesful_RESCHEDULES += 1;

        else:

            #max attempts reached
            if (reschedule.attempts > self.settings.max_allowed_reschedule_attempts):
                
                #remove and add var
                reschedule.remove_me = True
                self.stat_failed_RESCHEDULES += 1;
                self.stat_patients_DENIED += 1;

            else:

                #re-set clock
                reschedule.hoursToGo = self.settings.hours_between_reschedule
                    

