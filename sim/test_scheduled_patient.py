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

    def test_create_scheduled(self):

        #create
        sched = self.getScheduledPatient();

        #assert 60 hours
        self.assertEqual(sched.hoursToGo, 60)
        
    def test_create_scheduled_hours_passed(self):

        #create
        sched = self.getScheduledPatient();

        #pass time
        sched.hours_has_passed(10)

        #assert 50
        self.assertEqual(sched.hoursToGo, 50)
        
    def test_schedule_should_be_executed(self):

        #create
        sched = self.getScheduledPatient();
        
        #pass time
        sched.hours_has_passed(60)

        #assert true
        self.assertEqual(sched.should_be_executed(), True)
        
    def test_schedule_should_be_rescheduled_NEG(self):

        #create
        sched = self.getScheduledPatient();

        #pass time
        sched.hours_has_passed(50)

        #try to reschedule 12 hours from now
        #assert exception
        with self.assertRaises(Exception):
            sched.reschedule(12);
        
    def test_schedule_should_be_rescheduled_POS(self):

        #create
        sched = self.getScheduledPatient();

        #pass time
        sched.hours_has_passed(60)

        #try to reschedule 12 hours from now
        sched.reschedule(12);

        #assert rescheduled
        self.assertTrue(sched.has_been_rescheduled);


if __name__ == '__main__':
    unittest.main(verbosity=2)