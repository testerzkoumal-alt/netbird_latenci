import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Dočasná paměť v RAM serveru
memory_db = {}

RIGS = {
    "rig_1": {"name": "Super Gaming Rig 1", "specs": "RTX 3060 12GB", "price": 40},
    "rig_2": {"name": "High-End Beast", "specs": "RTX 4080 16GB", "price": 80},
}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        latency = data.get("ms", "--")
        p2p = data.get("p2p", "Unknown")
        rows += f"<tr><td>{info['name']}</td><td>{info['specs']}</td><td>{latency} ms</td><td>{p2p}</td><td>{info['price']}</td></tr>"
    
    return f"<html><head><meta http-equiv='refresh' content='5'></head><body><h1>Rig Dashboard</h1><table border='1'><tr><th>Název</th><th>Specs</th><th>Latence</th><th>Typ</th><th>Kredity</th></tr>{rows}</table></body></html>"

@app.post("/update")
async def update(data: dict):
    rig_id = data.get("rig_id")
    if rig_id:
        memory_db[rig_id] = {"ms": data.get("ms"), "p2p": data.get("p2p")}
    return {"status": "ok"}
