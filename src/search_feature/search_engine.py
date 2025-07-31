from Levenshtein import distance as levenshtein_distance
import unicodedata
import re
import faiss
from sentence_transformers import SentenceTransformer
import pickle
import torch


class SearchEngine:
    def __init__(self):
        # dic with information on product title -> link
        # In production this dic will contain title -> _id from mongoDB
        self.books_index = {}
        self.index = faiss.read_index("data/mock_data.index")
        self.index_to_title = pickle.load(open('data/mock_index_to_title.pkl', 'rb'))
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def _formalize_title(title: str) -> str:
        return unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode('utf-8').lower()

    def insert_book(self, book_name: str, book_link: str) -> None:
        formalized_book_name = self._formalize_title(book_name)
        if formalized_book_name not in self.books_index:
            self.books_index[formalized_book_name] = book_link

    def search_levenshtein_normalized(self, query: str, nb_result: int) -> list:
        query = self._formalize_title(query)

        results = []
        for title in self.books_index:
            dist = levenshtein_distance(query, title)
            max_len = max(len(query), len(title))
            results.append((dist/max_len, title))
        closest = sorted(results)[:nb_result]
        return [dict(title=title, link=self.books_index[title]) for (_ , title) in closest]

    def search_levenshtein(self, query: str, nb_result: int) -> list:
        query = self._formalize_title(query)

        results = []
        for title in self.books_index:
            dist = levenshtein_distance(query, title)
            results.append((dist, title))
        closest = sorted(results)[:nb_result]
        return [dict(title=title, link=self.books_index[title]) for (_ , title) in closest]

    def search_regex(self, query: str, nb_result: int) -> list:
        pattern = re.compile(query, re.IGNORECASE)
        title_match = [dict(title=title, link=self.books_index[title]) for title in self.books_index if pattern.search(title)]
        return title_match[:nb_result]

    def search_embedding(self, query: str, nb_result: int) -> list:
        vectorized_query = self.model.encode([query]).astype('float32')
        _, indices = self.index.search(vectorized_query, nb_result)
        indices = indices.squeeze()

        titles = [self._formalize_title(self.index_to_title[i]) for i in indices]

        return [dict(title=title, link=self.books_index[title]) for title in titles]

