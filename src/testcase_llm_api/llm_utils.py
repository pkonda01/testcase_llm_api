from transformers import pipeline


def generate_testcase_llm(
    api_name,
    request_type,
    testcase_type,
    existing_testcases,
    user_prompt,
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
):
    """
    Generate a new API testcase using a Hugging Face Transformers model, given context from existing testcases.
    """
    context = "\n".join(
        [f"- {tc[1]} (Pattern: {tc[2]}, Type: {tc[5]})" for tc in existing_testcases]
    )
    prompt = (
        f"API Name: {api_name}\n"
        f"Request Type: {request_type}\n"
        f"Testcase Type: {testcase_type}\n"
        f"Existing Testcases:\n{context}\n"
        f"User Prompt: {user_prompt}\n"
        "Suggest a new testcase description and pattern."
    )

    generator = pipeline("text-generation", model=model_name)
    response = generator(prompt, max_new_tokens=300, temperature=0.7)
    return response[0]["generated_text"]
