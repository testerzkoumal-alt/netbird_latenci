import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

memory_db = {}
# Nová proměnná pro příkaz
measure_trigger = False 

RIGS = {
    "rig_1": {"name": "Super Gaming Rig 1", "specs": "RTX 3060 12GB", "price": 40},
    "rig_2": {"name": "High-End Beast", "specs": "RTX 4080 16GB", "price": 80},
}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        rows += f"<tr><td>{info['name']}</td><td>{info['specs']}</td><td>{data.get('ms', '--')} ms</td></tr>"
    
    return f"""
    <html>
        <head><meta http-equiv='refresh' content='3'></head>
        <body>
            <h1>Rig Dashboard</h1>
            <table border='1'>{rows}</table>
            <br>
            <form action="/trigger" method="post">
                <button type="submit" style="padding: 10px; background: orange;">VYŽÁDAT MĚŘENÍ (On-demand)</button>
            </form>
        </body>
    </html>
    """

@app.post("/trigger")
async def trigger_measure():
    global measure_trigger
    measure_trigger = True # Aktivujeme příkaz pro klienta
    return HTMLResponse("Příkaz odeslán. <a href='/'>Zpět</a>")

@app.get("/check-tasks")
async def check_tasks():
    global measure_trigger
    status = measure_trigger
    measure_trigger = False # Resetujeme příkaz, aby se neměřilo do nekonečna
    return {"should_measure": status}

@app.post("/update")
async def update(data: dict):
    memory_db[data['rig_id']] = {"ms": data['ms'], "p2p": data['p2p']}
    return {"status": "ok"}
