import requests
import json

# def send_mcp_request(user_input):
#     url = 'http://localhost:8000/mcp'
#     data = {
#         'method': 'retrieve',
#         'context': {'input': user_input}
#     }
#     response = requests.post(url, json=data)
#     return response.json()
def send_mcp_request(user_input):
    url = 'http://localhost:8000/mcp'  
    headers = {'Content-Type': 'application/json'}

    request_payload = {
        "method": "generate",
        "context": {
            "user_input": user_input
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(request_payload))

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        return response.json()
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        return {"error": "Invalid response from server", "details": response.text}
