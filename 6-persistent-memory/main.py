# we want to store sessions in a database 
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from memory_agent.memory_agent import memory_agent
from utils import call_agent_async
import asyncio


load_dotenv()


db_url = "sqlite:///./my_agent_data.db" # we're saying we want all the info abt session to be saved to this file, if file doesn't exist it'll be created
session_service = DatabaseSessionService(db_url=db_url)

initial_state = {
    "user_name": "Hasini Reddy",
    "reminders": []
}


async def main_async():
    APP_NAME = "Memory Agent"
    USER_ID = "haaasini01"

    # session management (find/create)
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    # if there's an existing session, use it, else create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # create new session with intial state
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # Runner setup
    runner = Runner(
        agent=memory_agent,
        session_service=session_service,
        app_name=APP_NAME
    )

    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input = input("You: ")

        #check if user wrote exit/quir
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the conversation. Your data has been saved to the database.")
            break

        # process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main_async())