import streamlit as st
from main import EcommerceAgent

st.set_page_config(page_title="E-Commerce Assistant", layout="wide")

st.title("E-Commerce Product Assistant")

if 'agent' not in st.session_state:
    try:
        st.session_state.agent = EcommerceAgent()
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        st.stop()

st.write("""
This assistant can help you with:
- Finding products based on category, price, rating, and stock level
- Answering general questions about our services
""")

query = st.text_input("What would you like to know?", 
                     placeholder="e.g., Show me top-rated electronics under $500 in stock")

if query:
    with st.spinner("Processing your request..."):
        try:
            response = st.session_state.agent.process_query(query)
            st.write(response)
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

st.divider()

st.markdown("""
### Example Queries:
- Show me top-rated electronics under $500 in stock
- What laptops are available under $1500?
- Tell me about your return policy
- How can I track my order?
""") 