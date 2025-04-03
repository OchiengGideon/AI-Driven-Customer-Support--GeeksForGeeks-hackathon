from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from agents.base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    """
    Extracts key details from customer conversations using LLM.
    """
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="Summarize the following customer query: {query}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process(self, query):
        return self.chain.run(query)