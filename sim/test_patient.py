import unittest

import patient


class DataTests(unittest.TestCase):

    def test_create_new_patient(self):
        nPatient = patient.new_patient(True, 'Monday')
        self.assertEqual(nPatient.isPlanned, True)

    def test_create_new_patient_hourtogo(self):
        nPatient = patient.new_patient(True, 'Monday')
        self.assertEqual(nPatient.hoursToGo > 0, True)

    def test_create_new_patient_should_be_discharged_NEG(self):
        nPatient = patient.new_patient(True, 'Monday')
        self.assertEqual(nPatient.should_be_discharged(), False)

    def test_create_new_patient_should_be_discharged_POS(self):
        nPatient = patient.new_patient(True, 'Monday')
        nPatient.hours_has_passed(5600)
        self.assertEqual(nPatient.should_be_discharged(), True)

    departments = ['CARD/INT/OTHER', 'NEU/NEC', 'CAPU', 'CHIR']

    def test_specialism_gives_right_department_CARD(self):
        nPatient = patient.Patient(True, 0, 'CARD')
        self.assertEqual(nPatient.department(), self.departments[0])

    def test_specialism_gives_right_department_INT(self):
        nPatient = patient.Patient(True, 0, 'INT')
        self.assertEqual(nPatient.department(), self.departments[0])

    def test_specialism_gives_right_department_OTHER(self):
        nPatient = patient.Patient(True, 0, 'OTHER')
        self.assertEqual(nPatient.department(), self.departments[0])

    def test_specialism_gives_right_department_NEU(self):
        nPatient = patient.Patient(True, 0, 'NEU')
        self.assertEqual(nPatient.department(), self.departments[1])

    def test_specialism_gives_right_department_NEC(self):
        nPatient = patient.Patient(True, 0, 'NEC')
        self.assertEqual(nPatient.department(), self.departments[1])

    def test_specialism_gives_right_department_CAPU(self):
        nPatient = patient.Patient(True, 0, 'CAPU')
        self.assertEqual(nPatient.department(), self.departments[2])

    def test_specialism_gives_right_department_CHIR(self):
        nPatient = patient.Patient(True, 0, 'CHIR')
        self.assertEqual(nPatient.department(), self.departments[3])

    def test_create_new_COVID_patient(self):
        nPatient = patient.new_COVID_patient()
        self.assertEqual(nPatient.department(), 'COVID')


if __name__ == '__main__':
    unittest.main(verbosity=2)
