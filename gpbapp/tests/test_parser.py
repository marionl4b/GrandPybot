from gpbapp import parser


class TestParser:

    PARSER = parser.Parser()

    def test_empty_message(self):
        self.PARSER.parse_usermsg({"userMessage": ""})
        assert self.PARSER.error

    def test_stopwords(self):
        self.PARSER.parse_usermsg({"userMessage": "zut, alors !"})
        assert len(self.PARSER.parsed_message) == 0

    def test_valid_location(self):
        self.PARSER.parse_usermsg({"userMessage": "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms"})
        assert self.PARSER.parsed_message == ["openclassrooms"]

    def test_punctuation(self):
        self.PARSER.parse_usermsg({"userMessage": ": ; !+"})
        assert self.PARSER.error
