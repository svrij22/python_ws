import unittest
import patient
import numpy
import scipy

class DataTests(unittest.TestCase):

    def test_create_new_patient(self):

        nPatient = patient.new_patient(True);
        self.assertEqual(nPatient.isPlanned, True)
        
    def test_create_new_patient_hourtogo(self):

        nPatient = patient.new_patient(True);
        self.assertEqual(nPatient.hoursToGo > 0, True)
        
    def test_create_new_patient_should_be_discharged_NEG(self):

        nPatient = patient.new_patient(True);
        self.assertEqual(nPatient.should_be_discharged(), False)
        
    def test_create_new_patient_should_be_discharged_POS(self):

        nPatient = patient.new_patient(True);
        nPatient.hours_has_passed(5600);
        self.assertEqual(nPatient.should_be_discharged(), True)


if __name__ == '__main__':
    unittest.main(verbosity=2)