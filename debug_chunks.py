from langchain_chroma import Chroma
from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

def debug_query(query_text: str):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    results = db.similarity_search_with_score(query_text, k=5)
    
    print(f"Query: {query_text}")
    print("="*50)
    
    for i, (doc, score) in enumerate(results):
        print(f"\n--- CHUNK {i+1} (Score: {score:.3f}) ---")
        print(f"Source: {doc.metadata.get('id', 'Unknown')}")
        print(f"Content: {doc.page_content[:300]}...")
        print("-" * 40)

if __name__ == "__main__":
    debug_query("What are the key terms and conditions in the lease agreement?") 