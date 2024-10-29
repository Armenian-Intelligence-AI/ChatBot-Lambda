AI Chatbot Service for API Gateway

This repository contains a set of AWS Lambda functions designed to manage and respond to user interactions via API Gateway. The functions are structured across 33 folders, with each folder named after a corresponding Lambda function.

Core Components

	1.	fbm-ai-chatbot-api
	•	Connects to API Gateway to handle user requests for chatbot interactions.
	•	Supports speech-to-text conversion as needed.
	2.	fbm-ai-chatbot-api-authorizer
	•	Authorizes API Gateway access using an API key.
	3.	fbm-ai-chatbot-controller
	•	Processes classified labels to generate responses for the chatbot API.
	•	Classification logic is housed in a separate repository: Armenian-Classifier.
