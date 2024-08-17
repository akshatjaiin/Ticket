# Albert Hall Museum Ticket Booking Chatbot

This project is a virtual chatbot for booking tickets to the Albert Hall Museum in Jaipur, India. The chatbot interacts with users, collects necessary information, and helps them book tickets while maintaining a friendly and joyful conversation. It uses Google Generative AI (Gemini) for natural language processing.

## Features

- **Ticket Booking**: The chatbot assists users in booking tickets to the Albert Hall Museum by collecting all necessary details such as the number of tickets, names, ages, nationality, and student status.
- **Friendly Interaction**: The chatbot is designed to be creative, friendly, and helpful while interacting with users.
- **Automated JSON Handling**: The chatbot extracts user information and returns it in a structured JSON format.
- **Safety Settings**: The chatbot is configured with safety settings to avoid harmful content.
- **Payment Processing (Stub)**: The script includes a placeholder for integrating payment processing.
- **Retry Logic**: The chatbot uses retry logic to handle transient errors in API communication.

## Prerequisites

- Python 3.7 or higher
- Google Generative AI SDK (`google-generativeai`)
- `python-dotenv` for environment variable management

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/albert-hall-museum-chatbot.git
   cd albert-hall-museum-chatbot

