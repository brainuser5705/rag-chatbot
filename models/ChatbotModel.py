import os
import dotenv

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

LM_STUDIOS_SERVER_URL = os.getenv("LM_STUDIOS_SERVER_URL")

class Chatbot:
    def __init__(self):
        llm = ChatOpenAI(base_url=LM_STUDIOS_SERVER_URL, api_key="na")
        parser = StrOutputParser()
        prompt_template = ChatPromptTemplate.from_template("""
            Given the following context, answer the question. If the answer cannot 
            be found in the context, then reply with "I don't know".

            Context: {context}

            Question: {question}
            """
        )

        self.chain = prompt_template | llm | parser 

    def ask_question(self, returned_chunks, question):
        return self.chain.invoke({"context":returned_chunks, "question":question})
        
        