# -*- coding: UTF-8 -*-
""""
Created on 17.02.20
Evaluation script for Hulth 2003 (inspec) keywords dataset.
    Cite: Improved automatic keyword extraction given more linguistic knowledge
            https://dl.acm.org/doi/10.3115/1119355.1119383

:author:     Martin Dočekal
"""
import argparse
import glob
import os
import sys
from argparse import ArgumentParser
from enum import Enum, auto

from nltk import PorterStemmer
from spacy.lang.en import English
from tqdm import tqdm
from typing import Any, Set, Tuple

from evalhulth2003.inspec_doc_reader import InspecDocReader
from evalhulth2003.utils.generic import subSeq


class ArgumentParserError(Exception):
    """
    Exceptions for argument parsing.
    """
    pass


class ExceptionsArgumentParser(ArgumentParser):
    """
    Argument parser that uses exceptions for error handling.
    """

    def error(self, message):
        raise ArgumentParserError(message)


class ArgumentsManager(object):
    """
    Parsers arguments for script.
    """

    @classmethod
    def parseArgs(cls):
        """
        Performs arguments parsing.

        :param cls: arguments class
        :returns: Parsed arguments.
        """

        parser = ExceptionsArgumentParser(
            description="Script for evaluation of your results on Hulth 2003 (inspec) keywords dataset.")

        subparsers = parser.add_subparsers()

        keywordsParser = subparsers.add_parser('keywords', help="Selects keywords that are actually in a text.")
        keywordsParser.add_argument("-d", "--data",
                                    help="Path to directory with *.abstr and *.uncontr files.", type=str,
                                    required=True)
        keywordsParser.add_argument("-r", "--results",
                                    help="Path to directory where new *.uncontr_in files will be saved. (one file for each ID)",
                                    type=str,
                                    required=True)
        keywordsParser.set_defaults(func=callSelectKeywords)

        evalParser = subparsers.add_parser('eval', help="Keywords extraction evaluation of Hulth 2003 (inspec).")
        evalParser.add_argument("-g", "--groundTruth",
                                help="Path to directory with ground truths in *.uncontr_in files.", type=str,
                                required=True)
        evalParser.add_argument("-p", "--predicted",
                                help="Path to directory with predicted keywords in *.res files.", type=str,
                                required=True)
        evalParser.set_defaults(func=callEval)

        evalGenParser = subparsers.add_parser('evalGen', help="Keywords generation evaluation of Hulth 2003 (inspec).")
        evalGenParser.add_argument("-g", "--groundTruth",
                                   help="Path to directory with ground truths in *.uncontr files.", type=str,
                                   required=True)
        evalGenParser.add_argument("-p", "--predicted",
                                   help="Path to directory with predicted keywords in *.res files.", type=str,
                                   required=True)
        evalGenParser.set_defaults(func=callEvalGen)

        subparsersForHelp = {
            'eval': evalParser,
            'evalGen': evalGenParser,
            'keywords': keywordsParser
        }

        if len(sys.argv) < 2:
            parser.print_help()
            return None
        try:
            parsed = parser.parse_args()

        except ArgumentParserError as e:
            for name, subParser in subparsersForHelp.items():
                if name == sys.argv[1]:
                    subParser.print_help()
                    break
            print("\n" + str(e), file=sys.stdout, flush=True)
            return None

        return parsed


def callSelectKeywords(args):
    """
    Method for keywords selection.

    :param args: User arguments.
    :type args: argparse.Namespace
    """

    docReader = InspecDocReader(args.data)
    tokenizer = English()
    for name, content, keywords in tqdm(docReader, desc="Selecting", unit="document"):
        content = [t.lemma_.lower() for t in tokenizer(content)]
        keywords = [[t for t in tokenizer(kw.strip())] for kw in keywords]

        with open(os.path.join(args.results, name + ".uncontr_in"), "w") as resF:
            print("; ".join(
                [" ".join(t.text for t in k) for k in keywords if subSeq([t.lemma_.lower() for t in k], content)]),
                file=resF)  # filter only those that are in


