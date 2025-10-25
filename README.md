# Testcase LLM API

A FastAPI-based service that generates API test cases using Large Language Models (LLM) with Ollama. The service stores existing test cases in SQLite and uses them as context to generate new, relevant test cases.

## Features

- **Generate Test Cases**: Create new test cases using LLM based on API requirements
- **Context-Aware**: Uses existing test cases from database as context for better generation
- **Multiple APIs**: Support for different API types (user_api, product_api, payment_api, etc.)
- **Test Types**: Generate both positive and negative test cases
- **RESTful API**: Clean REST endpoints for managing and generating test cases
- **Local LLM**: Uses Ollama for local LLM inference (privacy-focused)

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight database for storing test cases
- **Ollama**: Local LLM inference server
- **Python 3.14**: Latest Python version
- **Poetry**: Dependency management

## Prerequisites

1. **Python 3.14+**
2. **Poetry** for dependency management
3. **Ollama** for LLM inference

### Install Ollama

```bash
# macOS
brew install ollama

# Start Ollama service
ollama serve

# Pull a model (required)
ollama pull llama2
```

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd testcase_llm_api
```

2. **Configure Poetry for local virtual environment**
```bash
poetry config virtualenvs.in-project true
```

3. **Install dependencies**
```bash
poetry install
```

4. **Activate virtual environment**
```bash
poetry shell
# or
source .venv/bin/activate
```

5. **Initialize database**
```bash
python src/testcase_llm_api/init_db.py
```

## Usage

### 1. Start the API Server

```bash
uvicorn src.testcase_llm_api.main:app --reload
```

The API will be available at `http://localhost:8000`

### 2. API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### 3. API Endpoints

#### Add Test Cases
```bash
POST /testcases/
```

#### List Test Cases
```bash
GET /testcases/?api_name=user_api&testcase_type=positive
```

#### Generate New Test Case
```bash
POST /generate/
```

## API Examples

### Add Sample Test Cases

```bash
curl -X POST "http://localhost:8000/testcases/" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "testcase_description": "Test successful user registration with valid email and password",
      "pattern": "POST /api/users with valid data should return 201",
      "api_name": "user_api",
      "request_type": "POST",
      "testcase_type": "positive"
    },
    {
      "testcase_description": "Test user registration with invalid email format",
      "pattern": "POST /api/users with invalid email should return 400",
      "api_name": "user_api",
      "request_type": "POST",
      "testcase_type": "negative"
    }
  ]'
```

### Generate New Test Case

```bash
curl -X POST "http://localhost:8000/generate/" \
  -H "Content-Type: application/json" \
  -d '{
    "api_name": "user_api",
    "request_type": "POST",
    "testcase_type": "positive",
    "user_prompt": "Create a test for user registration with social media login"
  }'
```

**Response:**
```json
{
  "generated_testcase": {
    "testcase_description": "Test user registration with social media OAuth integration",
    "pattern": "POST /api/users/oauth with valid social token should return 201",
    "api_name": "user_api",
    "request_type": "POST",
    "testcase_type": "positive"
  }
}
```

### List Existing Test Cases

```bash
curl "http://localhost:8000/testcases/?api_name=user_api&testcase_type=positive"
```

## Project Structure

```
testcase_llm_api/
├── src/
│   └── testcase_llm_api/
│       ├── __init__.py
│       ├── main.py              # FastAPI application
│       ├── models.py            # Pydantic models
│       ├── database.py          # Database operations
│       ├── llm_utils.py         # LLM integration
│       └── init_db.py           # Database initialization
├── pyproject.toml               # Poetry configuration
├── README.md                    # This file
└── testcases.db                 # SQLite database (created after init)
```

## Database Schema

```sql
CREATE TABLE api_testcases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    testcase_description TEXT NOT NULL,
    pattern TEXT,
    api_name TEXT NOT NULL,
    request_type TEXT NOT NULL,
    testcase_type TEXT NOT NULL
);
```

