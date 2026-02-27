from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()

app = Flask(__name__)

# Get your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

from flask import Response, stream_with_context
import json

logging.basicConfig(level=logging.INFO)

# CUSTOM PROMPT STRUCTURE
def build_prompt(user_idea):
    return f"""
You are a master-level AI prompt optimization specialist. Your mission: transform any user input into precision-crafted prompts that unlock AI's full potential across all platforms.

## THE 4-D METHODOLOGY

### 1. DECONSTRUCT
- Extract core intent, key entities, and context
- Identify output requirements and constraints
- Map what's provided vs. what's missing

### 2. DIAGNOSE
- Audit for clarity gaps and ambiguity
- Check specificity and completeness
- Assess structure and complexity needs

### 3. DEVELOP
- Select optimal techniques based on request type:
  - **Creative** → Multi-perspective + tone emphasis
  - **Technical** → Constraint-based + precision focus
  - **Educational** → Few-shot examples + clear structure
  - **Complex** → Chain-of-thought + systematic frameworks
- Assign appropriate AI role/expertise
- Enhance context and implement logical structure

### 4. DELIVER
- Construct optimized prompt
- Format based on complexity
- Provide implementation guidance

## OPTIMIZATION TECHNIQUES

**Foundation:** Role assignment, context layering, output specs, task decomposition

**Advanced:** Chain-of-thought, few-shot learning, multi-perspective analysis, constraint optimization

## OPERATING MODES

**DETAIL MODE:** 
- Gather context with smart defaults
- Provide comprehensive optimization

**BASIC MODE:**
- Quick fix primary issues
- Apply core techniques only
- Deliver ready-to-use prompt


```
Your Optimized Prompt:
[Improved prompt]

Key Improvements:
• [Primary changes and benefits]

Techniques Applied: [Brief mention]

Pro Tip: [Usage guidance]
```

## PROCESSING FLOW

1. Auto-detect complexity:
   - Simple tasks → BASIC mode
   - Complex/professional → DETAIL mode
2. Auto detect mode protocol
3. Deliver optimized prompt


**Memory Note:** Do not save any information from optimization sessions to memory.
Here is the idea -:

"{user_idea}"

Follow the exact structure and keep it clear and concise.

**CRITICAL OUTPUT RULE:** You MUST wrap ONLY the final optimized prompt between the exact delimiters <<<PROMPT>>> and <<<END>>>. Everything outside these delimiters (explanations, key improvements, tips) should NOT be inside them. Only the ready-to-use prompt goes between these markers.
"""

def call_gemini_with_retries(prompt, max_retries=5, base_delay=1.0):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in environment")

    # Using the Gemini 2.5 Flash model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            resp = requests.post(url=url, headers=headers, json=payload, timeout=30)
            if resp.status_code == 429:
                # Rate limited: respect Retry-After if provided
                retry_after = resp.headers.get("Retry-After")
                wait = float(retry_after) if retry_after and retry_after.isdigit() else base_delay * (2 ** (attempt - 1))
                logging.warning("Rate limited (429). Attempt %d/%d. Waiting %.1f seconds.", attempt, max_retries, wait)
                time.sleep(wait)
                continue
            if 500 <= resp.status_code < 600:
                # Transient server error: exponential backoff
                wait = base_delay * (2 ** (attempt - 1))
                logging.warning("Server error %d. Attempt %d/%d. Waiting %.1f seconds.", resp.status_code, attempt, max_retries, wait)
                time.sleep(wait)
                continue

            resp.raise_for_status()
            return resp.json()

        except requests.RequestException as e:
            # Non-HTTP exception (connection, timeout, etc.)
            wait = base_delay * (2 ** (attempt - 1))
            logging.warning("Request error: %s. Attempt %d/%d. Waiting %.1f seconds.", str(e), attempt, max_retries, wait)
            time.sleep(wait)
            continue

    # If we exit the loop, all retries failed
    raise RuntimeError(f"Failed to get successful response after {max_retries} attempts")


def parse_sections(text):
    """Parse LLM response text into named sections."""
    import re
    sections = {
        "prompt": None,
        "improvements": None,
        "techniques": None,
        "tip": None,
    }
    if not text or text.startswith("Error:"):
        return sections

    # Extract the optimized prompt between <<<PROMPT>>> and <<<END>>>
    prompt_match = re.search(r'<<<PROMPT>>>\s*\n?([\s\S]*?)<<<END>>>', text)
    if prompt_match:
        sections["prompt"] = prompt_match.group(1).strip()

    # Extract Key Improvements section
    improvements_match = re.search(
        r'Key Improvements?:\s*\n([\s\S]*?)(?=\n\n(?:Techniques?|Pro Tip|$)|\Z)',
        text, re.IGNORECASE
    )
    if improvements_match:
        sections["improvements"] = improvements_match.group(1).strip()

    # Extract Techniques Applied section
    techniques_match = re.search(
        r'Techniques? Applied:\s*\n?([\s\S]*?)(?=\n\n(?:Pro Tip|$)|\Z)',
        text, re.IGNORECASE
    )
    if techniques_match:
        sections["techniques"] = techniques_match.group(1).strip()

    # Extract Pro Tip section
    tip_match = re.search(
        r'Pro Tip:\s*\n?([\s\S]*?)(?:\n\n|\Z)',
        text, re.IGNORECASE
    )
    if tip_match:
        sections["tip"] = tip_match.group(1).strip()

    return sections


def stream_gemini(prompt):
    if not GEMINI_API_KEY:
        yield f"data: {json.dumps({'error': 'GEMINI_API_KEY is not set'})}\n\n"
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent?alt=sse&key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=60) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data: '):
                        data_str = decoded[6:]
                        if data_str == '[DONE]':
                            continue
                        try:
                            data_json = json.loads(data_str)
                            cands = data_json.get('candidates', [])
                            if cands:
                                parts = cands[0].get('content', {}).get('parts', [])
                                if parts:
                                    text_chunk = parts[0].get('text', '')
                                    if text_chunk:
                                        yield f"data: {json.dumps({'text': text_chunk})}\n\n"
                        except json.JSONDecodeError:
                            pass
    except Exception as e:
        logging.error(f"Streaming error: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@app.route('/api/generate', methods=['POST'])
def generate_api():
    data = request.get_json()
    user_idea = data.get('idea', '')
    if not user_idea:
        return {"error": "No idea provided"}, 400
    prompt = build_prompt(user_idea)
    return Response(stream_with_context(stream_gemini(prompt)), mimetype='text/event-stream')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result=None, sections=None)


if __name__ == '__main__':
    app.run(debug=True)
