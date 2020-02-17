# -*- coding: UTF-8 -*-
""""
Created on 17.02.20
Module containing class for reading the inspec dataset.

:author:     Martin Dočekal
"""
import glob
import os

from typing import Tuple, Generator, List


class InspecDocReader(object):
    """
    Reader of Inspec documents.
    """

    def __init__(self, d: str, ):
        """
        Initialization of a reader.

        :param d: Path to folder with .abstr and .contr/uncontr files.
        :type d: str
        """

        self._d = d

        self.documentsNames = []
        self.documentsPaths = []
        self.documentsPathsUncontr = []
        for filePath in glob.glob(os.path.join(d, "*.abstr")):
            name = os.path.basename(filePath)[:-6]  # get the name without extension
            pathWithoutExtension = filePath[:-6]

            self.documentsNames.append(name)
            self.documentsPaths.append(filePath)
            self.documentsPathsUncontr.append(pathWithoutExtension + ".uncontr")

    def __len__(self):
        return len(self.documentsNames)

    def __iter__(self) -> Generator[Tuple[str, str, List[str]], None, None]:
        """
        Iterates over the documents.

        :return:  Genearator that generates that tuple:
            (name/id of document, keywords)
        :rtype: Generator[Tuple[str, str, List[str]], None, None]
        """
        for name, filePath, keywordsFilePath in zip(self.documentsNames, self.documentsPaths, self.documentsPathsUncontr):
            with open(filePath, "r") as f, open(keywordsFilePath, "r") as keyF:
                # Firstly let's get the keywords.
                keywords = []
                for kw in keyF.read().split(";"):
                    kw = " ".join(kw.strip().split())
                    if len(kw)>0:
                        keywords.append(kw)

                # than the content
                content = " ".join(f.read().split())

                yield name, content, keywords
