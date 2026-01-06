# Full ADK Setup from Scratch

## Context

I'm setting up a Google ADK (Agent Development Kit) project on a fresh Mac. I need:
- Python 3.12+ (ADK requires 3.10+)
- Virtual environment
- ADK installed
- Working Gemini API key

## Role

Act as a developer assistant helping me set up ADK from scratch.

## Task

Execute these steps in order:

### 1. Check/Install Homebrew
```bash
brew --version
# If not found:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Python 3.12
```bash
brew install python@3.12
```

### 3. Create Project Folder
```bash
mkdir -p ~/adk-workshop
cd ~/adk-workshop
```

### 4. Create Virtual Environment
```bash
/opt/homebrew/bin/python3.12 -m venv venv
```

### 5. Activate and Install ADK
```bash
source venv/bin/activate
pip install google-adk
```

### 6. Get API Key from AI Studio
- Go to: https://aistudio.google.com/apikey
- Click "Create API key in new project"
- Copy the key

### 7. Set API Key
```bash
echo 'export GOOGLE_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 8. Create Agent Folder Structure
```bash
mkdir -p ~/adk-workshop/my_agent
touch ~/adk-workshop/my_agent/__init__.py
```

### 9. Create Agent File

Create `~/adk-workshop/my_agent/agent.py`:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
```

### 10. Test the Agent
```bash
cd ~/adk-workshop
source venv/bin/activate
adk run my_agent
```

## Constraints

- Use Python 3.12+ (not system Python)
- Use `gemini-2.5-flash` model (`gemini-2.0-flash` has quota issues)
- Get API key from AI Studio (not Google Cloud Console)
- Confirm each major step before proceeding
- If any step fails, stop and report the error
