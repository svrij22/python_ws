import unittest
import patient
import numpy
import scipy
from patient import ScheduledPatient
from patient import Patient
from icu import IcuBed

class DataTests(unittest.TestCase):

    def getPatient(self) -> Patient:

        #create patient
        nPatient = patient.new_patient(True);
        return nPatient;

    def getBed(self) -> IcuBed:
        return IcuBed();

    def test_bed_is_empty(self):
        
        # get bed
        bed = self.getBed();

        #assert false
        self.assertEqual(bed.is_occupied(), False)
        
    def test_bed_is_not_empty(self):
        
        # get bed
        bed = self.getBed();
        bed.set_patient(self.getPatient())

        #assert false
        self.assertEqual(bed.is_occupied(), True)
        
    def test_bed_assign_twice(self):
        
        # get bed
        bed = self.getBed();
        bed.set_patient(self.getPatient())

        # assert exception
        with self.assertRaises(Exception):
            bed.set_patient(self.getPatient())

    def test_bed_get_patient_exception(self):
        
        # get bed
        bed = self.getBed();

        # assert exception
        with self.assertRaises(Exception):
            bed.get_patient()
            
    def test_bed_clear(self):
        
        # get bed
        bed = self.getBed();
        bed.set_patient(self.getPatient())

        #clear
        bed.clear();
        
        #assert false
        self.assertEqual(bed.is_occupied(), False)


if __name__ == '__main__':
    unittest.main(verbosity=2)