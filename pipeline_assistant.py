import os
import json
import urllib.request

class VFXPipelineAssistant:
    """
    Open-source AI assistant for VFX compositing (Foundry Nuke) and 3D pipelines.
    Helps generate Python/TCL scripts and analyze node-graph errors.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def ask_pipeline_ai(self, prompt, software="Foundry Nuke"):
        if not self.api_key:
            return "Error: OPENAI_API_KEY is not set in environment variables."

        system_prompt = (
            f"You are an expert VFX Pipeline Technical Director specializing in {software} "
            "Python API, node-graph workflows, AOV compositing, and 3D asset management. "
            "Provide clean, production-ready Python code and concise technical fixes."
        )

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"API Request Failed: {str(e)}"


if __name__ == "__main__":
    assistant = VFXPipelineAssistant()
    sample_query = "Write a Python snippet for Foundry Nuke to create an Unpremult -> Grade -> Premult node chain on selected Read nodes."
    print(f"Query: {sample_query}\n")
    print(assistant.ask_pipeline_ai(sample_query))
