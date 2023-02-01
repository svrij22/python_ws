import matplotlib.pyplot as plt

import patient
from animate import LineAnimator, MatrixAnimator, VoxelAnimator, BaseAnimator, BarAnimator
from icu import IcuDepartment
from settings import Settings

# Create ICU
settings = Settings()
sICU = IcuDepartment({'CARD/INT/OTHER': 7, 'NEU/NEC': 8, 'CAPU': 8, 'CHIR': 4})

if sICU.department_distribution['COVID'] < 0:
    raise Exception(f"department distribution has to many beds: {sICU.department_distribution['COVID']*-1}")

# Define the current hour of the simulation
current_HOUR = 0
stat_unplanned = 0
stat_COVID = 0

# Define the interval between current and the next patient
interval_NEXT_PATIENT_stack = patient.new_patient_interval(False, None)
interval_NEXT_COVID_PATIENT_stack = patient.new_COVID_patient_interval()


# Define the step() method
def step():
    global current_HOUR, interval_NEXT_PATIENT_stack, interval_NEXT_COVID_PATIENT_stack, stat_unplanned, stat_COVID

    # TIME LOGIC
    current_HOUR += settings.step_size_hour
    interval_NEXT_PATIENT_stack -= settings.step_size_hour
    interval_NEXT_COVID_PATIENT_stack -= settings.step_size_hour

    # subtract hours from IcuDept
    sICU.hours_has_passed()

    # ICU do rescheduling
    sICU.work_schedule()

    # Patient spawning logic
    while interval_NEXT_PATIENT_stack <= 0:

        # Set new interval
        new_patient_interval = patient.new_patient_interval(False, None)
        interval_NEXT_PATIENT_stack += new_patient_interval

        # add unplanned
        stat_unplanned += 1

        # ===============DEBUG==================
        if settings.display_debug_msgs:
            print('next patient : {} hours'.format(str(new_patient_interval)))

        # Create patient
        nPatient = patient.new_patient(False, None)

        # try add patient
        sICU.try_adm_patient(nPatient)

    while interval_NEXT_COVID_PATIENT_stack <= 0:

        # Set new interval
        new_patient_interval = patient.new_COVID_patient_interval()
        interval_NEXT_COVID_PATIENT_stack += new_patient_interval

        # add unplanned
        stat_COVID += 1

        # ===============DEBUG==================
        if settings.display_debug_msgs:
            print('next patient : {} hours'.format(str(new_patient_interval)))

        # Create patient
        nPatient = patient.new_COVID_patient()

        # try add patient
        sICU.try_adm_patient(nPatient)


# Define sim vars
vIS_STEPS = int((settings.simulator_days * 24) / settings.step_size_hour)


# run
def run():

    # if animator
    if settings.animator_enabled:
        BaseAnimator.setup(2, 2, (10, 8))

    # all steps
    for step_var in range(vIS_STEPS):

        current_occupancy_animator: LineAnimator = LineAnimator(0, 0, vIS_STEPS)
        occupancy_by_specialism_animator: MatrixAnimator = MatrixAnimator(1, 0, (10, 10))
        occupancy_by_time_spent: VoxelAnimator = VoxelAnimator(0, 1, 6, 20, 120)
        n_patients_rescheduled: BarAnimator = BarAnimator(1, 1)
        # run step
        step()

        if settings.animator_enabled and step_var % settings.plot_graph_interval == 0:
            current_occupancy_animator.plot(step_var, sICU.occupied_num())
            occupancy_by_specialism_animator.plot(sICU.ICUBeds)
            occupancy_by_time_spent.plot(sICU.ICUBeds)
            n_patients_rescheduled.plot(sICU.schedules_stack)
            # animator.plot_rescheduled(sICU.schedules_stack)

        # ===============DEBUG==================
        # state msgs
        if (settings.display_debug_msgs):
            # desc state short
            sICU.describe_state_short()


def stats():
    print("patients denied: " + str(sICU.stat_patients_DENIED))
    print("patients adm: " + str(sICU.stat_patients_ADMISSIONED))
    print("patients rescheduled: " + str(sICU.stat_patients_RESCHEDULED))

    print("total waiting time: " + str(sICU.stat_total_waiting_time) + " hours")
    print("total bed occupation: " + str(sICU.stat_total_bed_occupation) + " hours")

    print("failed reschedules: " + str(sICU.stat_failed_RESCHEDULES))
    print("succesful reschedules: " + str(sICU.stat_succesful_RESCHEDULES))

    print("patients (planned): " + str(sICU.stat_planned))
    print("patients (unplanned): " + str(stat_unplanned))


run()
stats()

input("Press enter to exit.")
