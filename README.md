# Touch Grass 🌿

An open-source AI micro-adventure planner that gets you off the screen and into
the world. Built for the Hacktoberfest 2026 DEV Challenge — Week 1: *Touch Grass*.

Give it a place and a time budget; it plans a concrete outdoor micro-adventure:
best time window, a spot, timed steps, things to notice outside, and a rain check.
It grounds every plan in real data — geocoding, sunrise/sunset, and weather —
through a small agentic tool loop.

## How it works

```
you ──▶ CLI ──▶ agent loop ──▶ open-weight model (OpenAI-compatible endpoint)
                        │        ▲  ▲
                        │   tools: geocode · sun_times · weather
                        ▼
                   Markdown plan
```

- **Model-agnostic**: talks to any OpenAI-compatible chat endpoint. Point it at
  local Ollama for fully offline inference, or any gateway serving open-weight
  models. No vendor SDK, just `requests`.
- **Open data**: OpenStreetMap Nominatim, sunrise-sunset.org, Open-Meteo —
  all free, no API keys.
- **Small on purpose**: ~200 lines. The screen is the shortest part of the
  experience — the plan is.

## Quickstart

```bash
pip install -r requirements.txt

# Option A: local, fully offline-capable (needs Ollama running)
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_MODEL=qwen2.5:3b
python -m touchgrass.cli --place "Olympic Forest Park, Beijing" \
    --minutes 45 --interests "sunset photos, birding"

# Option B: any OpenAI-compatible gateway serving open-weight models
export OPENAI_BASE_URL=https://your-gateway/v1
export OPENAI_API_KEY=...
export OPENAI_MODEL=...
python -m touchgrass.cli --place "Central Park, New York" --minutes 60
```

See `examples/sample-plan.md` for a real run.

## Why open

Closed models would work for the text, but openness is the point: the same
agent runs against a model on your own laptop with no internet (handy on a
trail with no signal), sends your location to nobody, costs nothing per run,
and lets you swap models as open weights improve. Open data sources mean the
whole thing is reproducible by anyone, anywhere.

## License

MIT
