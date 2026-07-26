from src.chunker import chunk_text

print("Test 1: Normal Chunking")
text = "The big brown cat sat on the mat and ate a rat. After that it went on with chasing another rat."
chunks = chunk_text(text, chunk_size=12)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: ")
    print(chunk)
    print("-----------")

print("--------------------------------")

print("Test 2: Invalid Chuck Size")

text = "The Blossom of flowers in spring is truely a wonderful sight."

try:
    chunks = chunk_text(text, chunk_size=-1)
    print(chunks)
except ValueError as e:
    print(f"Error caught: {e}")

print("--------------------------------")

print("Test 3: Chunk Size Larger Than Text")

text = "Hello World!"
try:
    chunks = chunk_text(text, chunk_size=25)
    print(chunks)
except ValueError as e:
    print(f"Error caught: {e}")

print("--------------------------------")

print("Test 4: Empty Text")

text = ""
try:
    chunks = chunk_text(text, chunk_size=12)
    print(chunks)
except ValueError as e:
    print(f"Error caught: {e}")


print("--------------------------------")