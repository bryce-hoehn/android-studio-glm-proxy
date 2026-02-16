# Android Studio GLM Proxy

A FastAPI proxy server for using GLM Coding in Android Studio with MCP (Model Context Protocol) server support.

## Features

- Proxies requests to the upstream API
- Handles chat completions with role transformation (developer → system)
- Supports streaming responses
- Supports tool use
- Dynamic MCP server routing - Register MCP servers from configuration
- Docker support - Easy deployment with Docker and docker-compose

## Installation

### Docker

1. Clone the repository
2. Create a `.env` file with your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```
3. Configure MCP servers in `mcp_settings.json` (optional)
4. Start the container:
   ```bash
   docker-compose up -d
   ```
5. The server will run on `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file with the following variable:

```env
API_KEY=your_api_key_here
```

### MCP Servers

Configure MCP servers in `mcp_settings.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "DEFAULT_MINIMUM_TOKENS": ""
      },
      "alwaysAllow": [
        "resolve-library-id",
        "get-library-docs",
        "query-docs"
      ]
    }
  }
}
```

```bash
docker-compose restart
```

## Using MCP Servers in Android Studio

1. **Open Android Studio Settings:**
   - Go to `File` → `Settings` (or `Android Studio` → `Settings` on macOS)

2. **Configure LLM Provider:**
   - Navigate to `Tools` → `AI Assistant` → `LLM Provider`
   - Set the API endpoint to: `http://localhost:8000`
   - Enter anything into the API Key field (ex. "1234")

3. **Enable MCP Integration:**
   - Navigate to `Tools` → `AI Assistant` → `MCP Servers`
   - Add a new MCP server with the URL: `http://localhost:8000/mcp/{server_name}`
   - Replace `{server_name}` with the name from your `mcp_settings.json` (e.g., `context7`)

4. **Example Configuration:**
   - Server Name: `Context7 Docs`
   - Server URL: `http://localhost:8000/mcp/context7`

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

### MCP Servers

Dynamic endpoints are created for each configured MCP server:

```
GET /mcp/{server_name}
```

For example, with the default configuration:
```
GET /mcp/context7
```