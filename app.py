
import streamlit as st
import fitz
import os
import base64
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI


def read_scanned_pdf(pdf_bytes):
    """Extract text from scanned PDF pages using Gemini vision."""
    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    extracted_pages = []

    for page_number, page in enumerate(pdf):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
        image_bytes = pix.tobytes("png")
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Transcribe all readable text from this scanned "
                                "document page, including handwriting. Preserve "
                                "equations and headings where possible. "
                                "Do not summarize or invent missing text."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.1,
        )

        page_text = response.choices[0].message.content
        extracted_pages.append(
            f"Page {page_number + 1}:\n{page_text}"
        )

    pdf.close()
    return "\n\n".join(extracted_pages)
    
load_dotenv()

client = OpenAI(
    base_url="https://api.meshapi.ai/v1",
    api_key=os.getenv("MESH_API_KEY")
)

MODEL = "google/gemini-2.5-flash"

MODEL = "google/gemini-2.5-flash"

MODEL = "google/gemini-2.5-flash"

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide"
)

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #080e1f, #101832, #0b1020);
    color: #f1f5ff;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111b32, #0b1223);
    border-right: 1px solid #263452;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p, label {
    color: #edf2ff !important;
}

h1 {
    font-size: 2.6rem !important;
    font-weight: 800 !important;
}

.stCaption, small {
    color: #aab8d5 !important;
}

[data-testid="stFileUploader"] {
    background: #17233d;
    border: 1px dashed #7774ff;
    border-radius: 16px;
    padding: 12px;
}

