# Game-Narrative-Space-Medley

A project focusing on *Computationally* understanding the narrative structures, themes, and **character** dynamics within a *game's storytelling* and its surrounding ecosystem, i.e., commentaries and fan-created content. Some related research questions:

- How different characters (e.g. protagonists versus antagonists; main characters versus mascot-like figures) are portraited differently in-game and perceived differently by audiences?
- What are some key qualities and themes surrounding those popular characters? How these topics and themes differ in game and out game?
- How moral judgement might differ in-game versus in fan-created content? (i.e., We might expect a character is perceived in a different or complicated manner when it comes to the commentary and fan creation around them?)
- …

Data Collection:

- In-game Dialogues: Scrape and/or extract all dialogues from (at least one) game. This represent the context of the original game.
    - Currently prepared corpora includes all story telling of *Arknights*.
- Community Content: Collecting discussion posts, commentary, and fanfiction from forums, social media platforms, and fanfiction websites, representing variously contexts developed around game culture and ecosystems
    - Currently exploring *Reddit* and *AO3* API. Example data include keyword search on several *Arknights* characters to extract all discussion and fanfiction involve those characters.

Methodologies:

- Text preprocessing: In-game dialogues and blogs/discussions surrounding the game often have an informal nature, which means they may require extra cleaning and normalization before proceeding.
- Text Embedding: The key aspect of the project is to explore text-to-vec and NLP techniques. Besides direct Word2Vec or Doc2Vec, I’m also planning to use BRET, LLaMa2, or GPT for generating text embedding. These embeddings are the core tools to capture the contextual meaning of words and phrases, allowing deeper analysis of narrative.

(With the embedding available…)

- Exploring vector space: Compare and contrast the similarity of the different embedding among in-game and out-game text. Many question can be potentially explored with the similarity:
    - Simply, what characters are perceived similarly in different space?
    - If we project text embedding around a dialogue to a semantic space (with the help of LLM as baseline, e.g. good/bad, strong/weak….), how might this differ in-game versus out-game?
- Clustering and Topic Modeling: This my help identify common narrative themes and character archetypes within game and fan contents.
