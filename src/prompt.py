prompt_template="""
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer and with a formal prompt give them the site url.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
and also answer the formal basic questions other than context text like hello greeting etc 
Helpful answer:
"""

# this needs some improvement