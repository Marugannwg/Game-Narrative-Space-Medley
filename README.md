# Game Narrative Medley Project

Welcome to the Game Narrative Medley Project repository! This is an ongoing project aimed to dive deep into the *mobile gacha game* narrative. For now, this place curated a sample corpus made from 'Arknights' story plot for concept testing.

My goal is to explore the intricacies of character interactions and story progression within the game using computational social science methods.

## Repository Structure

The repository currently has: 

- `corpus_creation.ipynb`: Contains scripts for cleaning and structuring the raw game text data into a ConvoKit corpus format. This also include some visualized usage case (e.g. interesting network plot of game characters~!)

- `LLM_interactions.ipynb`: Encapsulated functions to quickly interact with OpenAI, Mistral, and Anthropic API with prompt inputs. Includes code for classifying characters into major or non-major roles / archetypes using their LLMs. 

- `embed_text.ipynb` && `embedding_analyses.ipynb`: Features scripts for generating and analyzing word2vec, doc2vec and LLM embeddings; Contains the pipeline for retrieving the most relevant contexts to a given query using LLM embeddings; Q&A function with 'Arknights' context-awaring GPT Agent is also included -- look into the [embedding fold](data\Arknights_plot\embedding) to obtain the data if you want to try.

If you are looking for **Data Preparation**:
   - `raw_text_explore.ipynb` folder contains scripts that clean and transform raw game text data into a format that ConvoKit can use for conversation analysis.
   - `corpus_creation.ipynb` -- This is the actally implementations of a ConvoKit-compatible corpus. 


If you are exploring LLMs and story: try `corpus_creation.ipynb` and `embedding_analyses.ipynb` -- they have lots of plots and usage cases.
