import unittest
import patient
import numpy
import scipy
from patient import ScheduledPatient
from icu import IcuDepartment

class DataTests(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main(verbosity=2)