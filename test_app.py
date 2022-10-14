from unittest import TestCase

from app import app, games

from boggle import DEFAULT_LETTERS_BY_FREQ

from wordlist import WordList

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
            obj = response.get_json()

            board = obj["board"]
            game_id = obj["gameId"]
            self.assertEqual(len(board), 5)
            self.assertIn("board", obj)
            self.assertIn("gameId", obj)

            # more specific tests (inner contents of board)
            all_cells_are_letters = True
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if not board[i][j] in DEFAULT_LETTERS_BY_FREQ:
                        all_cells_are_letters = False

            self.assertTrue(all_cells_are_letters)

            # game id in games dictionary?
            self.assertIn(game_id, games)

    def test_api_score_word(self):
        """Test if word is not in word list and not on board"""

        with self.client as client:
            response1 = client.post('/api/new-game')
            json_game = response1.get_json()
            game_id1 = json_game["gameId"]

            # get the board and fill with all A's
            game = games[game_id1]
            game.board = [
                ["C", "A", "T", "D", "O"],
                ["C", "A", "T", "D", "O"],
                ["C", "A", "T", "D", "O"],
                ["C", "A", "T", "D", "O"],
                ["C", "A", "T", "D", "O"],
            ]
            game.word_list = WordList("test_dictionary.txt")

            response2 = client.post(
                "/api/score-word", 
                data = {'gameId': game_id1, "word": "CAT"}
                )

            result = response2.get_json()

            ok = result.get("result")

            self.asssertTrue(ok, True)


            

            # obj = json.loads(json_resp)
            # id = obj["gameId"]
            # game = games[id]

            # self.assertFalse(game.is_word_in_word_list("AIESFIPGWGIP"))
            # self.assertFalse(game.check_word_on_board("ASDFAWEGAWEG"))
            # # test randomized board