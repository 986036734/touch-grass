#!/usr/bin/env python3
"""Touch Grass CLI — plan a micro-adventure that gets you outside.

Env:
  OPENAI_BASE_URL  OpenAI-compatible endpoint (default: http://localhost:11434/v1)
  OPENAI_API_KEY   key for the endpoint (default: empty; Ollama needs none)
  OPENAI_MODEL     model name (default: qwen2.5:3b)

Example:
  OPENAI_BASE_URL=https://your-gateway/v1 OPENAI_API_KEY=... OPENAI_MODEL=... \
      python -m touchgrass.cli --place "Olympic Forest Park, Beijing" --minutes 45 \
      --interests "birding, sunset photos"
"""
import argparse
import sys

from .agent import plan


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Plan an outdoor micro-adventure.")
    ap.add_argument("--place", required=True, help="where you are / want to go")
    ap.add_argument("--minutes", type=int, default=45, help="time available")
    ap.add_argument("--interests", default="", help="e.g. 'birding, running'")
    ap.add_argument("--out", default="", help="write plan Markdown to this file")
    args = ap.parse_args(argv)

    text = plan(args.place, args.minutes, args.interests)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
