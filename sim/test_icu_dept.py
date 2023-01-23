import unittest
import patient
import numpy
import scipy
from patient import ScheduledPatient
from icu import IcuDepartment

class DataTests(unittest.TestCase):

    def getScheduledPatient(self) -> ScheduledPatient:

        #create patient
        nPatient = patient.new_patient(True);

        #create schedule
        return ScheduledPatient(nPatient, 60);

    def test_dept_schedule_should_be_executed(self):

        #create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 60;

        #create
        sched = self.getScheduledPatient();
        
        #append to icu
        dept.schedules_stack.append(sched)
        
        #pass time
        dept.work_schedule()

        #assert true
        self.assertEqual(sched.should_be_executed(), True)
        

    def test_dept_is_full(self):

        #create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 60;

        #fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True))

        #is full
        self.assertTrue(not dept.has_space())
        
    def test_dept_is_full_all_beds_occupied(self):

        #create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 60;

        #fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True))

        #get filled beds
        filled_beds = [x for x in dept.ICUBeds if x.is_occupied()]

        #is full
        self.assertTrue(len(filled_beds) == dept.settings.amount_of_icu_beds)
        
    def test_dept_pass_time(self):

        #create dept
        dept = IcuDepartment()
        dept.settings.step_size_hour = 100;

        #fill dept
        for x in range(dept.settings.amount_of_icu_beds):
            dept.add_patient(patient.new_patient(True))

        #pass hours
        dept.hours_has_passed();

        #is full
        self.assertTrue(dept.has_space())


if __name__ == '__main__':
    unittest.main(verbosity=2)