# Day 1 — What Does an AI System Actually Do?

## AI Pipeline

Every AI system follows the same basic flow: **Input → Processing → Output**. There's no magic in the middle — just data going in, a model transforming it based on patterns it learned during training, and a result coming out.

<img width="807" height="217" alt="image" src="https://github.com/user-attachments/assets/7e7046c1-dc28-4003-a956-2622a2ccce2b" />


## Real-World AI Products Mapped to the Pipeline

| Product | Input | Processing | Output |
|---|---|---|---|
| **ChatGPT** | Your typed prompt | Language model predicts the most likely next words based on patterns learned from training data | Generated text response |
| **Google Translate** | Text in a source language | Model maps sentence structure and meaning from one language to another | Translated text |
| **Spotify Recommendations** | Your listening history and skips | Model finds patterns in what similar users enjoyed | Suggested playlist or songs |

## How a Chatbot Works 

A chatbot works by taking your typed message as input and converting it into a numerical representation the model can understand. It then processes this representation through a neural network trained on massive amounts of text, which has learned statistical patterns of how language flows. Based on these patterns, the model predicts the most likely next word, then the next, one at a time, building a full response. This process repeats token by token until the response is complete or reaches a natural stopping point. Finally, the generated tokens are converted back into readable text and displayed to you as the output — there's no understanding in the human sense, just very sophisticated pattern matching.

