from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from .db_utils import save_testcase, get_testcases
from .llm_utils import generate_testcase_llm

app = FastAPI()


class TestcaseIn(BaseModel):
    testcase_description: str
    pattern: Optional[str] = None
    api_name: str
    request_type: str
    testcase_type: str


class GenerateRequest(BaseModel):
    api_name: str
    request_type: str
    testcase_type: str
    user_prompt: str


@app.post("/testcases/")
def add_testcases(tcs: List[TestcaseIn]):
    for tc in tcs:
        save_testcase(
            tc.testcase_description,
            tc.pattern,
            tc.api_name,
            tc.request_type,
            tc.testcase_type,
        )
    return {"message": f"{len(tcs)} testcases saved successfully."}


@app.get("/testcases/")
def list_testcases(api_name: Optional[str] = None, testcase_type: Optional[str] = None):
    testcases = get_testcases(api_name, testcase_type)
    return {"testcases": testcases}


@app.post("/generate/")
def generate_testcase(req: GenerateRequest):
    existing_testcases = get_testcases(req.api_name, req.testcase_type)
    # You may want to specify the model name or pass it from the request
    generated = generate_testcase_llm(
        req.api_name,
        req.request_type,
        req.testcase_type,
        existing_testcases,
        req.user_prompt,
        model_name="distilgpt2"
    )
    return {"generated_testcase": generated}
