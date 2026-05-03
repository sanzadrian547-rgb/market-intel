import json, re, sys, os, urllib.request, urllib.error

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
today = os.environ.get("TODAY", "2026-05-03")

payload = {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 3000,
    "messages": [{
        "role": "user",
        "content": "Eres analista financiero senior. Devuelve SOLO JSON sin texto extra ni backticks. Formato: {\"fecha\":\"hoy\",\"generado\":\"" + today + "\",\"sentimiento\":\"mixto\",\"nivel_riesgo\":\"Medio\",\"resumen\":\"resumen del mercado hoy\",\"patron\":\"patron macro\",\"noticias\":[{\"titular\":\"titular\",\"explicacion\":\"explicacion\",\"impacto\":\"Alcista\",\"activo\":\"SP500\",\"alerta\":false}],\"acciones\":[{\"sector\":\"Tech\",\"accion\":\"MANTENER\",\"confianza\":\"Alto\",\"horizonte\":\"medio\",\"motivo\":\"motivo\"}],\"oportunidades\":[\"op1\"],\"riesgos\":[\"r1\"],\"priorizar\":[\"Tech\"],\"evitar\":[\"Bonos\"],\"senales_vigilar\":[\"s1\"]}"
    }]
}

data = json.dumps(payload).encode("utf-8")

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=data,
    headers={
        "anthropic-version": "2023-06-01",
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read())
    sys.exit(1)

text = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
match = re.search(r"\{[\s\S]*\}", text)
if not match:
    print("No JSON found:", text[:300])
    sys.exit(1)

parsed = json.loads(match.group(0))
os.makedirs("docs", exist_ok=True)
with open("docs/briefing.json", "w", encoding="utf-8") as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)

print("OK:", parsed.get("generado"))
