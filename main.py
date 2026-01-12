import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# Dočasná paměť přímo v RAM serveru
memory_db = {}
measure_trigger = False 

# Definice našich Rigů
RIGS = {
    "jakub-103-243": {"specs": "RTX 3060 12GB", "price": 40},
    "apponfly-gaming-2": {"specs": "RTX 4080 16GB", "price": 80},
}

class LatencyData(BaseModel):
    rig_id: str
    ms: int
    p2p: str

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # Sestavení řádků tabulky
    table_rows = ""
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        latency = data.get("ms", "--")
        conn_type = data.get("p2p", "Unknown")
        
        # Určení barvy podle typu spojení
        color = "#4CAF50" if conn_type == "P2P" else "#FF9800" if "Relay" in conn_type else "#757575"
        
        table_rows += f"""
        <tr>
            <td><strong>{r_id}</strong></td>
            <td>{info['specs']}</td>
            <td style="text-align:center">{latency} ms</td>
            <td style="color:{color}; font-weight:bold">{conn_type}</td>
            <td>{info['price']} kr/h</td>
        </tr>
        """

    # Finální HTML rozdělené tak, aby Python nedělal chyby v uvozovkách
    html_template = """
    <html>
        <head>
            <title>Netbird P2P Monitor</title>
            <meta http-equiv="refresh" content="3">
            <style>
                body { font-family: sans-serif; margin: 40px; background: #f4f7f6; }
                table { border-collapse: collapse; width: 100%; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: left; }
                th { background-color: #2c3e50; color: white; }
                .btn { padding: 15px 25px; background: #e67e22; color: white; border: none; 
                         border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
                .btn:hover { background: #d35400; }
            </style>
        </head>
        <body>
            <h1>Rig Latency Dashboard (Netbird POC)</h1>
            <table>
                <thead>
                    <tr>
                        <th>Název (FQDN)</th>
                        <th>Specifikace</th>
                        <th>Latence</th>
                        <th>Typ spojení</th>
                        <th>Cena</th>
                    </tr>
                </thead>
                <tbody>
                    REPLACE_WITH_ROWS
                </tbody>
            </table>
            <br>
            <form action="/trigger" method="post">
                <button type="submit" class="btn">VYŽÁDAT AKTUÁLNÍ MĚŘENÍ</button>
            </form>
            <p><small>Dashboard se obnovuje každé 3s. Klient v Praze kontroluje úkoly každé 2s.</small></p>
        </body>
    </html>
    """
    
    final_html = html_template.replace("REPLACE_WITH_ROWS", table_rows)
    return HTMLResponse(content=final_html)

@app.post("/trigger")
async def trigger_measure():
    global measure_trigger
    measure_trigger = True
    return RedirectResponse(url="/", status_code=303)

@app.get("/check-tasks")
async def check_tasks():
    global measure_trigger
    status = measure_trigger
    measure_trigger = False 
    return {"should_measure": status}

@app.post("/update")
async def update(data: LatencyData):
    memory_db[data.rig_id] = {
        "ms": data.ms,
        "p2p": data.p2p
    }
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
