from agents.base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from vector_store import VectorStore
from agents.routing_agent import RoutingAgent  

class RecommendationAgent(BaseAgent):
    """
    Uses a RAG system to provide recommendations based on past ticket data.
    If no relevant cases are found, activates the RoutingAgent.
    """

    def __init__(self, llm):
        super().__init__(llm)
        self.vector_store = VectorStore() 
        self.routing_agent = RoutingAgent(llm)  
        self.prompt = PromptTemplate(
            input_variables=["query", "context"],
            template=(
                "Respond to this user query as a friendly support assistant. Use direct speech and simple markdown formatting.\n\n"
                "**Structure your response like this:**\n"
                "💬 Hello! [Brief friendly greeting]\n\n"
                "[Explain your understanding of their problem in 1-2 sentences]\n\n"
                "🛠️ **Step-by-Step Solution:**\n"
                "1. [First step in clear language]\n"
                "2. [Second step if needed]\n"
                "3. [Additional steps as required]\n\n"
                "💡 **Pro Tip:** [Optional helpful tip or note]\n\n"
                "Let me know if you need more help with this!\"\n\n"
                "User Query: {query}\n\n"
                "Relevant Context:\n{context}\n\n"
                "Maintain a warm, professional tone and use **bold** for section headers."
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process(self, query):
        """Retrieve relevant cases and generate a response using RAG.
        If no relevant cases exist, route the query to the appropriate team.
        """
        similar_cases = self.vector_store.query_similar(query)

        if similar_cases:
            # Using retrieved cases as context
            context = "\n".join(
                  case["text"] if isinstance(case, dict) and "text" in case else str(case)
                  for case in similar_cases
              ) if similar_cases else "No relevant cases found."

            return self.chain.run({"query": query, "context": context})
        else:
            #  Activating RoutingAgent if No past cases foundm
            return f"No past cases found. Assigned to: {self.routing_agent.process(query)}"
