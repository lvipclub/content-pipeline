#!/usr/bin/env python3
"""STEP 1 — FAL edit-route retest: invoke the exact image_generate code path
(image_generate_tool) with the bro-woo clean reference (identity lock)."""
import sys, json

sys.path.insert(0, "/Users/marcsir/.hermes/hermes-agent")

from tools.image_generation_tool import image_generate_tool

PROMPT = (
    "Clean duo character reference: Bro Woo (spiky black hair, glasses, grey "
    "V-neck over white collared shirt, pointer) and Inu Faa (slim Shiba, "
    "tan/white, yellow collar with orange lightning bolt charm), flat vector, "
    "black line art, pure white background, landscape 16:9, characters only, "
    "no text, no whiteboard, no footer"
)
REF = "/Users/marcsir/workspace/content-pipeline/.ip-assets/characters/bro-woo/character-reference-clean.png"

print("calling image_generate_tool (edit route via managed FAL gateway)...", flush=True)
try:
    raw = image_generate_tool(
        prompt=PROMPT,
        aspect_ratio="landscape",
        reference_image_urls=[REF],
    )
    print("RAW_RESULT_START", flush=True)
    print(raw, flush=True)
    print("RAW_RESULT_END", flush=True)
    try:
        parsed = json.loads(raw)
        print("SUCCESS_FLAG:", parsed.get("success"), flush=True)
        print("IMAGE_URL:", parsed.get("image"), flush=True)
        if not parsed.get("success"):
            print("ERROR:", parsed.get("error"), flush=True)
    except Exception as e:
        print("JSON_PARSE_FAIL:", e, flush=True)
except Exception as exc:
    print("CALL_RAISED:", type(exc).__name__, str(exc), flush=True)
    sys.exit(1)
