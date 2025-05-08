# Nuclear Textbook Fine-tuning Project

This project processes a nuclear textbook PDF and prepares it for fine-tuning using the Gemini API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Project Structure

- `pdf_processor.py`: Handles PDF text extraction and preprocessing
- `data_preparation.py`: Prepares the extracted text for fine-tuning
- `.env`: Contains API keys and configuration (not tracked in git)
- `requirements.txt`: Project dependencies
