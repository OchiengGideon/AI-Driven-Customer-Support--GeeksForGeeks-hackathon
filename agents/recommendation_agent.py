from agents.base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from vector_store import VectorStore
from agents.routing_agent import RoutingAgent  # Import RoutingAgent

class RecommendationAgent(BaseAgent):
    """
    Uses a RAG system to provide recommendations based on past ticket data.
    If no relevant cases are found, activates the RoutingAgent.
    """

    def __init__(self, llm):
        super().__init__(llm)
        self.vector_store = VectorStore()  # Load vector store
        self.routing_agent = RoutingAgent(llm)  # Initialize RoutingAgent
        self.prompt = PromptTemplate(
            input_variables=["query", "context"],
            template=(
                "Based on past resolved issues, generate a response for this query:\n\n"
                "Query: {query}\n\n"
                "\n{context}\n\n"
                "Provide a clear and concise resolution."
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process(self, query):
        """Retrieve relevant cases and generate a response using RAG.
        If no relevant cases exist, route the query to the appropriate team.
        """
        similar_cases = self.vector_store.query_similar(query)

        if similar_cases:
            # Use retrieved cases as context
            context = "\n".join(
                  case["text"] if isinstance(case, dict) and "text" in case else str(case)
                  for case in similar_cases
              ) if similar_cases else "No relevant cases found."

            return self.chain.run({"query": query, "context": context})
        else:
            # No past cases found → Activate RoutingAgent
            return f"No past cases found. Assigned to: {self.routing_agent.process(query)}"
