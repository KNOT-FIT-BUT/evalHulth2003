# -*- coding: UTF-8 -*-
""""
Created on 17.02.20
Unit tests for the main module

:author:     Martin Dočekal
"""
import argparse
import os
import sys
import unittest

from evalhulth2003.__main__ import Evaluator, callEval, precisionRecallF1
from typing import Dict, Tuple


class TestEvaluator(unittest.TestCase):
    """
    Unit test of Evaluator.
    """

    def setUp(self) -> None:
        self.predicted = {
            "ideal": {"telecom", "nuvox communications", "wavelength service", "telecom industry",
                      "insider investment"},
            "caseDiffer": {"telecom", "Nuvox communications", "wavelength service", "telecom industry",
                           "Insider investment"},
            "lemmaSame": {"telecom", "Nuvox communication", "wavelength service", "telecom industry",
                          "Insider investment"},
            "stemSame": {"telecom", "Nuvox commun", "wavelength service", "telecom industry",
                         "Insider investment"},

            "ideal2": {"telecom", "nuvox communications"},
            "caseDiffer2": {"telecom", "nuvox communications", "Nuvox communications"},
            "lemmaSamer2": {"telecom", "nuvox communications", "Nuvox communication"},
            "stemSame2": {"telecom", "nuvox communications", "Nuvox commun"},

            "wrong all": {"wrong", "word wrong"},

            "nothing": set(),

            "partialIdeal": {"telecom", "communications", "wavelength", "telecom", "insider"},
            "partialCaseDiffer": {"telecom", "communications", "wavelength", "industry", "Insider"},
            "partialLemmaSame": {"telecom", "communication", "wavelength", "industry", "Insider"},
            "partialStemSame": {"telecom", "commun", "wavelength", "industry", "Insider"},

        }

        self.target = {
            "telecom", "nuvox communications", "wavelength service", "telecom industry", "insider investment"
        }

        self.pathToThisScriptFile = os.path.dirname(os.path.realpath(__file__))
        self.pathToEvalFile = os.path.join(self.pathToThisScriptFile, "tmp/eval.txt")


        self.dataFolder = os.path.join(self.pathToThisScriptFile, "fixtures/reader")

        self.savedStdout = sys.stdout

    def tearDown(self) -> None:
        sys.stdout = self.savedStdout

    def test_precision_recall_f1(self):
        """
        Tests the precision recall F1 method.

        """
        p, r, f = precisionRecallF1(10, 10, 10)
        self.assertAlmostEqual(p, 1.0)
        self.assertAlmostEqual(r, 1.0)
        self.assertAlmostEqual(f, 1.0)

        p, r, f = precisionRecallF1(0, 3, 10)
        self.assertAlmostEqual(p, 0.0)
        self.assertAlmostEqual(r, 0.0)
        self.assertAlmostEqual(f, 0.0)

        p, r, f = precisionRecallF1(2, 4, 10)
        self.assertAlmostEqual(p, 0.5)
        self.assertAlmostEqual(r, 0.2)
        self.assertAlmostEqual(f, 0.28571428571428571429)

    def test_call_eval(self):
        """
        Tests the call eval method.
        """

        with open(self.pathToEvalFile, "w") as evalF:
            sys.stdout = evalF
            callEval(argparse.Namespace(groundTruth=self.dataFolder, predicted=self.dataFolder))

        res = self.parseResults(self.pathToEvalFile)

        self.assertAlmostEqual(res["exact"]["precision"], 0.636363636363636)
        self.assertAlmostEqual(res["exact"]["recall"], 0.466666666666667)
        self.assertAlmostEqual(res["exact"]["F1"], 0.538461538461539)

        self.assertAlmostEqual(res["part"]["precision"], 0.727272727272727)
        self.assertAlmostEqual(res["part"]["recall"], 0.533333333333333)
        self.assertAlmostEqual(res["part"]["F1"], 0.615384615384615)

        self.assertAlmostEqual(res["exactOnLowerCaseForm"]["precision"], 0.727272727272727)
        self.assertAlmostEqual(res["exactOnLowerCaseForm"]["recall"], 0.533333333333333)
        self.assertAlmostEqual(res["exactOnLowerCaseForm"]["F1"], 0.615384615384615)

        self.assertAlmostEqual(res["partOnLowerCaseForm"]["precision"], 0.818181818181818)
        self.assertAlmostEqual(res["partOnLowerCaseForm"]["recall"], 0.6)
        self.assertAlmostEqual(res["partOnLowerCaseForm"]["F1"], 0.692307692307692)

        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["precision"], 0.818181818181818)
        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["recall"], 0.6)
        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["F1"], 0.692307692307692)

        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["precision"], 0.909090909090909)
        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["recall"], 0.666666666666667)
        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["F1"], 0.769230769230769)

        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["precision"], 0.909090909090909)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["recall"], 0.666666666666667)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["F1"], 0.769230769230769)

        self.assertAlmostEqual(res["partOnLowerCaseStemForm"]["precision"], 1)
        self.assertAlmostEqual(res["partOnLowerCaseStemForm"]["recall"], 0.733333333333333)
        self.assertAlmostEqual(res["partOnLowerCaseStemForm"]["F1"], 0.846153846153846)

    @staticmethod
    def parseResults(p: str) -> Dict[str, Dict[str, float]]:
        """
        Parses evaluation results.

        :param p: Path to file with results.
        :type p: str
        :return: Results from the evaluation
            First dict key is the match method.
            Key of second dictionary is the metric name and its value is the metric value.
        :rtype: Dict[str, Dict[str, float]]
        """
        res = {"exact": {}, "part": {}, "exactOnLowerCaseForm": {}, "partOnLowerCaseForm": {},
               "exactOnLowerCaseLemmaForm": {}, "partOnLowerCaseLemmaForm": {},
               "exactOnLowerCaseStemForm": {}, "partOnLowerCaseStemForm": {}}
        """
        Example of result file:
            Exact match:
                    precision       0.44279176201373
                    recall  0.707680250783699
                    F1      0.5447416046651921
            Part of match:
                    precision       0.54086302713305
                    recall  0.8644200626959248
                    F1      0.6653931228634627
            Exact match on lower case form:
                    precision       0.47289407839866554
                    recall  0.7405956112852664
                    F1      0.5772167362312939
            Part of match on lower case form:
                    precision       0.5778148457047539
                    recall  0.9049111807732497
                    F1      0.7052835182734398
            Exact match on lower case lemma form:
                    precision       0.4821337849280271
                    recall  0.7445083682008368
                    F1      0.5852605612087574
            Part of match on lower case lemma form:
                    precision       0.5867908552074513
                    recall  0.9061192468619247
                    F1      0.7123034227567067
            Exact match on lower case stem form:
                    precision       0.48424995743231736
                    recall  0.7445026178010471
                    F1      0.586815227483751
            Part of match on lower case stem form:
                    precision       0.5933934956580964
                    recall  0.912303664921466
                    F1      0.7190756215825854

        """
        with open(p, "r") as F:
            match = "exact"
            for line in F:
                if line.startswith("Exact match on lower case form"):
                    match = "exactOnLowerCaseForm"
                    continue
                elif line.startswith("Part of match on lower case form"):
                    match = "partOnLowerCaseForm"
                    continue
                elif line.startswith("Exact match on lower case lemma form"):
                    match = "exactOnLowerCaseLemmaForm"
                    continue
                elif line.startswith("Part of match on lower case lemma form"):
                    match = "partOnLowerCaseLemmaForm"
                    continue
                elif line.startswith("Exact match on lower case stem form"):
                    match = "exactOnLowerCaseStemForm"
                    continue
                elif line.startswith("Part of match on lower case stem form"):
                    match = "partOnLowerCaseStemForm"
                    continue
                elif line.startswith("Part of match"):
                    match = "part"
                    continue
                elif line.startswith("Exact match"):
                    match = "exact"
                    continue

                parts = line.strip().split("\t")

                res[match][parts[0]] = float(parts[1])
        return res


if __name__ == '__main__':
    unittest.main()
