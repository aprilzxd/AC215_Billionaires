# gemini_module.py
import os
import vertexai
from vertexai.generative_models import GenerativeModel
from pydantic import PrivateAttr
from phi.llm.base import LLM

# Initialize Vertex AI
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))

class FineTunedGemini:
    def __init__(self, model_endpoint, generation_config):
        self.model_endpoint = model_endpoint
        self.generation_config = generation_config
        self.model = GenerativeModel(model_endpoint)

    def call_model(self, prompt):
        # Generate content using the fine-tuned model
        response = self.model.generate_content(
            [prompt],  # Input prompt
            generation_config=self.generation_config,
            stream=False
        )
        return response.text

    def call_model_stream(self, prompt):
        # Generate content using the fine-tuned model with streaming enabled
        response = self.model.generate_content(
            [prompt],
            generation_config=self.generation_config,
            stream=True  # Enable streaming for responses
        )
        # Iterate over the response to yield each text chunk
        for chunk in response:
            yield chunk.text

class FineTunedGeminiWrapper(LLM):
    # Use PrivateAttr to handle fields that should not be part of the Pydantic model
    _fine_tuned_gemini: FineTunedGemini = PrivateAttr()
    _tools: list = PrivateAttr(default_factory=list)
    _run_id: str = PrivateAttr(default=None)

    def __init__(self, fine_tuned_gemini, **kwargs):
        # Set the private attributes using Pydantic's PrivateAttr
        object.__setattr__(self, '_fine_tuned_gemini', fine_tuned_gemini)
        object.__setattr__(self, '_tools', [])  # Initialize tools as an empty list
        object.__setattr__(self, '_run_id', None)  # Initialize run_id to None

        # Dynamically set any additional attributes passed in
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def generate(self, prompt):
        # Use the FineTunedGemini's method to generate a response
        return self._fine_tuned_gemini.call_model(prompt)

    def response_stream(self, messages):
        # Access the last message's content using the attribute instead of dictionary-style indexing
        prompt = messages[-1].content
        # Stream the response using the FineTunedGemini's streaming capabilities
        for chunk in self._fine_tuned_gemini.call_model_stream(prompt):
            yield chunk

    def add_tool(self, tool):
        # Add the tool to the list of tools
        self._tools.append(tool)

    def get_tools(self):
        # Return the list of tools
        return self._tools

    def run_tool(self, tool_name, *args, **kwargs):
        # Find the tool by name and execute it
        for tool in self._tools:
            if tool.name == tool_name:
                return tool.run(*args, **kwargs)
        raise ValueError(f"Tool {tool_name} not found")

    def __getattr__(self, name):
        # Handle dynamic attribute access gracefully
        if name == 'run_id':
            return self._run_id
        # Return None for other attributes not explicitly set
        return None

    def __setattr__(self, name, value):
        # Use custom handling for setting the run_id
        if name == 'run_id':
            object.__setattr__(self, '_run_id', value)
        else:
            super().__setattr__(name, value)

def get_gemini_assistant(show_tool_calls=False, debug_mode=False, tool_choice=None):
    # Configuration settings for content generation
    generation_config = {
        "max_output_tokens": 3000,
        "temperature": 0.75,
        "top_p": 0.95,
    }

    # Define the fine-tuned model endpoint
    MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/4117575388509503488"

    # Initialize the fine-tuned Gemini model
    fine_tuned_gemini = FineTunedGemini(model_endpoint=MODEL_ENDPOINT, generation_config=generation_config)

    # Initialize the wrapper for the fine-tuned Gemini model with additional attributes
    gemini_wrapper = FineTunedGeminiWrapper(
        fine_tuned_gemini,
        show_tool_calls=show_tool_calls,
        debug_mode=debug_mode,
        tool_choice=tool_choice
    )

    # Return the initialized wrapper
    return gemini_wrapper
