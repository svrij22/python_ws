import patient
from icu import IcuDepartment
from patient import Reschedule

#Create ICU
sICU = IcuDepartment()

#Define the current hour of the simulation
current_HOUR = 0

#Define the step size of the simulation
step_SIZE_HOUR = 6

#Define the interval between current and the next patient
interval_NEXT_PATIENT_stack = patient.new_patient_interval()

#Define the patients that are denied
patients_RESCHEDULED = 0
patients_DENIED = 0
patients_ADMISSIONED = 0

#hours and max attempts
hours_TO_RESCHEDULE = 6
max_ALLOWED_RES_ATTEMPTS = 5

#Total waiting time for planned patients, patients to reschedule
total_waiting_time = 0
patients_to_reschedule = []

#failed and succesful reschedules
failed_RESCHEDULES = 0
succesful_RESCHEDULES = 0

#try add patient
def try_add_patient(nPatient, reschedule_if_needed = True):
    global current_HOUR, step_SIZE_HOUR, interval_NEXT_PATIENT_stack, patients_DENIED, patients_ADMISSIONED, patients_to_reschedule, total_waiting_time, hours_TO_RESCHEDULE, max_ALLOWED_RES_ATTEMPTS, failed_RESCHEDULES, succesful_RESCHEDULES, patients_RESCHEDULED

    #Has space?
    if (sICU.has_space()):

        #add patient
        sICU.add_patient(nPatient)
        patients_ADMISSIONED += 1
        
        #DEBUG
        print('Next patient admissioned')
        return True
    else:

        # if its planned add to reschedule stack
        if (reschedule_if_needed):
            if (nPatient.isPlanned):
                patients_to_reschedule.append(Reschedule(nPatient, hours_TO_RESCHEDULE))
                patients_RESCHEDULED += 1;
            else:
                patients_DENIED +=1

        #DEBUG
        print('Patient denied')
        return False

#Define the step() method
def step():
    global current_HOUR, step_SIZE_HOUR, interval_NEXT_PATIENT_stack, patients_DENIED, patients_ADMISSIONED, patients_to_reschedule, total_waiting_time, hours_TO_RESCHEDULE, max_ALLOWED_RES_ATTEMPTS, failed_RESCHEDULES, succesful_RESCHEDULES, patients_RESCHEDULED

    #Add step size to hour
    current_HOUR += step_SIZE_HOUR

    #Time logic
    current_HOUR += step_SIZE_HOUR;
    interval_NEXT_PATIENT_stack -= step_SIZE_HOUR;

    #subtract hours from IcuDept
    sICU.hours_has_passed(step_SIZE_HOUR)

    #
    #
    #Work reschedule stack
    for index, res in enumerate(patients_to_reschedule):

        #add to total waiting time
        total_waiting_time += res.hoursToGo

        #subtract hours
        res.hours_has_passed(step_SIZE_HOUR)

        #check if should be replanned
        if (res.should_be_replanned()):

            #add attempts
            res.attempts += 1;

            #try add patient
            is_succesful = try_add_patient(res.patient, False)
            if (is_succesful):

                #remove and add var
                res.vshould_be_removed = True;
                succesful_RESCHEDULES += 1;
            else:
                #max attempts reached
                if (res.attempts > max_ALLOWED_RES_ATTEMPTS):
                    
                    #remove and add var
                    res.vshould_be_removed = True
                    failed_RESCHEDULES += 1;
                    patients_DENIED += 1;
                
    #Remove patients that have been replanned
    patients_to_reschedule = [x for x in patients_to_reschedule if not x.should_be_removed()]

    #
    #
    #Patient spawning logic
    while(interval_NEXT_PATIENT_stack <= 0):
        
        #Set new interval
        new_patient_interval = patient.new_patient_interval()
        interval_NEXT_PATIENT_stack += new_patient_interval

        #DEBUG
        print('Next patient in {} hours'.format(str(new_patient_interval)))

        #Create patient
        nPatient = patient.new_patient()

        #try add patient
        try_add_patient(nPatient)


#Define sim vars
vRUN_FOR_DAYS = 365;
vIS_STEPS = int((vRUN_FOR_DAYS * 24) / step_SIZE_HOUR)

#run
def run():

    #all steps
    for x in range(vIS_STEPS):
        
        #run step
        step()

        #desc state short
        sICU.describe_state_short()

def stats():
    print("patients denied: " + str(patients_DENIED))
    print("patients adm: " + str(patients_ADMISSIONED))
    print("patients rescheduled: " + str(patients_RESCHEDULED))
    
    print("total_waiting_time: " + str(total_waiting_time) + " hours")
    
    print("failed reschedules: " + str(failed_RESCHEDULES))
    print("succesful reschedules: " + str(succesful_RESCHEDULES))

run()
stats()