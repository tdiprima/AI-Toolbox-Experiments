`myapp.py`

Here's how you can build a [FastAPI](https://fastapi.tiangolo.com/) app with an endpoint `/refactor` that takes a code snippet, uses OpenAI to refactor it for efficiency, and returns both the original and the refactored code with explanations.

## 1. Install dependencies

```bash
pip install fastapi uvicorn openai
```

This installs the necessary packages:

* `fastapi`: The web framework.
* `uvicorn`: The ASGI server to run your FastAPI app.
* `openai`: Python client to call OpenAI's models.

## 2. Set up the FastAPI app

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use env variable for security
```

* Creates a FastAPI app instance.
* Uses `os.getenv` to fetch your OpenAI key from the environment. You *can* hardcode it while testing, but environment variables are safer and more flexible.

## 3. Define request and response models

```python
class RefactorRequest(BaseModel):
    code: str
    language: str = "python"  # Optional, defaults to Python

class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    explanation: str
```

* `RefactorRequest` defines the shape of the incoming JSON: code string and an optional language (defaults to Python).
* `RefactorResponse` shapes the outgoing response with original, refactored code, and a GPT-generated explanation.

## 4. Refactoring logic using OpenAI

```python
import re

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def refactor_code_with_gpt(code: str, language: str):
    prompt = (
        f"Refactor the following {language} code to be more efficient and pythonic. "
        "Explain the changes you made:\n\n"
        f"Original code:\n{code}\n\nRefactored code with explanation:"
    )

    response = await aclient.chat.completions.create(model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are an expert software engineer."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.2,
    max_tokens=800)

    content = response.choices[0].message.content

    # Extract refactored code (inside triple backticks) and explanation (text after)
    code_blocks = re.findall(r"```(?:\w+\n)?(.*?)```", content, re.DOTALL)
    refactored_code = code_blocks[0].strip() if code_blocks else ""
    explanation = content.split("```")[-1].strip() if "```" in content else content

    return refactored_code, explanation
```

* Builds a prompt asking GPT to refactor and explain the input code.
* Uses `aclient.chat.completions.create` (✅ async version) to send it to OpenAI's chat model.
* Uses regex to pull out the refactored code from triple backticks and treat the rest as explanation. This assumes GPT formats output reasonably. Tweak this if the model's response is inconsistent.

## 5. Create the `/refactor` endpoint

```python
from fastapi.responses import JSONResponse

@app.post("/refactor", response_model=RefactorResponse)
async def refactor_endpoint(req: RefactorRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    refactored_code, explanation = await refactor_code_with_gpt(req.code, req.language)

    if not refactored_code:
        raise HTTPException(status_code=500, detail="Failed to refactor code.")

    return RefactorResponse(
        original_code=req.code,
        refactored_code=refactored_code,
        explanation=explanation
    )
```

* Validates that `code` isn't empty.
* Calls the async refactor function to get new code + explanation.
* Returns it wrapped in the `RefactorResponse` model.
* If something fails, throws a 500 error with a clear message.

## 6. Run the app

```bash
uvicorn your_filename:app --reload
```

This launches your FastAPI app using `uvicorn`.

* Replace `your_filename` with the name of your Python script (without `.py`).
* `--reload` auto-restarts the server on code changes, great for dev work.

## 🛠️ How it works

* You send a POST request to `/refactor` with JSON like:

  ```json
  {
    "code": "for i in range(len(arr)): print(arr[i])",
    "language": "python"
  }
  ```

* GPT refactors the code and explains why.
* You get a JSON response with:

  * the original code
  * the cleaned-up version
  * an explanation

## 💻 Example request (with `curl`)

```bash
curl -X POST http://localhost:8000/refactor \
  -H "Content-Type: application/json" \
  -d '{"code": "for i in range(len(arr)): print(arr[i])", "language": "python"}'
```

**Response:**

```json
{
  "original_code": "for i in range(len(arr)): print(arr[i])",
  "refactored_code": "for item in arr:\n    print(item)",
  "explanation": "Used direct iteration over the list for better readability and efficiency."
}
```

## 🔒 Notes

* Handle rate limits or errors gracefully in production (timeouts, retries, etc.).
* Sanitize inputs if you're storing or further processing them.
* Extend it to support other languages like JS, Go, etc., by tweaking the prompt.

<br>
