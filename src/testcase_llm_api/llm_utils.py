import ollama
import json
import re

def generate_testcase_llm(
    api_name, request_type, testcase_type, user_prompt, existing_testcases
):
    # Format existing testcases for better context
    existing_formatted = ""
    if existing_testcases:
        existing_formatted = "\n".join([
            f"- {tc[1]}: {tc[2]}" for tc in existing_testcases  # pattern: description
        ])
    
    prompt = f"""
You are a test case generation expert. Generate a single, well-structured test case based on the following requirements:

API Name: {api_name}
Request Type: {request_type}
Testcase Type: {testcase_type}
User Requirements: {user_prompt}

Existing Test Cases for this API:
{existing_formatted if existing_formatted else "None"}

Generate ONE new test case in this exact JSON format:
{{
    "testcase_description": "Brief description of what this test validates",
    "pattern": "HTTP_METHOD /api/endpoint description should return STATUS_CODE",
    "api_name": "{api_name}",
    "request_type": "{request_type}",
    "testcase_type": "{testcase_type}"
}}

Return only the JSON object, no additional text.
"""

    try:
        response = ollama.generate(
            model="llama2",
            prompt=prompt,
            options={
                "temperature": 0.7,
                "num_predict": 300
            }
        )
        
        raw_response = response['response']
        
        # Try to extract and parse JSON from the response
        try:
            # Look for JSON pattern in the response
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                # Parse and return formatted JSON
                parsed_json = json.loads(json_str)
                return parsed_json
            else:
                # If no JSON found, return a structured response
                return {
                    "testcase_description": f"Generated test case for {api_name} {request_type} {testcase_type}",
                    "pattern": f"{request_type.upper()} /api/{api_name.replace('_api', '')} should return 200",
                    "api_name": api_name,
                    "request_type": request_type,
                    "testcase_type": testcase_type,
                    "raw_response": raw_response
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, return structured error
            return {
                "error": "Failed to parse JSON response",
                "raw_response": raw_response,
                "api_name": api_name,
                "request_type": request_type,
                "testcase_type": testcase_type
            }
            
    except Exception as e:
        return {
            "error": f"Error generating testcase: {str(e)}",
            "api_name": api_name,
            "request_type": request_type,
            "testcase_type": testcase_type
        }