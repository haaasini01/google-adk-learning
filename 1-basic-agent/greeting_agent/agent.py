from google.adk.agents import Agent
import json

_original_dumps = json.dumps

def _safe_dumps(*args, **kwargs):
    class BytesEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, bytes):
                return obj.decode("utf-8", errors="replace")
            return super().default(obj)
    kwargs.setdefault("cls", BytesEncoder)
    return _original_dumps(*args, **kwargs)

json.dumps = _safe_dumps

root_agent =  Agent(
    name = "greeting_agent",
    model = "gemini-3.6-flash",
    description= "Greeting Agent",
    instruction="""
    You are a helpful assistant that greets the user.
    Ask the user for their name and greet them by name.
    """
)