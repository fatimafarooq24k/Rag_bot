from src.embedder import create_embeddings

print("Test 1: Normal Functionality Check")

chunks = [
    "Artificial intelligence is interesting.",
    "Machine learning is a branch of AI."
]
embeddings = create_embeddings(chunks)
print(type(embeddings), "\n", embeddings.shape)

print("------------------------------")

print("Test 2: Empty Chunks List")

chunks = []

try:
    embeddings = create_embeddings(chunks)
except ValueError as e:
    print(f"Error caught: {e}")

print("------------------------------")

print("Test 3: Another Datatype Check")

chunks = ["abc", 56, "he is 21 years old"]
try:
    embeddings = create_embeddings(chunks)
except ValueError as e:
    print(f"Error caught: {e}")

print("------------------------------")