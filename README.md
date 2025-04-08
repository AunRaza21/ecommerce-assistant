# E-Commerce FAQ Agent

An intelligent agent built with Google's Gemini that helps customers find products and answers their questions about an e-commerce platform. The agent uses natural language processing to understand user queries and provides relevant product recommendations and FAQ answers.

## Features

- Natural language product search with multiple filters (price, category, rating, stock)
- Smart FAQ matching using vector similarity search
- User-friendly Streamlit interface
- Supports complex queries combining multiple criteria

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd faq-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Create a `.env` file in the root directory
   - Add your Gemini API key:
   ```
   GOOGLE_API_KEY='your-gemini-api-key'
   ```

4. Prepare your data:
   - Place your product data in `Product_Statistics.csv`
   - Place your FAQ data in `FAQ.xlsx`

## Running the Application

Start the Streamlit interface:
```bash
streamlit run app.py
```

## Example Queries

Product Search:
- "Show me top-rated electronics under $500 in stock"
- "What laptops are available under $1500?"
- "Find accessories with rating above 4.5"

FAQ Questions:
- "What is your return policy?"
- "How can I track my order?"
- "Do you offer international shipping?"

## Project Structure

- `main.py`: Core agent implementation with product search and FAQ handling
- `app.py`: Streamlit user interface
- `requirements.txt`: Project dependencies
- `Product_Statistics.csv`: Sample product database
- `FAQ.xlsx`: Frequently asked questions and answers

## Technologies Used

- Google Gemini for natural language understanding
- FAISS for vector similarity search
- Streamlit for web interface
- Pandas for data handling 