from agents.summary_agent import SummaryAgent
from agents.classification_agent import ClassificationAgent
from agents.recommendation_agent import RecommendationAgent
from agents.routing_agent import RoutingAgent
from langchain_community.llms import Ollama

# Initializing the LLM and agents
llm = Ollama(model="llama3.2")
summary_agent = SummaryAgent(llm)
classification_agent = ClassificationAgent(llm)
recommendation_agent = RecommendationAgent(llm)
routing_agent = RoutingAgent(llm)

def process_customer_query(query):
    """Handles a customer query step-by-step using AI agents."""
    
    summary = summary_agent.process(query)
    priority = classification_agent.process(summary)
    recommendations = recommendation_agent.process(summary)
    if "No past cases found" in recommendations:
        routing = routing_agent.process(summary)
    else:
        routing = "Resolved automatically"  

    return {
        "summary": summary,
        "priority": priority,
        "recommendations": recommendations,
        "routing": routing
    }

if __name__ == "__main__":
    customer_query = "Hello! My project data isn’t syncing between my laptop and tablet."
    response = process_customer_query(customer_query)
    print(response)
