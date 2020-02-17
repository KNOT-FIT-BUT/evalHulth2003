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
            "stemSame": {"telecom", "Nuvox communication", "wavelength service", "telecom industry",
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

        if os.path.exists(self.pathToEvalFile):
            os.remove(self.pathToEvalFile)

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

        self.assertAlmostEqual(res["partOnLowerCaseForm"]["precision"], 818181818181818)
        self.assertAlmostEqual(res["partOnLowerCaseForm"]["recall"], 0.6)
        self.assertAlmostEqual(res["partOnLowerCaseForm"]["F1"], 0.692307692307692)

        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["precision"], 0.818181818181818)
        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["recall"], 0.6)
        self.assertAlmostEqual(res["exactOnLowerCaseLemmaForm"]["F1"], 0.692307692307692)

        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["precision"], 909090909090909)
        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["recall"], 0.666666666666667)
        self.assertAlmostEqual(res["partOnLowerCaseLemmaForm"]["F1"], 0.769230769230769)

        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["precision"], 0.909090909090909)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["recall"], 0.666666666666667)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["F1"], 0.769230769230769)

        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["precision"], 1)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["recall"], 0.733333333333333)
        self.assertAlmostEqual(res["exactOnLowerCaseStemForm"]["F1"], 0.846153846153846)

    def evalAll(self, e: Evaluator, res: Dict[str, Tuple[int, int, int, int]]) -> None:
        """
        Sared part for testing the evaluator on all testing data.

        :param e: Evaluator for testing.
        :type e: Evaluator
        :param res: Results on shared data.
            Dict with key defining name of test data and values:
                number of distinct predicted keywords
                number of distinct target keywords
                number of correctly predicted distinct keywords
                number of predicted distinct keywords that are sub-phrases of an target keyword
        :type res: Dict[str, Tuple[int, int, int, int]]
        """
        for name, keywords in self.predicted.items():
            predicted, truth, correct, partCorrect = e(keywords, self.target)

            predictedTarget, truthTarget, correctTarget, partCorrectTarget = res[name]

            self.assertEqual(predicted, predictedTarget)
            self.assertEqual(truth, truthTarget)
            self.assertEqual(correct, correctTarget)
            self.assertEqual(partCorrect, partCorrectTarget)

    def test_eval_plain(self):
        """
        Test of plain match.
        """
        self.evalAll(Evaluator(Evaluator.Match.PLAIN), {
            "ideal": (5, 5, 5, 5),
            "caseDiffer": (5, 5, 3, 3),
            "lemmaSame": (5, 5, 3, 3),
            "stemSame": (5, 5, 3, 3),

            "ideal2": (2, 5, 2, 2),
            "caseDiffer2": (3, 5, 2, 2),
            "lemmaSamer2": (3, 5, 2, 2),
            "stemSame2": (3, 5, 2, 2),

            "wrong all": (2, 5, 0, 0),

            "nothing": (0, 5, 0, 0),

            "partialIdeal": (5, 5, 1, 5),
            "partialCaseDiffer": (5, 5, 1, 4),
            "partialLemmaSame": (5, 5, 1, 3),
            "partialStemSame": (5, 5, 1, 3),
        })

    def test_eval_lower_case(self):
        """
        Test of lower case match.
        """

        self.evalAll(Evaluator(Evaluator.Match.LOWER_CASE), {
            "ideal": (5, 5, 5, 5),
            "caseDiffer": (5, 5, 5, 5),
            "lemmaSame": (5, 5, 4, 4),
            "stemSame": (5, 5, 4, 4),

            "ideal2": (2, 5, 2, 2),
            "caseDiffer2": (2, 5, 2, 2),
            "lemmaSamer2": (3, 5, 2, 2),
            "stemSame2": (3, 5, 2, 2),

            "wrong all": (2, 5, 0, 0),

            "nothing": (0, 5, 0, 0),

            "partialIdeal": (5, 5, 1, 5),
            "partialCaseDiffer": (5, 5, 1, 5),
            "partialLemmaSame": (5, 5, 1, 4),
            "partialStemSame": (5, 5, 1, 4),
        })

    def test_eval_lower_case_lemma(self):
        """
        Test of lower case lemma match.
        """

        self.evalAll(Evaluator(Evaluator.Match.LOWER_CASE_LEMMA), {
            "ideal": (5, 5, 5, 5),
            "caseDiffer": (5, 5, 5, 5),
            "lemmaSame": (5, 5, 5, 5),
            "stemSame": (5, 5, 4, 4),

            "ideal2": (2, 5, 2, 2),
            "caseDiffer2": (2, 5, 2, 2),
            "lemmaSamer2": (2, 5, 2, 2),
            "stemSame2": (3, 5, 2, 2),

            "wrong all": (2, 5, 0, 0),

            "nothing": (0, 5, 0, 0),

            "partialIdeal": (5, 5, 1, 5),
            "partialCaseDiffer": (5, 5, 1, 5),
            "partialLemmaSame": (5, 5, 1, 5),
            "partialStemSame": (5, 5, 1, 4),
        })

    def test_eval_lower_case_stem(self):
        """
        Test of lower case stem match.
        """

        self.evalAll(Evaluator(Evaluator.Match.LOWER_CASE_STEM), {
            "ideal": (5, 5, 5, 5),
            "caseDiffer": (5, 5, 5, 5),
            "lemmaSame": (5, 5, 5, 5),
            "stemSame": (5, 5, 5, 5),

            "ideal2": (2, 5, 2, 2),
            "caseDiffer2": (2, 5, 2, 2),
            "lemmaSamer2": (2, 5, 2, 2),
            "stemSame2": (3, 2, 2, 2),

            "wrong all": (2, 5, 0, 0),

            "nothing": (0, 5, 0, 0),

            "partialIdeal": (5, 5, 1, 5),
            "partialCaseDiffer": (5, 5, 1, 5),
            "partialLemmaSame": (5, 5, 1, 5),
            "partialStemSame": (5, 5, 1, 5),
        })

    def test_partOfMatch(self):
        """
        Test for part of match.
        """

        self.assertEqual(
            Evaluator.partOfMatch(
                {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"), ("mauris", ),
                 ("car",), ("vehicle",), ("Integer",)},
                set()),
            0
        )

        self.assertEqual(
            Evaluator.partOfMatch(set(), {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"),
                                          ("mauris",),
                                          ("car",), ("vehicle",), ("Integer",)}),
            0
        )

        self.assertEqual(
            Evaluator.partOfMatch({("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus")},
                                  {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"),
                                   ("mauris",),
                                   ("car",), ("vehicle",), ("Integer",)}),
            3
        )

        self.assertEqual(
            Evaluator.partOfMatch({("lorem", "ipsum"), ("vestibulum", "erat"), ("nascetur", "ridiculus", "mus")},
                                  {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"),
                                   ("mauris", ),
                                   ("car", ), ("vehicle", ), ("Integer", )}),
            2
        )

        self.assertEqual(
            Evaluator.partOfMatch({("lorem", "ipsum"), ("Vestibulum", "ipsum"), ("nascetur", "ridiculuses", "mus")},
                                  {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"),
                                   ("mauris", ),
                                   ("car", ), ("vehicle", ), ("Integer", )}),
            1
        )

        self.assertEqual(
            Evaluator.partOfMatch(
                {("lorem", "ipsum"), ("erat", ), ("nascetur", "ridiculus"), ("mus", ), ("ridiculuses", "mus"),
                 ("nascetur", )},
                {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"), ("mauris", ),
                 ("car", ), ("vehicle", ), ("Integer", )}),
            6
        )

        self.assertEqual(
            Evaluator.partOfMatch({("lorem", "ipsum"), ("Vestibulum", "erat"), ("ridiculuses", "mus")},
                                  {("lorem", "ipsum"), ("Vestibulum", "erat"), ("nascetur", "ridiculus", "mus"),
                                   ("mauris", ),
                                   ("car", ), ("vehicle", ), ("Integer", )}),
            2
        )

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
