# Android Studio GLM Proxy

A FastAPI proxy server for using GLM Coding in Android Studio. Use alongside [android-studio-mcp-proxy](https://github.com/bryce-hoehn/android-studio-mcp-proxy) for MCP support.

## Features

- Proxies requests to the upstream API
- Handles chat completions with role transformation (developer → system)
- Supports streaming responses
- Supports tool use
- Docker support

## Installation

### Docker

1. Clone the repository
   ```bash
   git clone https://github.com/bryce-hoehn/android-studio-glm-proxy
   ```

2. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   ```
   Edit .env and add your API key

3. Start the container:
   ```bash
   docker compose up -d
   ```

4. The server will run on `http://localhost:8000`

### Without Docker

1. Clone the repository
   ```
   git clone https://github.com/bryce-hoehn/android-studio-glm-proxy
   ```

2. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   ```
   Edit .env and add your API key

3. Create a .venv environment
   ```bash
   python -m venv .venv
   ```

4. Enter venv environment
   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the server:
   ```bash
   python main.py
   ```

7. The server will run on `http://localhost:8000` (until you close the terminal)

## Configuration

### Environment Variables

Create a `.env` file with the following variable:

```env
API_KEY=your_api_key_here
```

### Configuration via config.py

For advanced configuration, you can modify settings directly in [`app/config.py`](app/config.py:1):

```python
class Settings:
    BASE_URL: str = "https://api.z.ai/api/coding/paas/v4"  # Upstream API URL
    HOST: str = "0.0.0.0"                                  # Server host
    PORT: int = 8000                                       # Server port
    TIMEOUT: int = 60                                       # Request timeout (seconds)
```

### Configuration via docker-compose.yml

When using Docker, you can customize the deployment by editing [`docker-compose.yml`](docker-compose.yml:1):

```yaml
services:
  android-studio-llm-proxy:
    ports:
      - "8000:8000"    # Format: "host_port:container_port"
    environment:
      - API_KEY=${API_KEY}
    env_file:
      - .env
    restart: unless-stopped  # Options: no, always, on-failure, unless-stopped
```

Common docker-compose configurations:
- **Change host port**: Modify `"8000:8000"` to `"HOST_PORT:8000"`
- **Disable restart**: Set `restart: no`
- **Always restart**: Set `restart: always`

## Using in Android Studio

1. **Open Android Studio Settings:**
   - Go to `File` -> `Settings` -> `Tools` -> `AI`

2. **Configure LLM Provider:**
   - Add a provider (local or remote depending on where you deploy it)
   - Set the API endpoint to: `http://localhost:8000`. Replace `localhost` with ip address if running on a different device
   - Enter anything into the API Key field (ex. "1234")

## API Endpoints

### Chat Completions

```
POST /chat/completions
```

Proxy endpoint for chat completion requests. Supports streaming and tool use.

### Models

```
GET /models
```

List available models from the upstream API.