.stTextInput input {
    background: #17233d !important;
    color: white !important;
    border: 1px solid #635bff !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

.stButton button {
    background: linear-gradient(90deg, #5145ff, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 9px 20px;
    font-weight: 600;
}

.stButton button:hover {
    border: 1px solid #b7a7ff;
    color: white;
}

[data-testid="stExpander"] {
    background: #131f38;
    border: 1px solid #293b60;
    border-radius: 12px;
}

[data-testid="stTabs"] button {
    color: #c6d2ed;
}

hr {
    border-color: #293653;
}

.feature-card {
    background: linear-gradient(145deg, #192746, #111a30);
    border: 1px solid #34466d;
    border-radius: 18px;
    padding: 22px 18px;
    min-height: 155px;
    margin-bottom: 12px;
}

.feature-card h3 {
    color: #ffffff;
    font-size: 19px;
    margin-bottom: 10px;
}

.feature-card p {
    color: #bac9e7 !important;
    font-size: 14px;
}

.chat-card {
    background: linear-gradient(145deg, #14213c, #10192e);
    border: 1px solid #414c86;
    border-radius: 20px;
    padding: 24px;
    margin-top: 20px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------- SIDEBAR ----------
st.sidebar.markdown("# 📚 DocuMind AI")
st.sidebar.caption("YOUR PERSONAL STUDY ASSISTANT")
st.sidebar.divider()

st.sidebar.markdown("### 📁 Document Library")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

documents = {}


if uploaded_files:
    for file in uploaded_files:
        try:
            if file.name.lower().endswith(".pdf"):
                pdf_bytes = file.getvalue()

                # Extract selectable text first
                pdf = fitz.open(
                    stream=pdf_bytes,
                    filetype="pdf"
                )
                text = "\n".join(
                    page.get_text() for page in pdf
                )
                pdf.close()

                # Use Gemini if the PDF is scanned
                if len(text.strip()) < 50:
                    with st.spinner(
                        f"Reading scanned pages in {file.name}..."
                    ):
                        text = read_scanned_pdf(pdf_bytes)

            else:
                text = file.getvalue().decode(
                    "utf-8",
                    errors="replace"
                )

            documents[file.name] = text

        except Exception as e:
            st.sidebar.error(
                f"Error reading {file.name}: {e}"
            )

    st.sidebar.success(
        f"✅ {len(documents)} document(s) uploaded"
    )

selected_docs = st.sidebar.multiselect(
    "Choose documents to study",
    options=list(documents.keys()),
    default=list(documents.keys())
)

st.sidebar.divider()
st.sidebar.markdown("### ✨ Your Study Tools")
st.sidebar.markdown("💬 Ask your documents")
st.sidebar.markdown("📝 MCQ quizzes")
st.sidebar.markdown("🗂️ Flashcards")
st.sidebar.markdown("🔀 Flowcharts")

st.sidebar.divider()
st.sidebar.caption("Study smarter • Learn faster")


# ---------- MAIN DASHBOARD ----------
st.markdown("# ✨ Welcome to DocuMind AI")
st.markdown(
    "Your personal learning companion. "
    "Understand notes, revise faster, and learn visually."
)

st.markdown("---")

# Feature cards
col1, col2, col3, col4 = st.columns(4)

features = [
    (col1, "💬", "Ask Questions",
     "Get answers from your uploaded documents."),
    (col2, "🧠", "Flashcards",
     "Turn notes into quick revision cards."),
    (col3, "📝", "MCQ Quizzes",
     "Test your knowledge with practice questions."),
    (col4, "🔀", "Visual Learning",
     "Understand concepts through flowcharts.")
]

for col, emoji, title, description in features:
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div style="font-size:30px">{emoji}</div>
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------- APP TABS ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Ask Documents",
    "📝 MCQ Quiz",
    "🗂️ Flashcards",
    "🔀 Flowcharts"
])

with tab1:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    st.markdown("""
    <div class="chat-card">
        <h3>✨ Chat with your documents</h3>
        <p>Ask questions about your notes and study materials.</p>
    </div>
    """, unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.text_input(
        "Your question",
        placeholder="Ask anything about your documents...",
        key="chat_question"
    )

    if st.button("🚀 Ask AI", key="ask_ai"):
        st.session_state.chat_history.append({
    "role": "user",
    "content": question
})
        if not selected_docs:
            st.warning("Upload and select a document first.")
        elif not question.strip():
            st.warning("Please enter a question.")
        elif not os.getenv("MESH_API_KEY"):
            st.error("Mesh API key missing. Check your .env file.")
        else:
            # Find relevant passages in the selected documents
            chunks = []
            for name in selected_docs:
                text = documents[name]
                words = text.split()
                for start in range(0, len(words), 180):
                    chunk = " ".join(words[start:start + 180])
                    if chunk:
                        chunks.append((name, chunk))

            # Simple keyword-based retrieval
            question_words = {
                word.lower().strip(".,?!:;()[]")
                for word in question.split()
                if len(word) > 2
            }

            ranked = []
            for name, chunk in chunks:
                chunk_words = {
                    word.lower().strip(".,?!:;()[]")
                    for word in chunk.split()
                }
                score = len(question_words & chunk_words)
                if score > 0:
                    ranked.append((score, name, chunk))

            ranked.sort(key=lambda item: item[0], reverse=True)
            relevant = ranked[:5]

            if not relevant:
                st.warning(
                    "I couldn't find a relevant passage in the "
                    "selected documents. Try different keywords."
                )
            else:
                context = "\n\n".join(
                    f"Source: {name}\nPassage: {chunk}"
                    for _, name, chunk in relevant
                )

                try:
                    with st.spinner("Reading your documents..."):
                        response = client.chat.completions.create(
                            model=MODEL,
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Answer using only the supplied "
                                        "document passages. If they do not "
                                        "contain the answer, say so clearly. "
                                        "Cite the source filename."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": (
                                        f"Document passages:\n{context}\n\n"
                                        f"Question: {question}"
                                    )
                                }
                            ],
                            temperature=0.2
                        )


                    st.markdown("### 💡 Answer")
                    answer = response.choices[0].message.content
                    st.write(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                    st.caption(
                        "Answer generated from retrieved document passages."
                    )


                    with st.expander("📚 Retrieved source passages"):
                        for score, name, chunk in relevant:
                            st.markdown(f"**{name}**")
                            st.write(chunk)

                except Exception as e:
                    st.error(
                        f"Mesh API request failed: {e}"
                    )


with tab2:
    st.markdown("### 📝 Create a practice quiz")
    st.write("Generate MCQs based on your selected documents.")

    num_questions = st.slider(
        "Number of questions", 5, 20, 5, key="mcq_count"
    )

    if st.button("✨ Generate MCQs", key="generate_mcqs"):
        if not selected_docs:
            st.warning("Please upload and select a document first.")
        else:
            study_text = "\n\n".join(
                documents[name] for name in selected_docs
            )[:12000]

            try:
                with st.spinner("Generating your quiz..."):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Create multiple-choice questions using only "
                                    "the provided study notes. Return valid JSON "
                                    "only, as a list of objects with keys: "
                                    "question, options (a list of 4 strings), "
                                    "answer (exactly one option), explanation."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Create {num_questions} MCQs from these notes. "
                                    "Do not invent facts.\n\n" + study_text
                                ),
                            },
                        ],
                        temperature=0.3,
                    )

                import json

                raw = response.choices[0].message.content
                raw = raw.replace("```json", "").replace("```", "").strip()
                questions = json.loads(raw)

                st.session_state["mcq_questions"] = questions
                st.session_state["mcq_answers"] = {}
            except Exception as e:
                st.error(f"Quiz generation failed: {e}")

    questions = st.session_state.get("mcq_questions", [])

    if questions:
        for i, q in enumerate(questions):
            st.markdown(f"**Q{i + 1}. {q['question']}**")
            choice = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"mcq_answer_{i}",
                index=None,
            )
            if choice is not None:
                st.session_state["mcq_answers"][i] = choice

        if st.button("✅ Check Answers", key="check_mcqs"):
            score = 0
            for i, q in enumerate(questions):
                chosen = st.session_state["mcq_answers"].get(i)
                if chosen == q["answer"]:
                    score += 1
                    st.success(f"Q{i + 1}: Correct!")
                else:
                    st.error(
                        f"Q{i + 1}: Answer: {q['answer']}"
                    )
                st.caption(q.get("explanation", ""))

            st.metric("Your Score", f"{score}/{len(questions)}")



