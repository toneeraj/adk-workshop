# Google ADK Agent Setup on macOS

## Prerequisites

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12+
brew install python@3.12
```

## 1. Create Project Structure

```bash
mkdir -p ~/adk-workshop
cd ~/adk-workshop

# Create virtual environment with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv

# Activate it
source venv/bin/activate

# Install ADK
pip install google-adk
```

## 2. Get API Key

1. Go to: https://aistudio.google.com/apikey
2. Click **"Create API key in new project"**
3. Copy the key

```bash
# Add to ~/.zshrc
echo 'export GOOGLE_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

## 3. Create Agent

```bash
mkdir -p ~/adk-workshop/my_agent
touch ~/adk-workshop/my_agent/__init__.py
```

Create `~/adk-workshop/my_agent/agent.py`:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
```

## 4. Run Agent

```bash
cd ~/adk-workshop
source venv/bin/activate

# CLI mode
adk run my_agent

# Web UI mode
adk web my_agent
```

## Troubleshooting

### 429 Quota Errors
- If you get quota errors with `gemini-2.0-flash`, use `gemini-2.5-flash` instead
- Check your quota at: https://ai.dev/usage?tab=rate-limit

### Test API Key Directly

```bash
curl -s "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Python version too old | Install Python 3.12+ via Homebrew |
| `limit: 0` quota errors | API key from Cloud Console; use AI Studio instead |
| API key expired | Generate new key at aistudio.google.com/apikey |
| Model not found | Check available models; use `gemini-2.5-flash` |

## Available Models (as of Jan 2026)

- `gemini-2.5-flash` - Fast, recommended
- `gemini-2.5-pro` - More capable
- `gemini-2.5-flash-lite` - Lightweight
- `gemini-2.0-flash-lite` - Lightweight (2.0 series)