## Configuration

### Environment Variables

- `OLLAMA_HOST`: Ollama server host (default: localhost:11434)
- `DATABASE_PATH`: SQLite database path (default: testcases.db)

### Ollama Models

The service uses `llama2` by default. You can use other models:

```bash
# Available models
ollama pull codellama
ollama pull mistral
ollama pull llama3

# Update model in llm_utils.py
model="your-preferred-model"
```

## Development

### Running Tests

```bash
poetry run pytest
```

### Code Formatting

```bash
# Install formatter
poetry add --group dev black

# Format code
poetry run black src/
```

### Adding Dependencies

```bash
poetry add package-name
poetry add --group dev package-name  # For development dependencies
```

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if not running
   ollama serve
   ```

2. **Model Not Found**
   ```bash
   # List available models
   ollama list
   
   # Pull required model
   ollama pull llama2
   ```

3. **Database Issues**
   ```bash
   # Reinitialize database
   rm testcases.db
   python src/testcase_llm_api/init_db.py
   ```

4. **Virtual Environment Issues**
   ```bash
   # Reset virtual environment
   poetry env remove python
   poetry install
   ```

## API Response Formats

### Success Response
```json
{
  "generated_testcase": {
    "testcase_description": "Description of the test case",
    "pattern": "HTTP_METHOD /api/endpoint should return STATUS_CODE",
    "api_name": "api_name",
    "request_type": "GET|POST|PUT|DELETE",
    "testcase_type": "positive|negative"
  }
}
```

### Error Response
```json
{
  "generated_testcase": {
    "error": "Error message",
    "raw_response": "Raw LLM response",
    "api_name": "api_name",
    "request_type": "request_type",
    "testcase_type": "testcase_type"
  }
}
```

## Roadmap & Next Steps

This POC demonstrates the core functionality of AI-powered test case generation. Here are the planned enhancements:

### Phase 1: Core Improvements (Weeks 1-2)
- **OpenAPI Specification Parsing**: Import and analyze Swagger/OpenAPI specs
- **Enhanced Validation**: Validate generated test cases for correctness
- **User Authentication**: JWT-based authentication system
- **Better Error Handling**: Comprehensive error handling and logging
- **Configuration Management**: Environment-based configuration

### Phase 2: Quality & UX (Weeks 3-4)
- **Web Interface**: Simple web UI for test case management
- **Test Case Editing**: Edit and refine generated test cases
- **Duplicate Detection**: Prevent duplicate test case generation
- **Export Functionality**: Export to Postman, JSON, or other formats
- **Performance Optimization**: Caching and response time improvements

### Phase 3: Production Features (Month 2)
- **PostgreSQL Migration**: Scale beyond SQLite
- **Redis Caching**: Improve response times with caching
- **Rate Limiting**: API usage controls
- **Monitoring & Metrics**: Application performance monitoring
- **Docker Containerization**: Easy deployment and scaling

### Phase 4: Advanced Features
- **Test Execution**: Execute generated test cases automatically
- **CI/CD Integration**: GitHub Actions and Jenkins plugins
- **Multiple LLM Support**: OpenAI, Anthropic, and other providers
- **Fine-tuned Models**: Domain-specific model training
- **Analytics Dashboard**: Test coverage and quality metrics

### Phase 5: Enterprise Features
- **Multi-tenancy**: Organization and team isolation
- **Advanced Analytics**: Business intelligence and reporting
- **Third-party Integrations**: Postman, Insomnia, testing frameworks
- **On-premise Deployment**: Enterprise deployment options

### Architecture Evolution
```
Current: FastAPI + SQLite + Ollama
Next: FastAPI + PostgreSQL + Redis + Multiple LLM providers
Future: Microservices + Event-driven + ML Pipeline
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Ollama](https://ollama.ai/) for local LLM inference
- [Poetry](https://python-poetry.org/) for dependency management