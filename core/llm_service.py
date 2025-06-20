import os
from openai import OpenAI

class LLMService:
    """
    A centralized service to manage the LLM client.
    This ensures that the client is configured and instantiated in only one place.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        """Initializes the OpenAI client based on the environment provider."""
        api_provider = os.getenv("API_PROVIDER", "openai").lower()

        if api_provider == "ollama":
            print("🔧 Initializing Ollama LLM Client...")
            self.client = OpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",  # required but unused
            )
            self.model = os.getenv("OLLAMA_MODEL", "llama3")
        else:
            print("🔧 Initializing OpenAI LLM Client...")
            self.client = OpenAI()
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o")

# Create a single, shared instance of the service
llm_service = LLMService() 