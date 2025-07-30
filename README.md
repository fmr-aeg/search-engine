# search-engine
```bash
pip install -r requirements.txt
```


## launch autocompletion api
```bash
uvicorn src.autocompletion_feature.api_main:app
```

## Launch search api 
```bash
uvicorn src.search_feature.api_main:app --port 8050
```