import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from question_answering_agent import question_answering_agent
from google.genai import types


load_dotenv()

# creating a new session to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Hasini Reddy",
    "user_preferences": """
        I like frogs. I like playing basketball. 
        I lovee chicken. I love reading books and one of my favourite books is 'The Color Purple'.
        I love watching 'Modern Family'
    """
}

APP_NAME = "Hasini Bot"
SESSION_ID = str(uuid.uuid4())
USER_ID = "hasini_reddy"
# create a new session
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("Created new session")
print(SESSION_ID)

# creating a runner 
# we need two elements (agents + session)
runner = Runner(
    agent=question_answering_agent,
    session_service=session_service_stateful,
    app_name=APP_NAME
)

# creating a msg to send (user msg)
new_msg = types.Content(
    role="user", #this'll be wither user or agent
    parts=[types.Part(text="What is Hasini's favourite TV Show?")]
)


for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_msg,
):
    if event.is_final_response(): #response is gonna get saved as an event in our session so we check if there's a final response in the events
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")
