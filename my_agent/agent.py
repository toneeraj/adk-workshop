from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful assistant. Be concise and friendly.",
)
