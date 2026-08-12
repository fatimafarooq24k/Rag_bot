from src.retriever import find_relevant_chunks
from src.llm import generate_response
from src.reranker import Reranker
import src.config as cnfg

reranker = None

def generate_answer(query):
    global reranker

    if reranker is None:
        reranker = Reranker()

    if not isinstance(query, str):
        raise TypeError("Your prompt must be String.")

    if query.strip() == "":
        raise ValueError("Please enter a prompt.")

    retrieved_chunks = find_relevant_chunks(query, cnfg.TOP_K)

    unique_chunks = []
    seen = set()
    for chunk in retrieved_chunks:
        key = (chunk["page_number"], chunk["text"])
        if key not in seen:
            unique_chunks.append(chunk)
            seen.add(key)

    retrieved_chunks = unique_chunks

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
    6- Whenever you use information, cite it at the end of the sentence in exactly this format:
    [Page X]
    7- If multiple pages support the same statement, cite them exactly like this:
    [Pages X, Y, Z]
    8- Never use any other citation style such as (Page 1), Page 1, 【1】, or superscripts.
        
    Context:
    {context}
    
    Question:
    {query}

    Answer:
    Answer the question completely.

    For every requested topic:
    - Give a heading.
    - Give 3–8 bullet points.
    - Mention page numbers.
    - Combine information from multiple chunks.
    - Do not stop until every topic is covered.

    '''

    response = generate_response(prompt)

    return response


    