from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
from src.search_feature.api_lifecycle import APILifecycleSearchEngine

lifecycle = APILifecycleSearchEngine()

app = FastAPI(
    title="Search Engine",
    description="Search Engine with 3 modes",
    version="1.0",
    lifespan=lifecycle.lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(keyword: str,
           search_mode:str = 'levenshtein',
           limit: int = 10):

    logger.debug(f'keyword: {keyword}')
    if search_mode == 'levenshtein':
        response = app.state.search_engine.search_levenshtein_normalized(query=keyword, nb_result=limit)

    if search_mode == 'regex':
        response = app.state.search_engine.search_regex(query=keyword, nb_result=limit)

    if search_mode == 'embedding':
        response = app.state.search_engine.search_embedding(query=keyword, nb_result=limit)

    return response