def precisionRecallF1(correct: int, extracted: int, groundTruth: int) -> Tuple[float, float, float]:
    """
    Calculates metrices.

    :param correct: Number of correct keywords.
    :type correct: int
    :param extracted: Number of extracted keywords.
    :type extracted: int
    :param groundTruth: Number of annotated keywords.
    :type groundTruth: int
    :return: precision, recall, F1
    :rtype: Tuple[float, float, float]
    :raise ValueError: When invalid values are passed.
    """
    if correct > extracted:
        raise ValueError("Number of correct keywords is greater than number of all extracted keywords.")

    if groundTruth == 0 and correct > 0:
        raise ValueError("There should be no keywords, but correct is > 0.")

    precision = correct / extracted if extracted > 0 else 0
    recall = correct / groundTruth if groundTruth > 0 else 0
    return precision, recall, 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0


def printEval(title: str, correct: int, extracted: int, groundTruth: int):
    """
    Prints evaluation metrics.

    :param title: Title that will be printed.
    :type title: str
    :param correct: Number of correctly predicted keyphrases.
    :type correct: int
    :param extracted: Number of extracted keyphrases.
    :type extracted: int
    :param groundTruth: Number of ground truth phrases.
    :type groundTruth: int
    """

    print(title)
    precision, recall, F1 = precisionRecallF1(correct, extracted, groundTruth)

    print("\tprecision\t{}".format(precision))
    print("\trecall\t{}".format(recall))
    print("\tF1\t{}".format(F1))


def callEval(args: argparse.Namespace):
    """
    Method for evaluation of the keywords extraction task on the Inspec dataset.

    :param args: User arguments.
    :type args: argparse.Namespace
    """

    return evalOn(args, "uncontr_in")


def callEvalGen(args: argparse.Namespace):
    """
    Method for evaluation of the keywords generation task on the Inspec dataset.

    :param args: User arguments.
    :type args: argparse.Namespace
    """

    return evalOn(args, "uncontr")


def evalOn(args: argparse.Namespace, targetsExtension: str):
    """
    Method for evaluation on the Inspec dataset.

    :param args: User arguments.
    :type args: argparse.Namespace
    :param targetsExtension: The extension of files that contains target keywords.
        Pass the extension without the dot.
        Example:
            OK -> uncontr
            INVALID -> .uncontr
    :type targetsExtension: str
    """

    allGtNames = []
    for filePath in glob.glob(os.path.join(args.groundTruth, "*." + targetsExtension)):
        allGtNames.append(os.path.basename(filePath).rsplit(".", maxsplit=1)[0])

    res = {
        "plain": {"correct": 0, "correctPartOf": 0, "extracted": 0, "groundTruth": 0},
        "lower case": {"correct": 0, "correctPartOf": 0, "extracted": 0, "groundTruth": 0},
        "lower case lemma": {"correct": 0, "correctPartOf": 0, "extracted": 0, "groundTruth": 0},
        "lower case stem": {"correct": 0, "correctPartOf": 0, "extracted": 0, "groundTruth": 0}
    }

    evaluators = {
        "plain": Evaluator(Evaluator.Match.PLAIN),
        "lower case": Evaluator(Evaluator.Match.LOWER_CASE),
        "lower case lemma": Evaluator(Evaluator.Match.LOWER_CASE_LEMMA),
        "lower case stem": Evaluator(Evaluator.Match.LOWER_CASE_STEM)
    }

    for name in tqdm(allGtNames, desc="Evaluating", unit="document"):
        with open(os.path.join(args.groundTruth, name + "." + targetsExtension), "r") as gtF, \
                open(os.path.join(args.predicted, name + ".res"), "r") as resF:
            predicted = {kw.strip() for kw in resF}
            truth = set()
            for kw in gtF.read().split(";"):
                kw = " ".join(kw.strip().split())
                if len(kw) > 0:
                    truth.add(kw)

            for match, evaluator in evaluators.items():
                actE = evaluator(predicted, truth)

                res[match]["extracted"] += actE[0]
                res[match]["groundTruth"] += actE[1]
                res[match]["correct"] += actE[2]
                res[match]["correctPartOf"] += actE[3]

    printEval("Exact match:", res["plain"]["correct"], res["plain"]["extracted"], res["plain"]["groundTruth"])
    printEval("Part of match:", res["plain"]["correctPartOf"], res["plain"]["extracted"],
              res["plain"]["groundTruth"])
    printEval("Exact match on lower case form:", res["lower case"]["correct"], res["lower case"]["extracted"],
              res["lower case"]["groundTruth"])
    printEval("Part of match on lower case form:", res["lower case"]["correctPartOf"],
              res["lower case"]["extracted"], res["lower case"]["groundTruth"])
    printEval("Exact match on lower case lemma form:", res["lower case lemma"]["correct"],
              res["lower case lemma"]["extracted"], res["lower case lemma"]["groundTruth"])
    printEval("Part of match on lower case lemma form:", res["lower case lemma"]["correctPartOf"],
              res["lower case lemma"]["extracted"], res["lower case lemma"]["groundTruth"])
    printEval("Exact match on lower case stem form:", res["lower case stem"]["correct"],
              res["lower case stem"]["extracted"], res["lower case stem"]["groundTruth"])
    printEval("Part of match on lower case stem form:", res["lower case stem"]["correctPartOf"],
              res["lower case stem"]["extracted"], res["lower case stem"]["groundTruth"])


