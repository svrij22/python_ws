import unittest

import patient
from icu import IcuDepartment
from patient import ScheduledPatient


class DataTests(unittest.TestCase):

    def getScheduledPatient(self) -> ScheduledPatient:

        # create patient
        nPatient = patient.new_patient(True, 'Monday')

        # create schedule
        return ScheduledPatient(nPatient, 60)

    def test_dept_schedule_should_be_executed(self):

        # create dept
        dept = IcuDepartment()
        dept.schedules_stack = []
        dept.settings.step_size_hour = 60

        # create
        sched = self.getScheduledPatient()

        # append to icu
        dept.schedules_stack.append(sched)

        # pass time
        dept.work_schedule()

        # assert true
        self.assertEqual(sched.should_be_executed(), True)

    def test_dept_is_full(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 60

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # is full
        self.assertTrue(not dept.has_space())

    def test_dept_is_full_all_beds_occupied(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 60

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # get filled beds
        filled_beds = [x for x in dept.ICUBeds if x.is_occupied()]

        # is full
        self.assertTrue(len(filled_beds) == dept.settings.amount_of_icu_beds)

    def test_dept_pass_time(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 100

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # pass hours
        dept.hours_has_passed()

        # is full
        self.assertTrue(dept.has_space())

    def test_dept_created_beds(self):

        # create dept
        dept = IcuDepartment()

        # is amount_of_icu_beds
        self.assertTrue(len(dept.ICUBeds) == dept.settings.amount_of_icu_beds)

    def getReScheduledPatient(self) -> ScheduledPatient:

        # create patient
        nPatient = patient.new_patient(True, 'Monday')

        # create schedule
        reSched = ScheduledPatient(nPatient, 1000)
        reSched.has_been_rescheduled = True

        return reSched

    # this test actually made me realize i made a mistake

    def test_STAT_total_waiting_time(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 100

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # fill schedule
        dept.schedules_stack = [self.getReScheduledPatient() for x in range(5)]

        # work schedule
        dept.work_schedule()

        # assert equals
        self.assertEqual(dept.stat_total_waiting_time, 5 * 100)

    def test_STAT_patients_RESCHEDULED_zero(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 100

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # fill schedule
        dept.schedules_stack = [self.getReScheduledPatient() for x in range(5)]

        # work schedule
        dept.work_schedule()

        # assert equals
        self.assertEqual(dept.stat_patients_RESCHEDULED, 0)

    def test_STAT_patients_RESCHEDULED_all(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 1000

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # fill schedule
        dept.schedules_stack = [self.getReScheduledPatient() for x in range(5)]

        # work schedule
        dept.work_schedule()

        # assert equals
        self.assertEqual(dept.stat_patients_RESCHEDULED, 5)

    # same here

    def test_STAT_patients_max_allowed_reschedule_attempts(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 1000

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True, 'Monday'))

        # fill schedule
        dept.schedules_stack = [self.getReScheduledPatient() for x in range(5)]

        # work schedule
        for x in range(dept.settings.max_allowed_reschedule_attempts):
            dept.work_schedule()

        # assert equals
        self.assertEqual(len(dept.schedules_stack), 0)
        self.assertEqual(dept.stat_failed_RESCHEDULES, 5)
        self.assertEqual(dept.stat_succesful_RESCHEDULES, 0)

    def test_STAT_patients_admissioned(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 1000

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.try_adm_patient(patient.new_patient(True, 'Monday'))

        # assert equals
        self.assertEqual(dept.stat_patients_ADMISSIONED, dept.settings.amount_of_icu_beds)

    def test_STAT_patients_admissioned_EXCEPTION_add(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 1000

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.try_adm_patient(patient.new_patient(True, 'Monday'))

        # assert equals
        self.assertEqual(dept.stat_patients_ADMISSIONED, dept.settings.amount_of_icu_beds)

        # assert exception
        with self.assertRaises(Exception):
            dept.add_patient(patient.new_patient(True, 'Monday'))

    def test_STAT_patients_DENIED(self):

        # create dept
        dept = IcuDepartment()

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.try_adm_patient(patient.new_patient(True, 'Monday'))

        # add 50 non planned patients
        for x in range(50):
            dept.try_adm_patient(patient.new_patient(False, 'Monday'))

        # assert equals
        self.assertEqual(dept.stat_patients_DENIED, 50)

    def test_STAT_total_bed_occup(self):

        # create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 1

        # fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.try_adm_patient(patient.new_patient(True, 'Monday'))

        # pass hours
        hours_passed = 0
        while (dept.occupied_num() > 0):
            hours_passed += dept.occupied_num() * dept.settings.step_size_hour
            dept.hours_has_passed()

        # assert equals
        self.assertEqual(dept.stat_total_bed_occupation, hours_passed)


if __name__ == '__main__':
    unittest.main(verbosity=2)
