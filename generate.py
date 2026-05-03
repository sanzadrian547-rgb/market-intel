import json, re, sys, os, urllib.request

api_key = os.environ.get('ANTHROPIC_API_KEY', '')
today = os.environ.get('TODAY', '2026-05-03')

data = json.dumps({
    "model": "claude-haiku-4-5-20251001
",
    "max_tokens": 3000,
    "messages": [{
        "role": "user",
        "content": f"Hoy es {today}. Eres analista financiero senior. Analiza las noticias mas importantes de hoy y devuelve SOLO un JSON valido con este formato exacto sin backticks: {{\"fecha\":\"{today}\",\"generado\":\"{today}\",\"sentimiento\":\"mixto\",\"nivel_riesgo\":\"Medio\",\"resumen\":\"string\",\"patron\":\"string\",\"noticias\":[{{\"titular\":\"string\",\"explicacion\":\"string\",\"impacto\":\"Alcista\",\"activo\":\"string\",\"alerta\":false}}],\"acciones\":[{{\"sector\":\"string\",\"accion\":\"MANTENER\",\"confianza\":\"Alto\",\"horizonte\":\"medio\",\"motivo\":\"string\"}}],\"oportunidades\":[\"string\"],\"riesgos\":[\"string\"],\"priorizar\":[\"string\"],\"evitar\":[\"string\"],\"senales_vigilar\":[\"string\"]}}"
    }]
}).encode()

req = urllib.request.Request(
    'https://api.anthropic.com/v1/messages',
    data=data,
    headers={
        'anthropic-version': '2023-06-01',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
)

with urllib.request.urlopen(req) as r:
    resp = json.loads(r.read())

text = ''.join(b.get('text','') for b in resp.get('content',[]) if b.get('type')=='text')
match = re.search(r'\{[\s\S]*\}', text)
if not match:
    print("No JSON:", text[:300])
    sys.exit(1)

parsed = json.loads(match.group(0))
os.makedirs('docs', exist_ok=True)
with open('docs/briefing.json', 'w', encoding='utf-8') as f:
    json.dump(parsed, f, ensure_ascii=False, indent=2)
print("OK:", parsed.get('generado'))
