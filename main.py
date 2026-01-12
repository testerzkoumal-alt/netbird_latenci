import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Místo Redisu použijeme dočasnou paměť přímo v aplikaci
fake_db = {}

RIGS = {
    "rig_1": {"name": "Super Gaming Rig 1", "specs": "RTX 3060 12GB", "price": 40},
    "rig_2": {"name": "High-End Beast", "specs": "RTX 4080 16GB", "price": 80},
}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        # Taháme data z naší dočasné paměti
        data = fake_db.get(r_id, {})
        latency = data.get("ms", "--")
        p2p = data.get("p2p", "Unknown")
        
        rows += f"<tr><td>{info['name']}</td><td>{info['specs']}</td><td>{latency} ms</td><td>{p2p}</td><td>{info['price']}</td></tr>"
    
    return f"<html><head><meta http-equiv='refresh' content='5'></head><body><h1>Rig Dashboard</h1><table border='1'><tr><th>Název</th><th>Specs</th><th>Latence</th><th>Typ</th><th>Kredity</th></tr>{rows}</table><p>Stránka se automaticky obnovuje každých 5s.</p></body></html>"

@app.post("/update")
async def update(data: dict):
    # Uložíme přijatá data do naší dočasné paměti
    rig_id = data.get("rig_id")
    fake_db[rig_id] = {
        "ms": data.get("ms"),
        "p2p": data.get("p2p")
    }
    return {"status": "success"}
