# Sloth AI Agent API

Python FastAPI service for the three Gemini agent actions from `ai-agent.ts`.

## Setting

```bash
sudo cp sloth-api.service /etc/systemd/system/sloth-api.service
sudo systemctl daemon-reload
sudo systemctl enable --now sloth-api.service
sudo systemctl status sloth-api.service
```

## Run

```bash
python3 -m pip install -r requirements.txt
export GEMINI_API_KEY="your-api-key"
python3 main.py
```

The service starts on `http://localhost:8000`.

## CORS

The API enables CORS for browser and mini app calls by default. Current config
allows any origin and does not enable credentialed cookie requests. If the
frontend needs cookies or login sessions, replace `allow_origins=["*"]` in
`main.py` with the exact production domains.

## Endpoints

All POST endpoints accept:

```json
{
  "contents": "user goals or task text"
}
```

- `GET /health` returns `{"status": "ok"}`
- `POST /suggest` returns `string[]`
- `POST /write` returns `string[7]`
- `POST /todo` returns `{ "name": string, "value": number, "todos": string[] }[]`
