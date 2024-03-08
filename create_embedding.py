import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from tqdm.auto import tqdm
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.auto import tqdm  # for the loading bar
import convokit


def get_embedding(client, text, model="text-embedding-3-large"):
    """
    Get the embedding for a given text using the OpenAI API.

    Args:
    text (str): The input text.
    model (str): The name of the model to use for the embedding.
    """
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def get_dialogue_text(utterance):
    """
    Get the text representation of a dialogue from an utterance.

    Args:
    utterance (convokit.Utterance): The utterance object.
    """
    speaker = utterance.speaker.id
    dialogue = utterance.text
    return f"{speaker}: {dialogue}\n"


def get_conversation_chunks(corpus, convo_id, max_length=500):
    """
    Split a conversation into chunks of text with a maximum length.

    Args:
    convo_id (str): The conversation ID.
    max_length (int): The maximum length of each text chunk.
    """
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

def process_conversation_chunks(corpus, convo_id):
    """
    Process the text chunks of a conversation to obtain their embeddings.

    Args:
    convo_id (str): The conversation ID.

    Returns:
    convo_id (str): The conversation ID.
    embeddings (list): The list of embeddings for the text chunks.
    """
    chunks = get_conversation_chunks(corpus, convo_id)
    embeddings = [get_embedding(client, chunk) for chunk in chunks]
    return convo_id, embeddings

def process_and_write_chunk(client, convo_id, text_chunk, lock, filename):
    """
    Process a text chunk to obtain its embedding and write it to a CSV file.

    Args:
    convo_id (str): The conversation ID.
    text_chunk (str): The text chunk. 
    """
    # Process the text chunk to obtain the embedding
    embedding = get_embedding(client, text_chunk)
    # Convert the embedding array into a string representation
    embedding_str = " ".join(map(str, embedding))
    
    # Acquire the lock before writing to the CSV file
    with lock:
        with open(filename, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the text chunk, its corresponding embedding, and the conversation ID to the CSV
            writer.writerow([text_chunk, embedding_str, convo_id])






if __name__ == "__main__":
    input_dir = "data/Arknights_plot/corpus"
    # Load the corpus from the saved directory
    corpus = convokit.model.corpus.Corpus(input_dir)

    client = OpenAI()

    # Filename for the CSV output
    filename = "conversation_embeddings_1.csv"

    # Initialize a lock for thread-safe writing to the CSV file
    lock = Lock()
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
            text_chunks = get_conversation_chunks(corpus, convo_id)
            for text_chunk in text_chunks:
                # Submit the processing and writing task for each text chunk
                futures.append(executor.submit(process_and_write_chunk, 
                                                  client,
                                               convo_id, 
                                               text_chunk,
                                                lock,
                                                filename
                                               ))

        # Using tqdm to display a loading bar
        for future in tqdm(as_completed(futures), total=len(futures)):
            _ = future.result()  # getting the result to handle exceptions if any