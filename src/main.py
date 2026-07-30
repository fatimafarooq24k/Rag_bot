from src.generator import generate_answer
from src.index import index_document

def main():

    #step 1: Process Document

    path = input("Please provide your document path here: ")
    print("Document Loading Initiated...")
    try:
        received_info = index_document(path)
    except Exception as e:
        print("Document processing failed!")
        print(e)
        return
    
    print("Document Processing status: ", received_info["status"])

    print("Summary")
    print(f"Chunks created: {received_info['chunks_created']}")
    print(f"Embeddings created: {received_info['embeddings_created']}")
    print("Document created.\n You can now start chatting.")
    print("\n***\t-------------------------------------------------\t***\n")


    #step 2: Start Chatting
    print('''Hello! I'm your PDF Q/A Bot.
            Ask me questions about your uploaded document.
            Type "exit" to quit.''')
    while True: 
        try:
            print("\n------------------------\n")
            query = input("Ask your question: ") 

            if query.strip() == "":
                print("Please write something")
                continue

            if query.lower() == "exit":
                print("Thank you for using PDF Q/A Bot.\nGoodbye!")
                break

            answer = generate_answer(query)

            print(answer)

        except Exception as e:
            print("An error occurred. Try Again!")
            print(e)

if __name__ == "__main__":
    main()
