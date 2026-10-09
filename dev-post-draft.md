# Touch Grass: an open-source AI agent that plans your way outside 🌿

*My submission for the Hacktoberfest Open-Source AI Challenge: Week 1 — "Touch Grass".
Tags: #devchallenge #hf26challenge*

The prompt was simple: build something with open-source AI at its core that gets
people off the screen and into the world. So I built the smallest agent I could
that does exactly that — you tell it where you are and how much time you have,
and it plans a real outdoor micro-adventure: when to go, where to stand, what to
look for, and what to do with your phone (spoiler: airplane mode).

## What I built

**Touch Grass** is a tiny Python agent (~200 lines, one dependency). It runs a
tool-using loop over any OpenAI-compatible chat endpoint:

- **Tools**: geocoding (OpenStreetMap), sunrise/sunset times, and a 12-hour
  weather outlook (Open-Meteo) — all free, keyless, open data.
- **Brain**: any open-weight model behind an OpenAI-compatible API. The agent
  supports local Ollama for fully offline inference, or a hosted gateway.
  For this demo I ran it against a hosted open-weight model served over an
  OpenAI-compatible endpoint; swapping models is one environment variable.
- **Output**: a concrete Markdown plan — time window, spot, timed steps,
  things to notice, a phone rule, and a rain check.

No frameworks, no vendor SDKs. The whole thing is `requests` + a loop.

## Demo

Real run, tonight, no cherry-picking — asked for a 45-minute sunset walk with
birding near Olympic Forest Park, Beijing:

> ## Lakeside Light & Last Calls — Aohai, Olympic Forest Park
> - **When:** 17:05 → 17:50. Sunset is 17:46, so this window catches warm
>   pre-sunset light and ends in the afterglow. Overcast, 21°C, 0% precipitation
>   across the next 12 hours — dry and calm. Honest caveat: overcast may swallow
>   the sun disc itself. That's fine — it's actually *better* for birds.
> - **Where:** the east shore of Aohai lake, looking west across the water.
>   Enter at the south gate, 8 minutes' walk to the shoreline.
> - **The plan:** timed steps from gate to shoreline birding (17:10–17:28),
>   then 5 minutes north to a west-facing photo gap, shooting the afterglow
>   5–10 minutes *after* official sunset.
> - **Look for:** grey herons and great egrets in the shallows, little grebes
>   and coots on open water, azure-winged magpies in the treeline, the lake
>   going two-tone in the wind, early-October migrants in the willows.
> - **Leave the phone:** airplane mode in your pocket until 17:44 — the camera
>   is the only phone use, and it starts when the light does.
> - **Rain check:** not needed today. If the sky fully greys out, drop the
>   sunset shot and walk the wetland boardwalk instead.

What I like about this output: the agent actually *used* its tools. It
geocoded the park, pulled real sunset/weather data, and reasoned about it —
noticing that overcast hurts the sunset photo but helps the birding, and
adjusting the plan accordingly. That's the agent earning its keep, not just
filling a template.

## Why open innovation matters here

This project only makes sense because it's open, in three concrete ways:

1. **It can go where the trail goes.** A closed API means the agent dies the
   moment you lose signal. Open weights mean the same agent runs on a laptop
   with Ollama, fully offline — which is exactly where a "touch grass" tool
   needs to work.
2. **Your location stays yours.** The agent's most sensitive input is where
   you are and when. With open models and open data sources, none of that has
   to travel to a server you don't control.
3. **It costs nothing to run and anyone can improve it.** The model is
   swappable, the data sources are free, the code is ~200 lines of MIT-licensed
   Python. A student, a hiking club, or a park ranger can fork it, point it at
   a newer open model next year, and it's better — no permission, no bill.

Closed models could generate the same *words*. They couldn't give you the same
*guarantees*. For a tool whose whole job is getting you outside, offline and
private aren't features — they're the point.

## Try it

```bash
pip install -r requirements.txt
export OPENAI_BASE_URL=http://localhost:11434/v1  # or any OpenAI-compatible endpoint
export OPENAI_MODEL=qwen2.5:3b
python -m touchgrass.cli --place "your park here" --minutes 45 \
    --interests "birding, sunset photos"
```

Repo: [link to GitHub repo]
I validated the plan logic against real data tonight; the agent geocoded,
checked sunset and weather, and reasoned over them rather than filling a
template.

## Prize Categories

- Overall
