from flask import Flask, request, render_template
import requests
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

app = Flask(__name__)

# Get your OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# 🔽 🔽 🔽 PUT YOUR CUSTOM PROMPT STRUCTURE HERE 🔽 🔽 🔽
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

**Platform Notes:**
- **ChatGPT/GPT-4:** Structured sections, conversation starters
- **Claude:** Longer context, reasoning frameworks
- **Gemini:** Creative tasks, comparative analysis
- **Others:** Apply universal best practices

## OPERATING MODES

**DETAIL MODE:** 
- Gather context with smart defaults
- Ask 2-3 targeted clarifying questions
- Provide comprehensive optimization

**BASIC MODE:**
- Quick fix primary issues
- Apply core techniques only
- Deliver ready-to-use prompt

## RESPONSE FORMATS

**Simple Requests:**
```
Your Optimized Prompt:
[Improved prompt]

What Changed: [Key improvements]
```

**Complex Requests:**
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
"""
# 🔼 🔼 🔼 DO NOT EDIT BELOW THIS LINE UNLESS NEEDED 🔼 🔼 🔼


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        user_idea = request.form.get('idea')
        prompt = build_prompt(user_idea)

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek/deepseek-chat-v3-0324:free",
                    "messages": [
                        {"role": "system", "content": "You are a helpful AI that formats user ideas into structured prompts."},
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            response.raise_for_status()
            data = response.json()
            result = data["choices"][0]["message"]["content"]

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
