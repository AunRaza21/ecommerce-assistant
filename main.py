import pandas as pd
import os
from typing import List, Dict, Any
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EcommerceAgent:
    def __init__(self):
        self.products_df = pd.read_csv('Product_Statistics.csv')
        self.faq_df = pd.read_excel('FAQ.xlsx')
        
        # Setup Gemini
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Setup embedding model for FAQ matching
        self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
        self.setup_faq_vectorstore()

    def setup_faq_vectorstore(self):
        # Get questions and answers
        self.questions = self.faq_df['Question'].tolist()
        self.answers = self.faq_df['Answer'].tolist()
        
        # Create embeddings
        embeddings = self.sentence_transformer.encode(self.questions)
        
        # Initialize FAISS index
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add vectors to the index
        self.index.add(np.array(embeddings).astype('float32'))

    def query_products(self, query: str) -> List[Dict[str, Any]]:
        system_prompt = f"""
        You are a product filter expert. Analyze this query and extract filter conditions: {query}
        """
        
        filtered_df = self.products_df.copy()
        
        # Category mapping for common terms
        category_mapping = {
            'laptop': 'Computers',
            'laptops': 'Computers',
            'computer': 'Computers',
            'computers': 'Computers',
            'phone': 'Electronics',
            'phones': 'Electronics',
            'smartphone': 'Electronics',
            'smartphones': 'Electronics',
            'accessory': 'Accessories',
            'accessories': 'Accessories',
            'earbud': 'Accessories',
            'earbuds': 'Accessories',
            'watch': 'Wearables',
            'watches': 'Wearables',
            'smartwatch': 'Wearables',
            'smartwatches': 'Wearables'
        }
        
        # Category filtering - check both direct categories and mapped terms
        query_terms = query.lower().split()
        requested_category = None
        
        # First check for exact category matches
        for category in self.products_df['Category'].unique():
            if category.lower() in query.lower():
                requested_category = category
                break
        
        # If no exact match, check mapped terms
        if not requested_category:
            for term in query_terms:
                if term in category_mapping:
                    requested_category = category_mapping[term]
                    break
        
        # Apply category filter if found
        if requested_category:
            filtered_df = filtered_df[filtered_df['Category'] == requested_category]
        
        # Price filtering
        if "price" in query.lower() or "$" in query:
            try:
                # Extract price value after $ symbol
                price_str = query.split("$")[1].strip()
                # Get the first number after $
                max_price = float(''.join([c for c in price_str.split()[0] if c.isdigit() or c == '.']))
            except:
                # Try to find any number followed by word "budget" or similar terms
                price_words = ['budget', 'under', 'below', 'less than']
                query_words = query.lower().split()
                for i, word in enumerate(query_words):
                    if word in price_words and i > 0:
                        try:
                            max_price = float(''.join([c for c in query_words[i-1] if c.isdigit() or c == '.']))
                            break
                        except:
                            continue
            
            try:
                if "over" in query.lower() or "more than" in query.lower() or "above" in query.lower():
                    filtered_df = filtered_df[filtered_df['Price'] >= max_price]
                else:  # Default to "under" if no specific comparison is mentioned
                    filtered_df = filtered_df[filtered_df['Price'] <= max_price]
            except:
                pass
        
        # Rating filtering
        if "top-rated" in query.lower():
            filtered_df = filtered_df.sort_values('Rating', ascending=False)
        
        # Stock filtering
        if "in stock" in query.lower():
            filtered_df = filtered_df[filtered_df['Stock_Level'] > 0]
        
        # Always sort by rating if no specific sort is requested
        if not filtered_df.empty and 'Rating' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('Rating', ascending=False)
        
        return filtered_df.to_dict('records')

    def answer_faq(self, query: str) -> str:
        # Get embedding for the query
        query_embedding = self.sentence_transformer.encode([query])
        
        # Search in FAISS
        D, I = self.index.search(query_embedding.astype('float32'), 1)
        
        # Get the most similar question's index
        most_similar_idx = I[0][0]
        
        # Get corresponding answer
        return self.answers[most_similar_idx]

    def process_query(self, query: str) -> str:
        # Determine if this is a product query or FAQ
        prompt = f"""
        Determine if this is a product search query or a general FAQ question: {query}
        Just respond with either 'PRODUCT' or 'FAQ'.
        """
        
        response = self.model.generate_content(prompt)
        query_type = response.text.strip().upper()
        
        if query_type == 'PRODUCT':
            results = self.query_products(query)
            if not results:
                return "No products found matching your criteria."
            
            # Format product results
            response = "Here are the matching products:\n\n"
            for product in results[:5]:  # Show top 5 results
                response += f"- {product['Product_Name']}\n"
                response += f"  Price: ${product['Price']}\n"
                response += f"  Rating: {product['Rating']}/5.0\n"
                response += f"  Stock: {product['Stock_Level']} units\n\n"
            return response
        else:
            return self.answer_faq(query)

if __name__ == "__main__":
    agent = EcommerceAgent()
    
    # Example queries
    product_query = "Show me top-rated electronics under $500 in stock"
    faq_query = "What is your return policy?"
    
    print("Product Query Result:", agent.process_query(product_query))
    print("\nFAQ Query Result:", agent.process_query(faq_query)) 