from fastapi import FastAPI, Request, HTTPException
from agents.summary_agent import SummaryAgent
from agents.classification_agent import ClassificationAgent
from agents.recommendation_agent import RecommendationAgent
from agents.routing_agent import RoutingAgent
from langchain_community.llms import Ollama
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
llm = Ollama(model="llama3.2")

# Initialize agents
summary_agent = SummaryAgent(llm)
classification_agent = ClassificationAgent(llm)
resolution_agent = RecommendationAgent(llm)
routing_agent = RoutingAgent(llm)

# Set up templates and static files
app.mount("/static", StaticFiles(directory="web_app/static"), name="static")
templates = Jinja2Templates(directory="web_app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_query")
async def process_query(request: Request):
    """Unified endpoint to handle summarization, classification, resolution, and routing."""
    data = await request.json()
    query = data.get("query", "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query text is required")

    print(f"Received query: {query}")  # Debugging log

    # Step 1: Summarize the issue
    summary = summary_agent.process(query)

    # Step 2: Classify the issue
    category = classification_agent.process(summary)

    # Step 3: Attempt automated resolution
    resolution = resolution_agent.process(summary)

    # Step 4: Route only if no clear resolution exists
    if "No automated solution found" in resolution:
        department = routing_agent.process(summary)
    else:
        department = "Resolved automatically"

    return {
        "summary": summary,
        "category": category,
        "resolution": resolution,
        "department": department
    }
