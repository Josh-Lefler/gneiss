#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2016--, gneiss development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------
import pandas as pd
import pandas.util.testing as pdt
import numpy as np
import statsmodels.formula.api as smf
import unittest
from gneiss._summary import RegressionResults
from skbio.stats.composition import (_gram_schmidt_basis, ilr_inv)


class TestRegressionResults(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame([[1, 3, 4, 5, 2, 3, 4],
                                  list(range(1, 8)),
                                  [1, 3, 2, 4, 3, 5, 4]],
                                 columns=['s1', 's2', 's3', 's4', 's5', 's6', 's7'],
                                 index=['Y1', 'Y2', 'X']).T
        model1 = smf.ols(formula="Y1 ~ X", data=self.data)
        model2 = smf.ols(formula="Y2 ~ X", data=self.data)
        self.results = [model1.fit(), model2.fit()]

    def test_r2(self):
        fittedvalues = pd.DataFrame({'s1': [1.986842, 1.236842],
                                     's2': [3.065789, 3.815789],
                                     's3': [2.526316, 2.526316],
                                     's4': [3.605263, 5.105263],
                                     's5': [3.065789, 3.815789],
                                     's6': [4.144737, 6.394737],
                                     's7': [3.605263, 5.105263]},
                                    index=['Y1','Y2']).T
        m = self.data.mean(axis=0)
        sse = ((fittedvalues - self.data.iloc[:, :2])**2).sum().sum()
        ssr = ((fittedvalues - m)**2).sum().sum()
        sst = ((m - self.data.iloc[:, :2])**2).sum().sum()
        exp_r2 = 1 - (sse / sst)

        res = RegressionResults(self.results)
        self.assertAlmostEqual(exp_r2, res.r2)

    def test_regression_results_pvalues(self):
        # checks to see if pvalues are calculated correctly.
        res = RegressionResults(self.results)
        exp = pd.DataFrame({'Intercept':[0.307081, 0.972395],
                            'X': [0.211391, 0.029677]},
                            index=['Y1', 'Y2'])
        pdt.assert_frame_equal(res.pvalues, exp,
                               check_exact=False,
                               check_less_precise=True)

if __name__ == "__main__":
    unittest.main()
