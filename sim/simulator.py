import patient
from icu import IcuDepartment
from settings import Settings

#Create ICU
settings = Settings()
sICU = IcuDepartment()

#Define the current hour of the simulation
current_HOUR = 0

#Define the interval between current and the next patient
interval_NEXT_PATIENT_stack = patient.new_patient_interval()

#Define the step() method
def step():

    global current_HOUR, interval_NEXT_PATIENT_stack

    #TIME LOGIC
    current_HOUR += settings.step_size_hour;
    interval_NEXT_PATIENT_stack -= settings.step_size_hour;

    #subtract hours from IcuDept
    sICU.hours_has_passed()

    #ICU do rescheduling
    sICU.work_reschedule_stack()

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
        sICU.try_adm_patient(nPatient, True)


#Define sim vars
vRUN_FOR_DAYS = 365 * 2;
vIS_STEPS = int((vRUN_FOR_DAYS * 24) / settings.step_size_hour)

#run
def run():

    #all steps
    for x in range(vIS_STEPS):
        
        #run step
        step()

        #desc state short
        sICU.describe_state_short()


def stats():
    print("patients denied: " +         str(sICU.stat_patients_DENIED))
    print("patients adm: " +            str(sICU.stat_patients_ADMISSIONED))
    print("patients rescheduled: " +    str(sICU.stat_patients_RESCHEDULED))
    
    print("total_waiting_time: " +      str(sICU.stat_total_waiting_time) + " hours")
    
    print("failed reschedules: " +      str(sICU.stat_failed_RESCHEDULES))
    print("succesful reschedules: " +   str(sICU.stat_succesful_RESCHEDULES))

run()
stats()