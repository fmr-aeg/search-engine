from fastapi import FastAPI, status
from src.autocompletion_feature.keyword_tree import KeywordTree
from pydantic import BaseModel
from src.autocompletion_feature.api_lifecycle import APILifecycleAutoCompletion
from loguru import logger

class Words(BaseModel):
    words: list[str]

lifecycle = APILifecycleAutoCompletion()

app = FastAPI(
    title="AutoCompletion API",
    version="1.0",
    description="AutoCompletion API that will autocomplete any suffix keyword",
    lifespan=lifecycle.lifespan,
)


@app.get("/autocomplete")
def search(prefix: str):
    logger.debug(f'call prefix: {prefix}')
    return app.state.keyword_tree.search(prefix)

@app.post("/insert")
def insert(words: Words):
    for word in words.words:
        app.state.keyword_tree.insert(word)
    return {"message": f"{len(words.words)} words inserted successfully."}

@app.get("/info", status_code=status.HTTP_200_OK)
def model_info():
    return f"children {app.state.keyword_tree} "

