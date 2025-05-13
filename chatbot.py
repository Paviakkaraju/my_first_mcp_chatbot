from mcp_client import send_mcp_request
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def generate_response(user_input):
    try:
        # Step 1: Retrieve context from MCP server
        retrieval = send_mcp_request(user_input)
        context_chunks = retrieval.get('retrieved_chunks', [])[:3]
        
        # Ensure there's some context to pass to the LLM
        context = '\n'.join(context_chunks) or "No relevant context available. Please refine your query or check the website for more information."

        # Step 2: Prepare headers and payload for GROQ API
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return "❌ GROQ_API_KEY is not set in environment variables."

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Step 3: Improved system prompt with more dynamic handling
        prompt = f"""You are an AI assistant for Codework, a company providing AI and Software Development services. Always address codework as "We" instead of "They" Example: "We offer AI solutions" 
        Answer the user’s questions based on the following context. If the question isn't related to Codework, kindly inform the user it is outside your scope.
        Context:
        {context}
        """

        payload = {
            "model": "meta-llama/llama-4-maverick-17b-128e-instruct",  
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        }

        print("Sending payload:", json.dumps(payload, indent=2))

        # Step 4: Call the GROQ API
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print(f"❌ Error from LLM: {response.status_code} - {response.text}")
            return f"Error from LLM: {response.status_code} - {response.reason}"

        # Step 5: Extract and return the result
        result = response.json()

        # Safely parse the response to ensure we get the correct content
        choices = result.get("choices", [])
        if choices and "message" in choices[0]:
            response_content = choices[0]["message"]["content"].strip()
            # Step 6: If response is too generic, add more useful follow-up advice
            if "Codework" not in response_content:
                response_content += "\nFor more specific information, please check our website or provide more details."
            return response_content
        else:
            print("❌ Unexpected LLM response format:", result)
            return "❌ Unexpected LLM response format. Please check the logs."

    except requests.exceptions.RequestException as req_err:
        print("❌ Network error:", req_err)
        return "Failed to connect to the LLM API."

    except Exception as e:
        print("❌ General error:", e)
        return "An error occurred while processing your request."
