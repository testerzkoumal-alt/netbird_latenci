import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

app = FastAPI()

# Dočasná paměť přímo v RAM serveru (po restartu Renderu se vymaže)
memory_db = {}
# Proměnná, která drží informaci, zda někdo klikl na tlačítko "Měřit"
measure_trigger = False 

# Definice našich Rigů (v reálné appce by bylo v DB)
RIGS = {
    "jakub-103-243": {"specs": "RTX 3060 12GB", "price": 40},
    "apponfly-gaming-2": {"specs": "RTX 4080 16GB", "price": 80},
}

# Model pro příchozí data z klienta
class LatencyData(BaseModel):
    rig_id: str
    ms: int
    p2p: str

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    rows = ""
    # Procházíme rigy a doplňujeme k nim naměřená data z paměti
    for r_id, info in RIGS.items():
        data = memory_db.get(r_id, {})
        latency = data.get("ms", "--")
        conn_type = data.get("p2p", "Unknown")
        
        # Barva pro typ spojení
        color = "#4CAF50" if conn_type == "P2P" else "#FF9800" if conn_type == "Relayed" else "#757575"
        
        rows += f"""
        <tr>
            <td><strong>{r_id}</strong></td>
            <td>{info['specs']}</td>
            <td style="text-align:center">{latency} ms</td>
            <td style="color:{color}; font-weight:bold">{conn_type}</td>
            <td>{info['price']} kr/h</td>
        </tr>
        """
    
    return f"""
    <html>
        <head>
            <title>Netbird P2P Monitor</title>
            <meta http-equiv='refresh' content='3'>
            <style>
                body {{ font-family: sans-serif; margin: 40px; background: #f4f7f6; }}
                table {{ border-collapse: collapse; width: 10
