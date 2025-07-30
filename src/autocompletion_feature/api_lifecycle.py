from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.autocompletion_feature.keyword_tree import KeywordTree


class APILifecycleAutoCompletion(FastAPI):
    @staticmethod
    def _mock_insert_data(keyword_tree: KeywordTree):
        import pandas as pd
        df = pd.read_csv('data/gutenberg_metadata.csv')
        df.apply(lambda row: keyword_tree.insert(row['Title']), axis=1)

    def startup(self):
        keyword_tree = KeywordTree()
        self._mock_insert_data(keyword_tree)

        return keyword_tree

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        app.state.keyword_tree = self.startup()

        yield

        del app.state.keyword_tree
