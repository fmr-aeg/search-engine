from Levenshtein import distance as levenshtein_distance
import unicodedata

class SearchEngine:
    def __init__(self):
        # Dans cet element j'ai une clef qui est le nom du livre et la value qui est son identifiant dans la collection MongoDB

        # Pour commencer on va juste avoir un dic avec {nom : lien} et on construira la collection mongoDB à la maison
        self.books_index = {}

    def insert_book(self, book_name: str, book_link: str) -> None:
        formalized_book_name = unicodedata.normalize('NFKD', book_name).encode('ascii', 'ignore').decode('utf-8').lower()
        if formalized_book_name not in self.books_index:
            self.books_index[formalized_book_name] = book_link

    def search_levenshtein(self, query: str, nb_result: int) -> list:
        query = unicodedata.normalize('NFKD', query).encode('ascii', 'ignore').decode('utf-8').lower()

        results = []
        for title in self.books_index:
            dist = levenshtein_distance(query, title)
            max_len = max(len(query), len(title))
            results.append((dist/max_len, title))
        closest = sorted(results)[:nb_result]
        print(closest)
        return [(title, self.books_index[title]) for (_ , title) in closest]

