"""
Test cases for flashcards.py (Room 2: "What comes out").
Run: python3 test_flashcards.py

Designed cases (T1-T8), including boundary cases:
  T1 valid CSV with 2 cards            -> 2 cards loaded
  T2 empty CSV file (boundary)         -> [] and no crash
  T3 file does not exist               -> [] and no crash
  T4 rows with 1 column / blank cells  -> skipped, valid rows kept
  T5 ask_number lower bound (1)        -> accepted
  T6 ask_number upper bound (5)        -> accepted; 0 and 6 rejected
  T7 ask_number non-number input       -> re-asks, then accepts valid
  T8 user types 'q'                    -> returns None (quit)
"""
import os
import tempfile
import unittest
from unittest.mock import patch

import flashcards


def write_tmp(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


class TestLoadCards(unittest.TestCase):
    def test_T1_valid(self):
        p = write_tmp("cat,แมว\ndog,หมา\n")
        self.assertEqual(flashcards.load_cards(p), [("cat", "แมว"), ("dog", "หมา")])
        os.remove(p)

    def test_T2_empty_file(self):
        p = write_tmp("")
        self.assertEqual(flashcards.load_cards(p), [])
        os.remove(p)

    def test_T3_missing_file(self):
        self.assertEqual(flashcards.load_cards("no_such_file.csv"), [])

    def test_T4_bad_rows_skipped(self):
        p = write_tmp("onlyone\n,empty question\nq,\nok,fine\n")
        self.assertEqual(flashcards.load_cards(p), [("ok", "fine")])
        os.remove(p)


class TestAskNumber(unittest.TestCase):
    @patch("builtins.input", side_effect=["1"])
    def test_T5_lower_bound(self, _):
        self.assertEqual(flashcards.ask_number("", 1, 5), 1)

    @patch("builtins.input", side_effect=["0", "6", "5"])
    def test_T6_upper_bound_and_out_of_range(self, _):
        self.assertEqual(flashcards.ask_number("", 1, 5), 5)

    @patch("builtins.input", side_effect=["abc", "", "3.5", "2"])
    def test_T7_non_numbers(self, _):
        self.assertEqual(flashcards.ask_number("", 1, 5), 2)

    @patch("builtins.input", side_effect=["q"])
    def test_T8_quit(self, _):
        self.assertIsNone(flashcards.ask_number("", 1, 5))


if __name__ == "__main__":
    unittest.main(verbosity=2)
