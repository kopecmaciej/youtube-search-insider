import unittest

from youtube.search import YoutubeSearcher

class TestYoutubeSearch(unittest.TestCase):
    def setUp(self):
        self._duration_to_minutes = YoutubeSearcher("test_phrase")._duration_to_seconds
        self._get_views = YoutubeSearcher("test_phrase")._get_views

    ### _duration_to_minutes tests ###
    def test_duration_none_input(self):
        self.assertEqual(self._duration_to_minutes(None), 0)

    def test_duration_integer_input(self):
        self.assertEqual(self._duration_to_minutes(30), 0)

    def test_duration_zero_hour(self):
        self.assertEqual(self._duration_to_minutes('00:30:20'), 30 + 20 / 60)

    def test_duration_full_duration(self):
        self.assertEqual(self._duration_to_minutes('01:30:20'), 60 + 30 + 20 / 60)

    def test_duration_minutes_seconds(self):
        self.assertEqual(self._duration_to_minutes('30:20'), 30 + 20 / 60)

    def test_duration_only_seconds(self):
        self.assertEqual(self._duration_to_minutes('00:20'), 20 / 60)

    def test_duration_only_minutes(self):
        self.assertEqual(self._duration_to_minutes('30'), 30 / 60)

    def test_duration_invalid_format(self):
        with self.assertRaises(ValueError):
            self._duration_to_minutes('invalid:input')

    ### _get_views tests ###
    def test_views_none_input(self):
        self.assertEqual(self._get_views(None), 0)

    def test_views_valid_input(self):
        self.assertEqual(self._get_views('3 000 230 views'), 3000230)

    def test_views_valid_input2(self):
        self.assertEqual(self._get_views('3,000 views'), 3000)

    def test_views_invalid_input(self):
        self.assertEqual(self._get_views('invalid:input'), 0)
if __name__ == '__main__':
    unittest.main()
