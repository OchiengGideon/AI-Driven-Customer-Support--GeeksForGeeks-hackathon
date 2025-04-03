from agents.base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class RoutingAgent(BaseAgent):
    """
    Routes customer queries to the appropriate team for resolution.
    """
    def __init__(self, llm):
        super().__init__(llm)
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="Determine the best team to handle this issue: {query}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process(self, query):
        return self.chain.run(query)