with tab3:
    st.markdown("### 🗂️ Quick Revision")
    st.write("Tap the card to reveal the answer.")

    if st.button("✨ Generate Flashcards", key="generate_flashcards"):
        if not selected_docs:
            st.warning("Upload and select a document first.")
        else:
            study_text = "\n\n".join(
                documents[name] for name in selected_docs
            )[:6000]

            try:
                with st.spinner("Creating flashcards..."):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Create 8 study flashcards from the notes. "
                                    "Return valid JSON only: a list of objects "
                                    'with "question" and "answer" string keys.'
                                )
                            },
                            {"role": "user", "content": study_text}
                        ],
                        temperature=0.3
                    )

                import json
                raw = response.choices[0].message.content
                raw = raw.replace("```json", "").replace("```", "").strip()
                cards = json.loads(raw)

                st.session_state["flashcards"] = cards
                st.session_state["card_index"] = 0
                st.session_state["card_flipped"] = False

            except Exception as e:
                st.error(f"Flashcard generation failed: {e}")

    cards = st.session_state.get("flashcards", [])

    if cards:
        if "card_index" not in st.session_state:
            st.session_state["card_index"] = 0
        if "card_flipped" not in st.session_state:
            st.session_state["card_flipped"] = False

        i = st.session_state["card_index"]
        card = cards[i]

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #242447, #443477);
                color: white;
                border-radius: 18px;
                padding: 35px 20px;
                min-height: 190px;
                text-align: center;
                border: 1px solid #7664bb;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="font-size:13px; opacity:0.8;">
                    {"ANSWER" if st.session_state.card_flipped else "QUESTION"}
                </div>
                <div style="font-size:22px; font-weight:600; margin-top:18px;">
                    {card["answer"] if st.session_state.card_flipped else card["question"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Use the button below to flip the card.")

        if st.button("🔄 Flip Card", key="flip_card", use_container_width=True):
            st.session_state["card_flipped"] = not st.session_state["card_flipped"]
            st.rerun()

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state["card_index"] = (i - 1) % len(cards)
                st.session_state["card_flipped"] = False
                st.rerun()

        with col2:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state["card_index"] = (i + 1) % len(cards)
                st.session_state["card_flipped"] = False
                st.rerun()

        st.caption(f"Card {i + 1} of {len(cards)}")





with tab4:
    st.markdown("### 🧠 AI Mind Map")
    st.caption("A compact, colourful map of your study notes.")

    if st.button("✨ Generate Mind Map", key="generate_flowchart"):
        if not selected_docs:
            st.warning("Upload and select a document first.")
        else:
            study_text = "\n\n".join(
                documents[name] for name in selected_docs
            )[:6000]

            try:
                with st.spinner("Creating your mind map..."):
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Create a compact study mind map using only "
                                    "the supplied notes. Return valid JSON only. "
                                    "Format: {\"title\":\"central topic\","
                                    "\"branches\":[{\"topic\":\"main idea\","
                                    "\"subtopics\":[\"detail 1\",\"detail 2\"]}]}. "
                                    "Create exactly 3 to 5 main branches, with "
                                    "1 to 2 short subtopics per branch. Keep "
                                    "every label under 6 words. Avoid paragraphs. "
                                    "Choose the most important concepts only."
                                )
                            },
                            {"role": "user", "content": study_text}
                        ],
                        temperature=0.2
                    )

                import json
                raw = response.choices[0].message.content.strip()
                raw = raw.replace("```json", "").replace("```", "").strip()
                mindmap = json.loads(raw)
                mindmap["branches"] = mindmap["branches"][:5]

                for branch in mindmap["branches"]:
                    branch["subtopics"] = branch.get("subtopics", [])[:2]

                st.session_state["mindmap"] = mindmap

            except Exception as e:
                st.error(f"Mind map generation failed: {e}")

    mindmap = st.session_state.get("mindmap")

    if mindmap:
        import json

        colors = [
            "#FCA5A5", "#93C5FD", "#86EFAC",
            "#FDE68A", "#D8B4FE"
        ]

        def safe_label(value):
            return json.dumps(str(value))

        lines = [
            "graph MindMap {",
            'layout=twopi;',
            'root="central";',
            'overlap=false;',
            'splines=true;',
            'bgcolor="transparent";',
            'pad=0.2;',
            'ranksep=1.0;',
            'node [shape=box, style="rounded,filled", fontname="Arial", fontsize=11, margin="0.16,0.10", color="#FFFFFF", penwidth=1.5];',
            'edge [color="#9CA3AF", penwidth=1.8];',
            f'"central" [label={safe_label(mindmap["title"])}, fillcolor="#C4B5FD", fontsize=14, penwidth=2.5];'
        ]

        node_count = 0

        for i, branch in enumerate(mindmap["branches"]):
            branch_id = f"branch{i}"
            color = colors[i % len(colors)]

            lines.append(
                f'"{branch_id}" [label={safe_label(branch["topic"])}, fillcolor="{color}", fontsize=12];'
            )
            lines.append(f'"central" -- "{branch_id}";')

            for j, subtopic in enumerate(branch.get("subtopics", [])):
                if node_count >= 12:
                    break

                sub_id = f"sub{i}_{j}"
                lines.append(
                    f'"{sub_id}" [label={safe_label(subtopic)}, fillcolor="#F3F4F6", color="{color}"];'
                )
                lines.append(f'"{branch_id}" -- "{sub_id}";')
                node_count += 1

        lines.append("}")

        st.graphviz_chart("\n".join(lines), use_container_width=True)

        st.caption("Central topic → coloured branches → key details")



# ---------- DOCUMENT PREVIEW ----------
with st.expander("🔍 Preview extracted document text"):
    if selected_docs:
        for name in selected_docs:
            st.markdown(f"**📄 {name}**")
            st.text(documents[name][:3000])
            st.caption(
                f"{len(documents[name]):,} characters extracted"
            )
    else:
        st.info("Upload a PDF or TXT file to preview its text.")