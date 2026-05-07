from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('./local_models/all-MiniLM-L6-v2')
print("Model saved successfully.")

/Users/praveen/workspace/testcase_llm_api/local_models