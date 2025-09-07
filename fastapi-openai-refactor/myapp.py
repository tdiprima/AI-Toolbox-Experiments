# uvicorn myapp:app --reload
import os
import re

from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class RefactorRequest(BaseModel):
    code: str
    language: str = "python"  # Optional, defaults to Python


class RefactorResponse(BaseModel):
    original_code: str
    refactored_code: str
    explanation: str


async def refactor_code_with_gpt(code: str, language: str):
    prompt = (
        f"Refactor the following {language} code to be more efficient and pythonic. "
        "Explain the changes you made:\n\n"
        f"Original code:\n{code}\n\nRefactored code with explanation:"
    )

    response = await aclient.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert software engineer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=800,
    )

    content = response.choices[0].message.content

    # Extract refactored code (inside triple backticks) and explanation (text after)
    code_blocks = re.findall(r"```(?:\w+\n)?(.*?)```", content, re.DOTALL)
    refactored_code = code_blocks[0].strip() if code_blocks else ""
    explanation = content.split("```")[-1].strip() if "```" in content else content

    return refactored_code, explanation


@app.post("/refactor", response_model=RefactorResponse)
async def refactor_endpoint(req: RefactorRequest):
    if not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    refactored_code, explanation = await refactor_code_with_gpt(req.code, req.language)

    if not refactored_code:
        raise HTTPException(status_code=500, detail="Failed to refactor code.")

    return RefactorResponse(
        original_code=req.code, refactored_code=refactored_code, explanation=explanation
    )
