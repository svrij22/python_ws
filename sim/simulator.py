import patient
from animate import Animator
from icu import IcuDepartment
from settings import Settings
import os
import matplotlib.pyplot as plt

#Create ICU
settings = Settings()
sICU = IcuDepartment()

#Define the current hour of the simulation
current_HOUR = 0
stat_unplanned = 0

#Define the interval between current and the next patient
interval_NEXT_PATIENT_stack = patient.new_patient_interval(False, None)

#Define the step() method
def step():

    global current_HOUR, interval_NEXT_PATIENT_stack, stat_unplanned

    #TIME LOGIC
    current_HOUR += settings.step_size_hour;
    interval_NEXT_PATIENT_stack -= settings.step_size_hour;

    #subtract hours from IcuDept
    sICU.hours_has_passed()

    #ICU do rescheduling
    sICU.work_schedule()

    #Patient spawning logic
    while(interval_NEXT_PATIENT_stack <= 0):
        
        
        #Set new interval
        new_patient_interval = patient.new_patient_interval(False, None)
        interval_NEXT_PATIENT_stack += new_patient_interval

        #add unplanned
        stat_unplanned += 1

        #===============DEBUG==================
        if (settings.display_debug_msgs):
            print('next patient : {} hours'.format(str(new_patient_interval)))

        #Create patient
        nPatient = patient.new_patient(False, None)

        #try add patient
        sICU.try_adm_patient(nPatient)


#Define sim vars
vIS_STEPS = int((settings.simulator_days * 24) / settings.step_size_hour)

#run
def run():
    if settings.animator_enabled:
        plt.ion()
        fig, ax = plt.subplots(figsize=(10, 8))
        animator = Animator(ax, vIS_STEPS)

    #all steps
    for x in range(vIS_STEPS):
        
        #run step
        step()

        if settings.animator_enabled and x % settings.plot_graph_interval == 0:
            animator.plot(x, sICU.occupied_num())

        #===============DEBUG==================
        #state msgs
        if (settings.display_debug_msgs):
            
            #desc state short
            sICU.describe_state_short()

def stats():
    print("patients denied: " +         str(sICU.stat_patients_DENIED))
    print("patients adm: " +            str(sICU.stat_patients_ADMISSIONED))
    print("patients rescheduled: " +    str(sICU.stat_patients_RESCHEDULED))
    
    print("total waiting time: " +      str(sICU.stat_total_waiting_time) + " hours")
    print("total bed occupation: " +   str(sICU.stat_total_bed_occupation) + " hours")
    
    print("failed reschedules: " +      str(sICU.stat_failed_RESCHEDULES))
    print("succesful reschedules: " +   str(sICU.stat_succesful_RESCHEDULES))
    
    print("patients (planned): " +      str(sICU.stat_planned))
    print("patients (unplanned): " +   str(stat_unplanned))


run()
stats()

input("Press enter to exit.")