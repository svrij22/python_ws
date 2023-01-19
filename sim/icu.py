from patient import ScheduledPatient
from settings import Settings
import patient

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
        self.schedules_stack = patient.new_patient_schedule_stack()

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
        self.stat_total_bed_occupation = 0
        self.stat_planned = len(self.schedules_stack)

    #Check if has space
    def has_space(self):
        for x in self.ICUBeds:
            if not (x.is_occupied()):
                return True
        return False

    # return percentage available
    def perc_avail(self):
        avail = [x for x in self.ICUBeds if not x.is_occupied()]
        return avail.count() / self.settings.amount_of_icu_beds


#
# State and hours passed
#
#

    #subtract hours from patients and remove from beds
    def hours_has_passed(self):

        # for each bed -> is occup -> get patient -> subtract
        for bed in self.ICUBeds:
            if (bed.is_occupied()):

                #get patient and subtract
                patient = bed.get_patient()
                patient.hours_has_passed(self.settings.step_size_hour)

                #add total bed occupation
                self.stat_total_bed_occupation += self.settings.step_size_hour

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
        rescheduled = [x for x in self.schedules_stack if x.has_been_rescheduled]
        print("{} scheduled. {} reschuled.".format(str(len(self.schedules_stack)), str(len(rescheduled))))

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
        self.schedules_stack.append(ScheduledPatient(patient, self.settings.hours_between_reschedule))
        self.stat_patients_RESCHEDULED += 1;

#
# SCHEDULING
#
#
    #work reschedule stack
    def work_schedule(self):
        
        #Work reschedule stack
        for sched in self.schedules_stack:

            #add to total waiting time
            if (sched.has_been_rescheduled):
                self.stat_total_waiting_time += sched.hoursToGo

            #subtract hours
            sched.hours_has_passed(self.settings.step_size_hour)

            #if schedule hours to go is lower than 0
            if (sched.hoursToGo < 0):

                #check if should be rescheduled
                if (sched.should_be_executed()):                         

                    #add attempts and try
                    self.try_execute_schedule(sched)

        #Remove patients that have been replanned
        self.schedules_stack = [x for x in self.schedules_stack if not x.should_be_removed()]

    #attempt to reschedule
    def try_execute_schedule(self, scheduled_p):

        #try add patient
        is_succesful = self.try_adm_patient(scheduled_p.patient, False)  
        if (is_succesful):

            #remove and add var
            scheduled_p.remove_me = True;

            #if is rescheduled
            if (scheduled_p.has_been_rescheduled):
                self.stat_succesful_RESCHEDULES += 1;

            #===============DEBUG==================
            if (self.settings.display_debug_msgs):
                print('Scheduled patient admissioned')

        else:

            #max attempts reached
            if (scheduled_p.attempts > self.settings.max_allowed_reschedule_attempts):
                
                #remove and add var
                scheduled_p.remove_me = True
                self.stat_failed_RESCHEDULES += 1;
                self.stat_patients_DENIED += 1;
                
                #===============DEBUG==================
                if (self.settings.display_debug_msgs):
                    print('Scheduled patient reached max admission attempts')

            else:
                
                scheduled_p.reschedule(self.settings.hours_between_reschedule)
                    

