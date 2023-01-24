import unittest

import numpy
import scipy

import patient


class DataTests(unittest.TestCase):

    def test_interval_unplanned(self):
        # print('Running interval test - unplanned')

        # Calc intervals
        intervals = []
        for x in range(100000):
            intervals.append(patient.new_patient_interval(False))

        # Get mean and round
        g_mean = numpy.mean(intervals)
        g_mean_rounded = numpy.round(g_mean, 1)

        # assert almost equal
        self.assertAlmostEqual(g_mean_rounded, 5.9849999051952985, 1)

    def test_interval_planned(self):
        # print('Running interval test - planned')

        # Calc intervals
        intervals = []
        for x in range(100000):
            intervals.append(patient.new_patient_interval(True))

        # Get mean and round
        g_mean = numpy.mean(intervals)
        g_mean_rounded = numpy.round(g_mean, 1)

        # assert almost equal
        self.assertAlmostEqual(g_mean_rounded, 11.659628456007704, 0)

    def test_proc_length(self):
        # print('Running  prodecure length test')

        # Calc intervals
        proc_lengths = []
        for x in range(100000):
            proc_lengths.append(patient.new_prodecure_length())

        # Get mean and round
        shape, location, scale = scipy.stats.lognorm.fit(proc_lengths)
        mu, sigma = numpy.log(scale), shape

        # assert almost equal
        self.assertAlmostEqual(mu, 3.50502901187668, 1)
        self.assertAlmostEqual(sigma, 1.3165461050924663, 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
