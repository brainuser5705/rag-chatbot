import os
import dotenv

dotenv.load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Chat History with LangGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

LM_STUDIOS_SERVER_URL = os.getenv("LM_STUDIOS_SERVER_URL")

# Here are context that can help you answer the question.

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: str


class Chatbot:
    def __init__(self):
        llm = ChatOpenAI(base_url=LM_STUDIOS_SERVER_URL, api_key="na")
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "Here are some context to help answer the following question: {context}. Only use the context if it is relevant to the question."),
                MessagesPlaceholder(variable_name="messages")
            ]
        )
        workflow = StateGraph(state_schema=State)
        parser = StrOutputParser()

        def call_model(state: State):
            chain = prompt_template | llm | parser
            return {"messages": [chain.invoke(state)]}
        
        workflow.add_edge(START, "model")
        workflow.add_node("model", call_model)

        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)

    def ask_question(self, returned_chunks, question):

        output = self.app.invoke(
            {"messages": [HumanMessage(question)], "context": returned_chunks},
            {"configurable": {"thread_id": "dummy_value"}}
        )
        
        print(output["messages"])
        return output["messages"][-1].content
        
        