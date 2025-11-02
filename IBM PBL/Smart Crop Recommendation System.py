import requests
import json

# ==============================
# IBM Cloud Model Integration
# ==============================

# Replace this with your actual IBM Cloud API key
API_KEY = "4to2Vmra8WuUn-WWlqaFHGA1ZgHh_Z3R52O1TZhbebpA"

# Get the IAM token
token_response = requests.post(
    'https://iam.cloud.ibm.com/identity/token',
    data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}
)

mltoken = token_response.json()["access_token"]
print("✅ Token retrieved successfully!")

# IBM Model deployment URL (replace with your own endpoint)
deployment_url = "https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/058ad653-ab84-4051-bcb2-e7c02809adb8/predictions?version=2021-05-01"

# Define headers
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# ==============================
# Input Section
# ==============================

# Example: you can take inputs dynamically or fix them manually
Nitrogen = float(input("Enter Nitrogen value: "))
Phosphorus = float(input("Enter Phosphorus value: "))
Potassium = float(input("Enter Potassium value: "))
Temperature = float(input("Enter Temperature (°C): "))
Humidity = float(input("Enter Humidity (%): "))
pH_Value = float(input("Enter pH value: "))
Rainfall = float(input("Enter Rainfall (mm): "))

# Prepare payload for prediction
payload_scoring = {
    "input_data": [
        {
            "fields": [
                "Nitrogen", "Phosphorus", "Potassium",
                "Temperature", "Humidity", "pH_Value", "Rainfall"
            ],
            "values": [[Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH_Value, Rainfall]]
        }
    ]
}

# Send request for prediction
response_scoring = requests.post(
    deployment_url,
    json=payload_scoring,
    headers=header
)

# ==============================
# Output Section
# ==============================

print("\n=== Scoring Response ===")
try:
    result = response_scoring.json()
    #print(json.dumps(result, indent=4))  # neatly print full response

    # Extract predicted value (if available)
    predictions = result.get("predictions", [])
    if predictions:
        predicted_value = predictions[0].get("values", [[]])[0][0]
        print(f"\n🌱 Predicted Result: {predicted_value}")
    else:
        print("⚠️ No predictions found in response.")

except ValueError:
    print("Invalid JSON received:")
    print(response_scoring.text)
except Exception as e:
    print(f"An unexpected error occurred: {e}")