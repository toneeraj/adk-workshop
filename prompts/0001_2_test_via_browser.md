# Test Agent via Browser

## Context

I'm at `~/adk-workshop` with a working ADK agent (`my_agent`).
- Virtual environment is activated
- Agent works via CLI (`adk run my_agent`)

## Role

Act as a developer assistant helping me test the agent via browser.

## Task

1. Run the ADK web interface:
   ```bash
   adk web
   ```

2. Tell me what URL to open in my browser (usually http://localhost:8000)

3. Keep the server running so I can interact with the agent in browser

## Constraints

- Keep the terminal session open
- The web server needs to stay running
- Tell me when it's ready and what URL to visit
