from google.adk.agents import Agent
from google.adk.tools import google_search
from datetime import datetime

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


# custom tool (type: functional tool)
def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    return{
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

root_agent = Agent(
    name="tool_agent",
    model="gemini-3.5-flash",
    description="Tool Agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time
    """,
    tools=[get_current_time]
    # tools=[google_search]
)