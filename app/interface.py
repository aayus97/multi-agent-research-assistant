import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from utils import extract_text_from_pdf
from agents.summarizer_agent import get_summary
from agents.reader_agent import extract_sections
from agents.critic_agent import critique_paper
from app.chunking import chunk_text, embed_chunks
from agents.qa_agent import answer_question_with_sources

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title and clear chat button
st.title("🧠 Multi-Agent Research Assistant")
if st.button("🧹 Clear Chat History"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# File upload
uploaded_file = st.file_uploader("Upload a research paper (PDF)", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Step 1: Extract raw text
    text = extract_text_from_pdf("temp.pdf")

    # Run chunking and embedding
    st.info("🔍 Chunking and embedding the document...")
    chunks = chunk_text(text)
    embed_chunks(chunks)
    st.success(f"✅ Document embedded into {len(chunks)} chunks.")

    # Step 2: Reader Agent extracts structure
    sections = extract_sections(text)
    st.subheader("📄 Extracted Sections")
    st.json(sections)

    # Step 3: Summarizer Agent
    summary = get_summary(text)
    st.subheader("📝 Summary")
    st.write(summary)

    # Step 4: Critic Agent
    st.subheader("🔍 Critique")
    st.write(critique_paper(summary + "\n\nOriginal:\n" + text[:1000]))

    # Q&A Interface
    st.subheader("💬 Ask a Question")
    user_q = st.text_input("Enter your question about the paper")

    if user_q:
        with st.spinner("Thinking..."):
            result = answer_question_with_sources(user_q)

            # Save to history
            st.session_state.chat_history.append({
                "question": user_q,
                "answer": result["answer"],
                "sources": result["sources"]
            })

# Display chat history using st.chat_message
for turn in st.session_state.chat_history:
    st.chat_message("user").markdown(turn["question"])
    st.chat_message("assistant").markdown(turn["answer"])

    with st.chat_message("assistant"):
        with st.expander("🔍 View retrieved context"):
            for i, src in enumerate(turn["sources"], start=1):
                st.markdown(f"**[Source {i}]**\n```text\n{src[:1000]}\n```")

        # Follow-up suggestions
        st.markdown("💡 **Follow-up Suggestions:**")
        st.markdown("- What are the limitations of this paper?")
        st.markdown("- How does this compare to prior work?")
        st.markdown("- What dataset or tools were used?")
