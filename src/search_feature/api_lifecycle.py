from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.search_feature.search_engine import SearchEngine


class APILifecycleSearchEngine(FastAPI):
    @staticmethod
    def _mock_insert_data(search_engine: SearchEngine):
        import pandas as pd
        df = pd.read_csv('data/gutenberg_metadata.csv')
        df.apply(lambda row: search_engine.insert_book(row['Title'], row['Link']), axis=1)

    def startup(self):
        search_engine = SearchEngine()
        self._mock_insert_data(search_engine)

        return search_engine

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        app.state.search_engine = self.startup()

        yield

        del app.state.search_engine
