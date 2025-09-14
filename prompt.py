from langchain.prompts import PromptTemplate

QUERY_PROMPT = PromptTemplate(
 input_variables=["question"],
 template=
 """
You are an AI assistant. Your task is to take the user’s question 
and, if needed, rephrase it slightly so that it retrieves the most relevant  
and precise context from a vector database built on the provided Finance Bill document.

The goal is to maximize the chance of finding exact or very close answers 
within the document.

User Question:
{question}
"""

)

ANSWER_PROMPT = PromptTemplate(
 input_variables=["context", "question"],
 template=
 """
You are an AI assistant for question-answering tasks.
Use only the following context extracted from the Finance Bill PDF:


Context:
{context}

Question:
{question}

Instructions:
- If the answer is in the context, provide a clear and concise response.
- If the information is NOT in the context, say:
  "The provided Finance Bill document does not contain information to answer that question."


Answer:
"""

)

