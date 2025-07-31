# 🔍 Search Engine

A modular search engine featuring autocomplete, regex search, Levenshtein distance, and semantic embedding search.

## 🏗️ Architecture

The global architecture is illustrated in `global_architecture.excalidraw`.  
To view it, install the IDE extension or open the file on the website [Excalidraw](https://excalidraw.com) (it's free).

---

## 🎥 Demo


---

## ⚙️ Installation & Run

Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
````

run autocompletion api in one terminal :
```bash
uvicorn src.autocompletion_feature.api_main:app
```

run search api in another one: 
```bash
uvicorn src.search_feature.api_main:app --port 8050
```

lastly, open index.html in your browser.

------

## 💡 Example queries
- regex example: "^(?=\S+\s+\S+\s+\S+$)(?=.*\b\w*\d\w*\b).*$"
- search example: "sins saint"
- embedding example: "Pirates Fantomes"

## ✨ Key Features

- ✅ Smart autocomplete
- ✅ Regex-based search 
- ✅ Levenshtein distance search 
- ✅ Semantic search via embeddings

## 🚀 Try It Out
Built with ❤️ by fmr-aeg


