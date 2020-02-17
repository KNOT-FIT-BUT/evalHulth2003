# -*- coding: UTF-8 -*-
""""
Created on 17.02.20

:author:     Martin Dočekal
"""
import os
import unittest

from evalhulth2003.inspec_doc_reader import InspecDocReader


class TestInspecDocReader(unittest.TestCase):
    """
    Unit test of subSeq method.
    """

    contents = {
        "1": "Some article of unknown title This is article that is just for unit testing purposes.",
        "16": "Lorem ipsum Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Suspendisse nisl. Vestibulum erat nulla, ullamcorper nec, rutrum non, nonummy ac, erat. Nullam justo enim, consectetuer nec, ullamcorper ac, vestibulum in, elit. Integer pellentesque quam vel velit. Phasellus faucibus molestie nisl. Mauris tincidunt sem sed arcu. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas sollicitudin.",
        "1073": "Abstract (summary) An abstract is a brief summary of a research article, thesis, review, conference proceeding, or any in-depth analysis of a particular subject and is often used to help the reader quickly ascertain the paper's purpose.[1] When used, an abstract always appears at the beginning of a manuscript or typescript, acting as the point-of-entry for any given academic paper or patent application. Abstracting and indexing services for various academic disciplines are aimed at compiling a body of literature for that particular subject."
    }

    keywords = {
        "1": ["unit testing"],
        "16": ["lorem ipsum", "Vestibulum erat", "nascetur ridiculus mus", "mauris", "car", "vehicle", "Integer"],
        "1073": ["abstract", "summary", "academic paper", "Conference proceeding", "point-of-entry",
                 "patent application", "patent", "manuscript", "typescript", "object oriented programing",
                 "academic disciplines"],
    }

    def setUp(self) -> None:
        pathToThisScriptFile = os.path.dirname(os.path.realpath(__file__))
        self.reader = InspecDocReader(os.path.join(pathToThisScriptFile, "fixtures/reader"))

    def test_len(self):
        """
        Unit test of the length method.
        """
        self.assertEqual(len(self.reader), 3)

    def test_iter(self):
        """
        Unit test of the content reading.
        """

        for name, content, keywords in self.reader:
            self.assertTrue(name in self.keywords)
            self.assertEqual(self.contents[name], content)
            self.assertEqual(self.keywords[name], keywords)


if __name__ == '__main__':
    unittest.main()
