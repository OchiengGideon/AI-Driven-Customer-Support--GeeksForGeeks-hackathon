class BaseAgent:
    """
    Base class for all AI agents in the system.
    Each agent should implement the `process` method.
    """
    def __init__(self, llm):
        self.llm = llm

    def process(self, input_text):
        raise NotImplementedError("Subclasses must implement process method")