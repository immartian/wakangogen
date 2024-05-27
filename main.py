import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

# MongoDB connection
from dotenv import load_dotenv
load_dotenv()

connection_string = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(connection_string)
db = client.get_database("lingo")
terms_collection = db.get_collection("terms")

app = FastAPI()
# mount static foder
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Term(BaseModel):
    term: str
    etymology: str
    jp: str
    en: str
    taxonomy: List[str]
    related: List[str]

class Link(BaseModel):
    source: str
    target: str
    value: int

# serve the index.html from /static as a template
@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/nodes", response_model=List[dict])
async def get_nodes():
    terms = list(terms_collection.find())
    nodes = [{"id": term["term"], "jp": term["jp"], "en": term["en"], "group": term["taxonomy"][0].lower(), "etymology": term["etymology"]} for term in terms]
    return nodes

@app.get("/links", response_model=List[dict])
async def get_links():
    terms = list(terms_collection.find())
    links = []
    for term in terms:
        for related_term in term["related"]:
            links.append({"source": term["term"], "target": related_term, "value": 1})
    return links

@app.post("/add_term", response_model=dict)
async def add_term(term: Term):
    term_dict = term.dict()
    if terms_collection.find_one({"term": term.term}):
        raise HTTPException(status_code=400, detail="Term already exists")
    result = terms_collection.insert_one(term_dict)
    return {"id": str(result.inserted_id)}

@app.delete("/delete_term/{term_id}", response_model=dict)
async def delete_term(term_id: str):
    result = terms_collection.delete_one({"_id": ObjectId(term_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"status": "deleted"}

@app.get("/terms", response_model=List[Term])
async def get_all_terms():
    terms = list(terms_collection.find())
    return terms

@app.get("/links_data", response_model=List[Link])
async def get_all_links():
    terms = list(terms_collection.find())
    links = []
    for term in terms:
        for related_term in term["related"]:
            links.append({"source": term["term"], "target": related_term, "value": 1})
    return links

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
