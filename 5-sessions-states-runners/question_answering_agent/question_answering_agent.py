from google.adk.agents import Agent

question_answering_agent = Agent(
    model='gemini-3.6-flash',
    name='question_answering_agent',
    description='A question answering agent.',
    instruction="""
        You are a helpfull assistant that answers questions about user preferences.
        Here's some info about the user:
        Name: {user_name}
        Preferences: {user_preferences}
    """
    # this is how you access info abt state inside the agent
)
