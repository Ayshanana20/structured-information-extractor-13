# Structured Information Extractor (Project 13)

Converts unstructured internship application text into validated JSON using Pydantic schemas, versioned prompts, and a 20-case test suite.

## Project Structure
- `schema.py`: Pydantic model (`InternshipApplication`) and enums (`TrackEnum`, `AvailabilityEnum`)
- `prompts.py`: Versioned system prompts (`SYSTEM_PROMPT_V1`, `SYSTEM_PROMPT_V2`), few-shot examples, and user prompt template
- `extractor.py`: Extraction and Pydantic validation logic
- `run_tests.py`: 20-test-case runner generating `results_table.md` and `test_results.json`
- `prompt_notes.md`: Prompt change log and risks/limitations
- `.env.example`: Environment variable template (no real API keys)
- `requirements.txt`: Python dependencies

## Setup & Usage
1. Install dependencies:
   ```powershell
   pip install -r requirements.txt