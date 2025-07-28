from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.autocompletion_feature.keyword_tree import KeywordTree

l_mock_query = ['One Piece',
'HunterxHunter',
'Naruto',
'Death Note',
'Berserk',
'One punch man']

class APILifecycleAutoCompletion(FastAPI):
    @staticmethod
    def _mock_insert_data(keyword_tree: KeywordTree):
        for query in l_mock_query:
            keyword_tree.insert(query)

    def startup(self):
        keyword_tree = KeywordTree()
        self._mock_insert_data(keyword_tree)

        return keyword_tree

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        app.state.keyword_tree = self.startup()

        yield

        del app.state.keyword_tree