class Evaluator(object):
    """
    Functor class for evaluation of predicted keywords.
    """

    class Match(Enum):
        """
        Type of match for keywords.
        """
        PLAIN = auto()
        """
        All keywords tokens must match exactly.
        """

        LOWER_CASE = auto()
        """
        Case insensitive variant of match.
        """
        LOWER_CASE_LEMMA = auto()
        """
        Case insensitive match on lemma form of keywords tokens.
        """

        LOWER_CASE_STEM = auto()
        """
        Case insensitive match on stem form of keywords tokens.
        """

    def __init__(self, match: Match):
        """
        Initialization of evaluator.

        :param match: Type of match. Determines which keywords are good.
            For more information see the Match enum class.
        :type match: Match
        """

        tokenizer = English()
        stemmer = PorterStemmer()

        self.transform = {
            self.Match.PLAIN: lambda x: (tuple(t.text for t in tokenizer(kw)) for kw in x),
            self.Match.LOWER_CASE: lambda x: (tuple(t.text.lower() for t in tokenizer(kw)) for kw in x),
            self.Match.LOWER_CASE_LEMMA: lambda x: (tuple(t.lemma_.lower() for t in tokenizer(kw)) for kw in x),
            self.Match.LOWER_CASE_STEM: lambda x: (tuple(stemmer.stem(t.text) for t in tokenizer(kw)) for kw in x)
        }[match]

    def __call__(self, predicted: Set[str], targets: Set[str]) -> Tuple[int, int, int, int]:
        """
        Performs evaluation of keywords.

        :param predicted: Predicted keywords.
        :type predicted: Set[str]
        :param targets: Ground truth targets.
        :type targets: Set[str]
        :return: Tuple:
            number of distinct predicted keywords
            number of distinct ground truth keywords
            number of correctly predicted keywords
            number of predicted keywords that are sub-phrase of an ground truth keyword
        :rtype: Tuple[int, int, int, int]
        """

        actPred = set(self.transform(predicted))
        actTruth = set(self.transform(targets))

        return len(actPred), len(actTruth), len(actPred & actTruth), self.partOfMatch(actPred, actTruth)

    @staticmethod
    def partOfMatch(predicted: Set[Any], truth: Set[Any]) -> int:
        """
        Calculates how many predicted keyphrases are part of at least one golden truth keyphrase.

        :param predicted: Predicted keyphrases.
        :type predicted: Set[Any]
        :param truth: Golden truth keyphrases.
        :type truth: Set[Any]
        :return: Number of keyphrases from predicted that are part of any keyphrase from truth.
        :rtype: int
        """

        counter = 0

        for predKW in predicted:
            for truthKW in truth:
                if len(predKW) <= len(truthKW) and \
                        any(predKW == truthKW[offset:offset + len(predKW)] for offset in
                            range(0, len(truthKW) - len(predKW) + 1)):
                    counter += 1
                    break

        return counter


def main():
    args = ArgumentsManager.parseArgs()

    if args is not None:
        args.func(args)
    else:
        exit(1)


if __name__ == '__main__':
    main()
