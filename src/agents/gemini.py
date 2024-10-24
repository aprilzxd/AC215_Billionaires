import os
import vertexai
from phi.assistant import Assistant
from vertexai.generative_models import GenerativeModel
from phi.llm.base import LLM

# *********** Step 1: Initialize Vertex AI ***********
vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))

# *********** Step 2: Create a Custom Integration for Fine-Tuned Gemini ***********
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

# Wrapper class to make FineTunedGemini compatible with the LLM interface
class FineTunedGeminiWrapper(LLM):
    def __init__(self, fine_tuned_gemini):
        object.__setattr__(self, 'fine_tuned_gemini', fine_tuned_gemini)

    def generate(self, prompt):
        # Use the FineTunedGemini's method to generate a response
        return self.fine_tuned_gemini.call_model(prompt)

# Configuration settings for content generation
generation_config = {
    "max_output_tokens": 3000,
    "temperature": 0.75,
    "top_p": 0.95,
}

# Define the fine-tuned model endpoint
# MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/4117575388509503488"
MODEL_ENDPOINT = "projects/738060168305/locations/us-central1/endpoints/2997797562410336256"
# Initialize the fine-tuned Gemini model
fine_tuned_gemini = FineTunedGemini(model_endpoint=MODEL_ENDPOINT, generation_config=generation_config)

# Initialize the wrapper for the fine-tuned Gemini model
fine_tuned_gemini_wrapper = FineTunedGeminiWrapper(fine_tuned_gemini)

# *********** Step 3: Integrate with the Assistant Class from `phidata` ***********
class CustomAssistant(Assistant):
    def __init__(self, model, description=""):
        super().__init__(llm=model, description=description)

    def generate_response(self, prompt):
        # Use the generate method of the wrapped LLM model
        return self.llm.generate(prompt)

# Create an instance of the custom assistant using the wrapper
assistant = CustomAssistant(
    model=fine_tuned_gemini_wrapper,
    description="This assistant provides recommendations and insights using a fine-tuned language model.",
)

# *********** Step 4: Test and Run the Integration ***********
# Example usage
prompt = "Provide investment strategies for a student interested in Nvidia stock. He recently graduated and has $100k for investment."
response = assistant.generate_response(prompt)
print("Assistant Response:", response)
