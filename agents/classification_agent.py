from agents.base_agent import BaseAgent
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from vector_store import VectorStore

class ClassificationAgent(BaseAgent):
    """
    Classifies customer issues based on priority level (Critical, High, Medium, Low).
    Uses a RAG system to retrieve similar past cases before classification.
    """

    def __init__(self, llm):
        super().__init__(llm)
        self.vector_store = VectorStore() 

        self.prompt = PromptTemplate(
            input_variables=["query", "context"],
            template=(
                "You are a support assistant classifying customer issues by priority level.\n\n"
                "Here is the customer's issue:\n{query}\n\n"
                "Relevant past cases for context:\n{context}\n\n"
                "Based on this, classify the issue as 'Critical', 'High', 'Medium', or 'Low'.\n"
                "Return only the priority level."
            )
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def process(self, query):
        """Retrieves similar cases and classifies the issue."""
        similar_cases = self.vector_store.query_similar(query)

       
        context = "\n".join(case["text"] if isinstance(case, dict) and "text" in case else str(case) for case in similar_cases) if similar_cases else "No relevant cases found."

    
        priority = self.chain.run({"query": query, "context": context})
        return priority.strip()
