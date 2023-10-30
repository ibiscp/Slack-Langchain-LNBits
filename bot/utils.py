import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


def draft_email(user_input):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    template = """Your name is Sam and you are a helpful assistant that helps slack users with their need.
    
User: {user_input}
Sam: """

    # signature = f"Kind regards, \n\{name}"
    # system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    # human_template = "Here's the email to reply to and consider any other comments from the user for reply as well: {user_input}"
    # human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # chat_prompt = ChatPromptTemplate.from_messages(
    #     [system_message_prompt, human_message_prompt]
    # )
    chat_prompt = ChatPromptTemplate.from_template(template)

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    return chain.run(user_input=user_input)






def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    return text.upper()