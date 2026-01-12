import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Dočasná paměť přímo v RAM serveru
memory_db = {}
measure_trigger = False 

RIGS = {
    "rig_1": {"name": "Super Gaming Rig 1", "specs": "RTX 3060 12GB", "price": 40},
    "rig_2": {"name": "High-End Beast", "specs": "RTX 4080 16GB", "price": 80},
}

class LatencyData(BaseModel):
    rig_id: str
    ms: int
    p2p: str

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        rows += f"<tr><td>{info['name']}</td><td>{info['specs']}</td><td>{data.get('ms', '--')} ms</td><td>{data.get('p2p', '--')}</td><td>{info['price']}</td></tr>"
    
    return f"""
    <html>
        <head><meta http-equiv='refresh' content='3'></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h1>Rig Dashboard (On-demand POC)</h1>
            <table border='1' cellpadding="10">
                <tr><th>Název</th><th>Specs</th><th>Latence</th><th>Typ</th><th>Kredity</th></tr>
                {rows}
            </table>
            <br>
            <form action="/trigger" method="post">
                <button type="submit" style="padding: 15px; background: orange; border: none; cursor: pointer; font-weight: bold;">
                    VYŽÁDAT MĚŘENÍ OD KLIENTA
                </button>
            </form>
            <p><small>Stránka se obnovuje každé 3s. Klient kontroluje úkoly každé 2s.</small></p>
        </body>
    </html>
    """

@app.post("/trigger")
async def trigger_measure():
    global measure_trigger
    measure_trigger = True
    return HTMLResponse("Příkaz odeslán klientovi. <a href='/'>Zpět na dashboard</a>")

@app.get("/check-tasks")
async def check_tasks():
    global measure_trigger
    status = measure_trigger
    measure_trigger = False 
    return {"should_measure": status}

@app.post("/update")
async def update(data: LatencyData):
    memory_db[data.rig_id] = {"ms": data.ms, "p2p": data.p2p}
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
