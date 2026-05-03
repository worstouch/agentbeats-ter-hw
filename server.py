"""
A2A Server for Terminal Bench 2.0 Purple Agent.

Uses ADK's to_a2a() to automatically convert the OpenSageAgent
into a fully functional A2A server — no manual executor, messenger,
or message parsing needed.
"""

import argparse
import logging

from dotenv import load_dotenv
load_dotenv()

import json
import litellm
import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agent import mk_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("terminal_bench_server")


import re
import litellm
_orig_acompletion = litellm.acompletion

def _fix_multiline_json(text: str) -> str:
    """Fix JSON where string values contain literal newlines (should be \\n)."""
    # Replace literal newlines inside JSON string values with \\n
    # Strategy: find the JSON object boundaries, then fix newlines inside strings
    lines = text.split("\n")
    if len(lines) <= 1:
        return text
    # Join all lines, escaping newlines that appear inside string values
    fixed = "\\n".join(lines)
    return fixed

def _extract_json(text: str) -> str:
    """Extract the first valid JSON object from text that may contain natural language."""
    if not text:
        return text
    # Try parsing as-is first
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass
    # Try fixing multi-line JSON (LLM put real newlines in command field)
    fixed = _fix_multiline_json(text)
    try:
        json.loads(fixed)
        return fixed
    except json.JSONDecodeError:
        pass
    # Find the first { and try to extract JSON from there
    idx = text.find("{")
    if idx == -1:
        return text
    candidate = text[idx:]
    # Find matching closing brace
    depth = 0
    for i, ch in enumerate(candidate):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                extracted = candidate[:i+1]
                try:
                    json.loads(extracted)
                    return extracted
                except json.JSONDecodeError:
                    pass
                # Try fixing multiline in extracted portion
                fixed_extracted = _fix_multiline_json(extracted)
                try:
                    json.loads(fixed_extracted)
                    return fixed_extracted
                except json.JSONDecodeError:
                    pass
                break
    return text

async def _patched_acompletion(*args, **kwargs):
    result = await _orig_acompletion(*args, **kwargs)
    try:
        original = result.choices[0].message.content
        cleaned = _extract_json(original)
        if cleaned != original:
            logger.info("Cleaned LLM response: stripped non-JSON text")
        result.choices[0].message.content = cleaned
    except Exception:
        pass
    return result
litellm.acompletion = _patched_acompletion


def main():
    parser = argparse.ArgumentParser(description="Run the terminal-bench purple agent.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=9019, help="Port to bind")
    args = parser.parse_args()

    agent = mk_agent()
    app = to_a2a(agent, host=args.host, port=args.port)

    logger.info(f"Starting terminal-bench purple agent on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
