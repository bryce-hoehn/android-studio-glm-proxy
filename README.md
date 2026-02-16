# Android Studio GLM Proxy

A simple FastAPI proxy server for using GLM Coding in Android Studio.

## Features

- Proxies requests to the upstream API
- Handles chat completions with role transformation (developer → system)
- Supports streaming responses
- Wildcard routing for all other API endpoints

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file with your API key:

```
API_KEY=your_api_key_here
```

## Usage

Start the server:

```bash
python main.py
```

The server will run on `http://0.0.0.0:8000`
