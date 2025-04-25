import unittest
from src.utils import truncate_text

class TestChatbot(unittest.TestCase):
    def test_truncate_text(self):
        test_text = "This is a test. This is another test. And a third test."
        truncated = truncate_text(test_text, 20)
        self.assertEqual(truncated, "This is a test.")

if __name__ == "__main__":
    unittest.main()