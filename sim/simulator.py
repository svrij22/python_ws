import patient
from animate import LineAnimator, MatrixAnimator, VoxelAnimator, BaseAnimator, BarAnimator
from icu import IcuDepartment
from settings import Settings

# patient intervals
interval_NEXT_PATIENT_stack = 0
interval_NEXT_COVID_PATIENT_stack = 0

# Define the current hour of the simulation
# simulation stats
current_HOUR = 0
stat_unplanned = 0
stat_COVID = 0


# Define the step() method
def step(sICU: IcuDepartment):
    global current_HOUR, interval_NEXT_PATIENT_stack, interval_NEXT_COVID_PATIENT_stack, stat_unplanned, stat_COVID

    # TIME LOGIC
    current_HOUR += sICU.settings.step_size_hour
    interval_NEXT_PATIENT_stack -= sICU.settings.step_size_hour
    interval_NEXT_COVID_PATIENT_stack -= sICU.settings.step_size_hour

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
        if sICU.settings.display_debug_msgs:
            print('next patient : {} hours'.format(str(new_patient_interval)))

        # Create patient
        nPatient = patient.new_patient(False, None)

        # try add patient
        sICU.try_adm_patient(nPatient)

    while interval_NEXT_COVID_PATIENT_stack <= 0:

        # Set new interval
        new_patient_interval = patient.new_COVID_patient_interval(sICU.settings.EXPO_VARIABLE_COVID)
        interval_NEXT_COVID_PATIENT_stack += new_patient_interval

        # +1 Covid patient
        stat_COVID += 1

        # ===============DEBUG==================
        if sICU.settings.display_debug_msgs:
            print('next patient : {} hours'.format(str(new_patient_interval)))

        # Create patient
        nPatient = patient.new_COVID_patient()

        # try add patient
        sICU.try_adm_patient(nPatient)


# run
def run(settings: Settings):
    global interval_NEXT_PATIENT_stack, interval_NEXT_COVID_PATIENT_stack, current_HOUR, stat_unplanned, stat_COVID

    # set amount of steps
    vIS_STEPS = int((settings.simulator_days * 24) / settings.step_size_hour)
    # Create ICU
    sICU = IcuDepartment(settings)

    # Define the interval between current and the next patient
    interval_NEXT_PATIENT_stack = patient.new_patient_interval(False, None)
    interval_NEXT_COVID_PATIENT_stack = patient.new_COVID_patient_interval(settings.EXPO_VARIABLE_COVID)

    # if animator
    if settings.animator_enabled:
        BaseAnimator.setup(2, 2, (10, 8))

        current_occupancy_animator: LineAnimator = LineAnimator(0, 0, vIS_STEPS)
        occupancy_by_specialism_animator: MatrixAnimator = MatrixAnimator(1, 0, (10, 10))
        occupancy_by_time_spent: VoxelAnimator = VoxelAnimator(0, 1, 6, 20, 120)
        n_patients_rescheduled: BarAnimator = BarAnimator(1, 1)

    # all steps
    for step_var in range(vIS_STEPS):

        # run step
        step(sICU)

        if settings.animator_enabled and step_var % settings.plot_graph_interval == 0:
            current_occupancy_animator.plot(step_var, sICU.occupied_num())
            occupancy_by_specialism_animator.plot(sICU.ICUBeds)
            occupancy_by_time_spent.plot(sICU.ICUBeds)
            n_patients_rescheduled.plot(sICU.schedules_stack)


        # state msgs
        if settings.display_debug_msgs:
            # desc state short
            sICU.describe_state_short()

    return sICU


def stats(sICU):
    print("patients denied: " + str(sICU.stat_patients_DENIED))
    print("covid patients denied: " + str(sICU.stat_covid_DENIED))
    print("patients adm: " + str(sICU.stat_patients_ADMISSIONED))
    print("patients rescheduled: " + str(sICU.stat_patients_RESCHEDULED))

    print("total waiting time: " + str(sICU.stat_total_waiting_time) + " hours")
    print("total bed occupation: " + str(sICU.stat_total_bed_occupation) + " hours")

    print("failed reschedules: " + str(sICU.stat_failed_RESCHEDULES))
    print("succesful reschedules: " + str(sICU.stat_succesful_RESCHEDULES))

    print("patients (planned): " + str(sICU.stat_planned))
    print("patients (COVID): " + str(stat_COVID))
    print("patients (unplanned): " + str(stat_unplanned))


#stats(run(Settings()))

#input("Press enter to exit.")

