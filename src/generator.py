from src.retriever import find_relevant_chunks
from src.llm import generate_response
from src.reranker import Reranker
import src.config as cnfg

reranker = Reranker()

def generate_answer(query):

    if not isinstance(query, str):
        raise TypeError("Your prompt must be String.")

    if query.strip() == "":
        raise ValueError("Please enter a prompt.")

    retrieved_chunks = find_relevant_chunks(query, cnfg.TOP_K)

    reranked_chunks = reranker.rerank(query, retrieved_chunks, cnfg.RERANK_TOP_K)

    context = ""
    for chunk in reranked_chunks:
        context += (
            f"(Page: {chunk['page_number']})\n"
            f"{chunk['text']}\n\n" 

        )
    prompt = f'''
    Instructions:
    1- For the question, answer from the given chunks only. 
    2- If the provided context does not contain the answer, respond exactly with: 
            This Information is not present in the provided document.
    3- If multiple chunks discuss the same topic, combine them into one answer.
    4- If information is partial, say that it is partial.
    5- Do not invent facts.
    6- Whenever you use information, include its page number in the answer.
    7- If multiple pages support the same point, cite all of them.
    
    Context:
    {context}
    
    Question:
    {query}

    Answer:

    '''

    response = generate_response(prompt)

    return response


    