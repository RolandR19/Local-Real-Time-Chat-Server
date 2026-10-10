"""
Chat local : le PC héberge, les téléphones ouvrent la page dans Safari.
Installation :  pip install aiohttp
Lancement    :  python chat_server.py
"""
import socket
from aiohttp import web, WSMsgType

PORT = 8000
clients = set()

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Chat local</title>
<style>
  html, body { height: 100%; margin: 0; font-family: -apple-system, Segoe UI, sans-serif; }
  body { display: flex; flex-direction: column; background: #f2f2f7; }
  #log { flex: 1; overflow-y: auto; padding: 12px; }
  .msg { background: #fff; border-radius: 14px; padding: 8px 12px; margin: 6px 0; max-width: 85%; word-wrap: break-word; }
  .moi { background: #0a84ff; color: #fff; margin-left: auto; }
  .nom { font-size: 11px; opacity: .65; }
  #bar { display: flex; gap: 8px; padding: 10px; padding-bottom: calc(10px + env(safe-area-inset-bottom)); background: #fff; }
  input { flex: 1; font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 10px; }
  button { font-size: 16px; padding: 10px 16px; border: 0; border-radius: 10px; background: #0a84ff; color: #fff; }
</style>
</head>
<body>
  <div id="log"></div>
  <div id="bar">
    <input id="txt" placeholder="Message" autocomplete="off">
    <button id="btn">Envoyer</button>
  </div>
<script>
  const nom = (prompt("Ton prénom :") || "Anonyme").trim();
  const log = document.getElementById("log");
  const txt = document.getElementById("txt");
  const ws = new WebSocket("ws://" + location.host + "/ws");

  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    const div = document.createElement("div");
    div.className = "msg" + (m.nom === nom ? " moi" : "");
    const n = document.createElement("div");
    n.className = "nom"; n.textContent = m.nom;
    const t = document.createElement("div");
    t.textContent = m.texte;
    div.append(n, t);
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  };

  function envoyer() {
    const texte = txt.value.trim();
    if (!texte || ws.readyState !== 1) return;
    ws.send(JSON.stringify({ nom: nom, texte: texte }));
    txt.value = "";
  }
  document.getElementById("btn").onclick = envoyer;
  txt.addEventListener("keydown", (e) => { if (e.key === "Enter") envoyer(); });
</script>
</body>
</html>"""


async def index(request):
    return web.Response(text=HTML, content_type="text/html")


async def ws_handler(request):
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    clients.add(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                for c in list(clients):
                    if not c.closed:
                        await c.send_str(msg.data)
    finally:
        clients.discard(ws)
    return ws


def adresses_locales():
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except socket.gaierror:
        pass
    return sorted(ips)


if __name__ == "__main__":
    print("\n=== Chat local démarré ===")
    print(f"Sur ce PC          : http://localhost:{PORT}")
    for ip in adresses_locales():
        print(f"Sur les téléphones : http://{ip}:{PORT}")
    print("(Ctrl+C pour arrêter)\n")

    app = web.Application()
    app.add_routes([web.get("/", index), web.get("/ws", ws_handler)])
    web.run_app(app, host="0.0.0.0", port=PORT, print=None)
