from unittest import TestCase

from app import app, games

import json

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('<table class="board">', html)
            self.assertIn('<table', html)
            self.assertIn('Homepage Template - used in test', html)


    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')
            json_resp = response.get_data(as_text=True)
            # response.get_json

            obj = json.loads(json_resp)
            board = obj["board"]
            self.assertEqual(len(board), 5)
            self.assertIn("board", json_resp)
            self.assertIn("gameId", json_resp)
            # more specific tests (inner contents of board)
            # game id in games dictionary?

    def test_api_score_word(self):
        """Test if word is not in word list and not on board"""

        with self.client as client:
            response = client.post('/api/new-game')
            json_resp = response.get_data(as_text=True)

            obj = json.loads(json_resp)
            id = obj["gameId"]
            game = games[id]

            self.assertFalse(game.is_word_in_word_list("AIESFIPGWGIP"))
            self.assertFalse(game.check_word_on_board("ASDFAWEGAWEG"))
            # test randomized board