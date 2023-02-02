import unittest

import numpy
import scipy

import patient


class DataTests(unittest.TestCase):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def do_test_interval(self, isPlanned, weekday):

        # Calc intervals
        intervals = []
        for x in range(100000):
            intervals.append(patient.new_patient_interval(isPlanned, weekday))

        # Get mean and round
        g_mean = numpy.mean(intervals)
        g_mean_rounded = numpy.round(g_mean, 1)

        # assert
        if isPlanned:
            self.assertAlmostEqual(g_mean_rounded, patient.EXPO_VARIABLE_PLANNED[weekday], 0)
        else:
            self.assertAlmostEqual(g_mean_rounded, patient.EXPO_VARIABLE_UNPLANNED_W_DENIED, 0)

    def test_interval_planned_monday(self):
        self.do_test_interval(True, self.weekdays[0])

    def test_interval_planned_tuesday(self):
        self.do_test_interval(True, self.weekdays[1])

    def test_interval_planned_wednesday(self):
        self.do_test_interval(True, self.weekdays[2])

    def test_interval_planned_thursday(self):
        self.do_test_interval(True, self.weekdays[3])

    def test_interval_planned_friday(self):
        self.do_test_interval(True, self.weekdays[4])

    def test_interval_planned_saturday(self):
        self.do_test_interval(True, self.weekdays[5])

    def test_interval_planned_sunday(self):
        self.do_test_interval(True, self.weekdays[6])

    def test_interval_unplanned(self):
        self.do_test_interval(False, '')

    def test_interval_COVID(self):
        # Calc intervals
        intervals = []
        for x in range(100000):
            intervals.append(patient.new_COVID_patient_interval())

        # Get mean and round
        g_mean = numpy.mean(intervals)
        g_mean_rounded = numpy.round(g_mean, 1)

        # assert
        self.assertAlmostEqual(g_mean_rounded, patient.default_settings.EXPO_VARIABLE_COVID, 0)

    def test_interval_planned_amount(self):
        for x in range(10):
            n_schedule = patient.new_patient_schedule_stack()
            print(len(n_schedule))

    def test_proc_length(self):
        # print('Running  prodecure length test')

        for spec in patient.SPECIALISM_MU_SIGMA.keys():
            # Calc intervals
            proc_lengths = []
            for x in range(100000):
                proc_lengths.append(patient.new_prodecure_length(spec))

            # Get mean and round
            shape, location, scale = scipy.stats.lognorm.fit(proc_lengths)
            mu, sigma = numpy.log(scale), shape

            # assert almost equal
            self.assertAlmostEqual(mu, patient.SPECIALISM_MU_SIGMA[spec][0], 1)
            self.assertAlmostEqual(sigma, patient.SPECIALISM_MU_SIGMA[spec][1], 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
