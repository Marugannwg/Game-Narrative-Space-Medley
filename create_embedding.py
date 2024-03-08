import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from tqdm.auto import tqdm
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm  # for the loading bar
import convokit



def get_embedding(text, model="text-embedding-3-large"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def get_dialogue_text(utterance):
    speaker = utterance.speaker.id
    dialogue = utterance.text
    return f"{speaker}: {dialogue}\n"



def get_conversation_chunks(convo_id, max_length=2000):
    text = ""
    chunks = []
    
    for utt in corpus.get_conversation(convo_id).iter_utterances():
        dialogue_text = get_dialogue_text(utt)
        # Check if adding this dialogue exceeds the max_length
        if len(text + dialogue_text) > max_length:
            # Save current chunk and start a new one
            chunks.append(text)
            text = dialogue_text
        else:
            text += dialogue_text

    # Add the last chunk if it's not empty
    if text:
        chunks.append(text)
    
    return chunks

def process_conversation_chunks(convo_id):
    chunks = get_conversation_chunks(convo_id)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    return convo_id, embeddings

def process_and_write_chunk(convo_id, text_chunk):
    # Process the text chunk to obtain the embedding
    embedding = get_embedding(text_chunk)
    # Convert the embedding array into a string representation
    embedding_str = " ".join(map(str, embedding))
    
    # Acquire the lock before writing to the CSV file
    with lock:
        with open(filename, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the text chunk, its corresponding embedding, and the conversation ID to the CSV
            writer.writerow([text_chunk, embedding_str, convo_id])




output_dir = "D:/MACSS PROGRAM/30122/MACS-60000-2024-Winter/data/Arknights_plot/corpus"
# Load the corpus from the saved directory
corpus = convokit.model.corpus.Corpus(output_dir)

client = OpenAI()

# Filename for the CSV output
filename = "conversation_embeddings_1.csv"

# Initialize a lock for thread-safe writing to the CSV file
lock = Lock()

if __name__ == "__main__":
    # Open the CSV file and write the header
    with open(filename, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Text Chunk", "Embedding", "Convo ID"])

    # Adjust the number of workers based on your system's capabilities
    num_workers = 25

    conversation_ids = [convo.id for convo in corpus.iter_conversations()]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # List to keep track of futures
        futures = []
        
        # Iterate through conversation IDs and their text chunks
        for convo_id in conversation_ids:
            text_chunks = get_conversation_chunks(convo_id)
            for text_chunk in text_chunks:
                # Submit the processing and writing task for each text chunk
                futures.append(executor.submit(process_and_write_chunk, convo_id, text_chunk))

        # Using tqdm to display a loading bar
        for future in tqdm(as_completed(futures), total=len(futures)):
            _ = future.result()  # getting the result to handle exceptions if any