# E-Commerce FAQ Agent

An intelligent agent built with LangChain that helps customers find products and answers their questions about an e-commerce platform. The agent uses natural language processing to understand user queries and provides relevant product recommendations and FAQ answers.

## Features

- Natural language product search with multiple filters (price, category, rating, stock)
- Smart FAQ matching using vector similarity search
- User-friendly Streamlit interface
- Supports complex queries combining multiple criteria

## Prerequisites

- Python 3.8+
- OpenAI API key

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

3. Set up your OpenAI API key:
   - Replace the API key in `main.py` with your key
   - Or set it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key'
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

- LangChain for agent orchestration
- OpenAI for natural language understanding
- FAISS for vector similarity search
- Streamlit for web interface
- Pandas for data handling 