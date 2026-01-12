import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis

app = FastAPI()

# Pro POC: Pokud nemáš Redis, data budou jen v paměti (po restartu zmizí)
# Pro produkci sem pak dáš údaje z Redis Cloud
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

RIGS = {
    "rig_1": {"name": "Super Gaming Rig 1", "specs": "RTX 3060 12GB", "price": 40},
    "rig_2": {"name": "High-End Beast", "specs": "RTX 4080 16GB", "price": 80},
}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        try:
            latency = r.get(f"lat:{r_id}") or "--"
            p2p = r.get(f"type:{r_id}") or "Unknown"
        except: latency, p2p = "N/A (No Redis)", "N/A"
        
        rows += f"<tr><td>{info['name']}</td><td>{info['specs']}</td><td>{latency} ms</td><td>{p2p}</td><td>{info['price']}</td></tr>"
    
    return f"<html><body><h1>Rig Dashboard</h1><table border='1'><tr><th>Název</th><th>Specs</th><th>Latence</th><th>Typ</th><th>Kredity</th></tr>{rows}</table></body></html>"

@app.post("/update")
async def update(data: dict):
    try:
        r.set(f"lat:{data['rig_id']}", data['ms'], ex=60)
        r.set(f"type:{data['rig_id']}", data['p2p'], ex=60)
    except: pass # Pro POC bez redisu to prostě projde
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn
    # Cloud Run si port určuje sám přes proměnnou prostředí
    port = int(os.environ.get('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)