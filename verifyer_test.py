import unittest
from verifyer import testFunction

class TestTestFunction(unittest.TestCase):
        def test_one_move(self):
            print("Testing One Move")
            result = testFunction("verifyerTests/testOneMove.txt")
            self.assertTrue(result)
            print("\n\n")

        def test_one_by_one(self):
            print("Testing One By One")
            result = testFunction("verifyerTests/testOnebyOne.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_bad_score(self):
            print("Testing Bad Score")
            result = testFunction("verifyerTests/testBadScore.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_bad_move_count(self):
            print("Testing Bad Move Count")
            result = testFunction("verifyerTests/testBadMoveCount.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_bad_size(self):
            print("Testing Bad Size")
            result = testFunction("verifyerTests/testBadSize.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_call_empty(self):
            print("Testing Empty Click")
            result = testFunction("verifyerTests/testCallEmpty.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_dependant_moves(self):
            print("Testing Dependant Moves")
            result = testFunction("verifyerTests/testDependantMoves.txt")
            self.assertTrue(result)
            print("\n\n")

        def test_multiple_moves(self):
            print("Testing Multiple Moves")
            result = testFunction("verifyerTests/testMultipleMoves.txt")
            self.assertTrue(result)
            print("\n\n")

        def test_out_of_bounds(self):
            print("Testing Out Of Bounds Click")
            result = testFunction("verifyerTests/testOutOfBounds.txt")
            self.assertFalse(result)
            print("\n\n")

        def test_column_shift(self):
            print("Testing Column Shift")
            result = testFunction("verifyerTests/testColumnShift.txt")
            self.assertTrue(result)
            print("\n\n")

if __name__ == "__main__" :
    unittest.main()