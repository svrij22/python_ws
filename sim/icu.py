import typing

import patient
from patient import Patient
from patient import ScheduledPatient
from settings import Settings


class IcuBed:
    def __init__(self):
        """
        Initialize an ICU bed object with empty patient and occupied status set to False
        """
        self.patient: Patient = {}
        self.occupied: bool = False

    def is_occupied(self) -> bool:
        """
        Check if the bed is currently occupied
        :return: bool
        """
        return self.occupied

    def get_patient(self) -> Patient:
        """
        Get the patient assigned to the bed
        :raises: Exception if the bed is empty
        :return: dict
        """
        if not self.occupied:
            raise Exception("Bed is empty")
        return self.patient

    def clear(self):
        """
        Clear the patient and set occupied status to False
        """
        self.patient = {}
        self.occupied = False

    def set_patient(self, patient: dict):
        """
        Set patient to the bed
        :raises: Exception if the bed is already occupied
        :param patient: dict
        """
        if self.occupied:
            raise Exception("Bed is occupied")

        self.patient = patient
        self.occupied = True

    def print_self(self):
        """
        Print the occupied status of the bed
        """
        print('icu bed is is occupied ' + str(self.occupied))


class IcuDepartment:

    def __init__(self, settings):
        """
        Initialize an ICU department object with empty schedules stack, settings, beds, specialism distribution and statistics
        """
        # INIT Reschedules
        self.schedules_stack = patient.new_patient_schedule_stack()

        # INIT settings
        self.settings = settings

        # INIT BEDS
        self.ICUBeds: typing.List[IcuBed] = []
        for x in range(self.settings.amount_of_icu_beds):
            self.ICUBeds.append(IcuBed())

        self.department_distribution = self.settings.department_distribution

        # INIT STATS
        self.stat_total_waiting_time: int = 0  # hours
        self.stat_patients_RESCHEDULED: int = 0
        self.stat_patients_DENIED: int = 0
        self.stat_covid_DENIED: int = 0
        self.stat_patients_ADMISSIONED: int = 0
        self.stat_failed_RESCHEDULES: int = 0
        self.stat_succesful_RESCHEDULES: int = 0
        self.stat_total_bed_occupation: int = 0
        self.stat_planned: int = len(self.schedules_stack)

    def has_space(self, department) -> bool:
        """
        Check if the ICU department has any available beds
        :return: bool
        """
        count = 0
        for bed in self.ICUBeds:
            if bed.is_occupied() and bed.patient.department() == department:
                count += 1

        if count >= self.department_distribution[department]:
            return False
        else:
            if self.department_distribution[department] == 'COVID':
                print(count)
            return True

    def perc_avail(self) -> float:
        """
        Get the percentage of available beds
        :return: float
        """
        avail = [x for x in self.ICUBeds if not x.is_occupied()]
        return avail.count() / self.settings.amount_of_icu_beds

    def occupied_num(self) -> int:
        """
        Get the number of available beds
        """
        return len([bed for bed in self.ICUBeds if bed.is_occupied()])

    #
    # State and hours passed
    #
    #

    def hours_has_passed(self):
        """
        Subtract hours from patients and remove them from beds if they should be discharged
        """
        # for each bed -> is occup -> get patient -> subtract
        for bed in self.ICUBeds:
            if bed.is_occupied():

                # get patient and subtract
                patient = bed.get_patient()
                patient.hours_has_passed(self.settings.step_size_hour)

                # add total bed occupation
                self.stat_total_bed_occupation += self.settings.step_size_hour

                # disc if needed
                if patient.should_be_discharged():
                    bed.clear()

    # print the icu dept. state
    def describe_state(self):

        # for each bed print
        for index, bed in enumerate(self.ICUBeds):
            print('bed ' + str(index + 1))
            if bed.is_occupied():
                bed.get_patient().print_self()
            else:
                print('empty')

    # describe a short state
    def describe_state_short(self):
        occup = [x for x in self.ICUBeds if x.is_occupied()]
        print("{} of {} beds occupied".format(str(len(occup)), str(self.settings.amount_of_icu_beds)))
        rescheduled = [x for x in self.schedules_stack if x.has_been_rescheduled]
        print("{} scheduled. {} reschuled.".format(str(len(self.schedules_stack)), str(len(rescheduled))))

    #
    # ADDING PATIENTS
    #
    #

    # add patient
    def add_patient(self, patient):

        # Sanity' has space
        if not self.has_space(patient.department()):
            raise Exception(f'No space available at: {patient.department()}')

        # Add patient
        for bed in self.ICUBeds:
            if not bed.is_occupied():
                bed.set_patient(patient)
                return

    def try_adm_patient(self, patient: Patient):
        # Has space?
        if self.has_space(patient.department()):

            # add patient
            self.add_patient(patient)
            self.stat_patients_ADMISSIONED += 1
            return True
        else:

            if patient.department() == 'COVID':
                self.stat_covid_DENIED += 1
                return False
            # denied
            if not patient.isPlanned:
                self.stat_patients_DENIED += 1
            return False

    # reschedule patient
    def reschedule_patient(self, patient):
        self.schedules_stack.append(ScheduledPatient(patient, self.settings.hours_between_reschedule))
        self.stat_patients_RESCHEDULED += 1

    #
    # SCHEDULING
    #
    #
    # work reschedule stack
    def work_schedule(self):

        # Work reschedule stack
        for sched in self.schedules_stack:

            # add to total waiting time
            if sched.has_been_rescheduled:
                self.stat_total_waiting_time += self.settings.step_size_hour
                sched.patient_waiting_time += self.settings.step_size_hour

            # subtract hours
            sched.hours_has_passed(self.settings.step_size_hour)

            # if schedule hours to go is lower than 0
            if sched.hoursToGo <= 0:

                # check if should be rescheduled
                if sched.should_be_executed():
                    # add attempts and try
                    self.try_execute_schedule(sched)

        # Remove patients that have been replanned
        self.schedules_stack = [x for x in self.schedules_stack if not x.should_be_removed()]

    # attempt to reschedule
    def try_execute_schedule(self, scheduled_p):

        # try add patient
        is_succesful = self.try_adm_patient(scheduled_p.patient)
        if is_succesful:

            # remove and add var
            scheduled_p.remove_me = True

            # if is rescheduled
            if scheduled_p.has_been_rescheduled:
                self.stat_succesful_RESCHEDULES += 1

            # ===============DEBUG==================
            if self.settings.display_debug_msgs:
                print('Scheduled patient admissioned')

        else:

            # reschedule
            scheduled_p.reschedule(self.settings.hours_between_reschedule)

            # BUT if max attempts reached, remove it
            if scheduled_p.attempts == self.settings.max_allowed_reschedule_attempts:

                # remove and add var
                scheduled_p.remove_me = True
                self.stat_failed_RESCHEDULES += 1
                self.stat_patients_DENIED += 1

                # ===============DEBUG==================
                if self.settings.display_debug_msgs:
                    print('Scheduled patient reached max admission attempts')

            else:
                self.stat_patients_RESCHEDULED += 1
