from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

SYSTEM_PROMPT = """
You are a website-specific assistant.
Answer ONLY using the provided context.
If the answer is not present, reply exactly:
"The answer is not available on the provided website."
"""

def get_qa_chain(vectordb):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
        memory=memory
    )

    return qa_chain
