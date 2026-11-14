import streamlit as st

from openai import OpenAI
import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="EyeCare AI",
    page_icon="👁️",
    layout="centered"
)

# ==========================================
# GROQ API CLIENT
# ==========================================

try:
    api_key = st.secrets["GROQ_API_KEY"]

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        timeout=30.0
    )

except Exception:
    st.error(
        "Groq API key not found. Please configure "
        "GROQ_API_KEY in .streamlit/secrets.toml"
    )
    st.stop()

MODEL = "openai/gpt-oss-20b"

# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are EyeCare AI, a friendly and responsible
eye care information assistant.

Your purpose is to provide general educational
information about eye health.

YOUR RESPONSIBILITIES:

1. Answer questions related to eye health.
2. Explain eye conditions in simple language.
3. Discuss general information about:
   - Dry eyes
   - Red eyes
   - Blurry vision
   - Eye strain
   - Watery eyes
   - Itchy eyes
   - Cataracts
   - Glaucoma
   - Conjunctivitis
4. Provide general eye care tips.
5. Explain the 20-20-20 screen rule.
6. Share general information about glasses
   and contact lenses.
7. Suggest healthy foods for eye health.
8. Encourage regular eye examinations.

MEDICAL SAFETY RULES:

1. Never diagnose a disease.
2. Never prescribe medicines.
3. Never recommend prescription eye drops.
4. Never claim to replace an eye doctor.
5. Never tell users their symptoms are harmless
   without proper medical evaluation.
6. Do not recommend self-medication.
7. For sudden vision loss, severe eye pain,
   eye injury, chemical exposure, new flashes
   or floaters, or a curtain-like shadow in vision,
   recommend immediate emergency eye care.
8. For chemical exposure, advise immediately
   rinsing the eye with clean running water while
   arranging emergency medical assistance.

CHATBOT BEHAVIOR:

1. Respond in the same language as the user.
2. Keep answers friendly and understandable.
3. Use bullet points when helpful.
4. If a question is unrelated to eye care,
   politely explain your specialization.
5. Ask relevant follow-up questions when needed.

IMPORTANT:
You are an AI educational assistant, NOT a doctor.
You provide general information, not diagnosis
or treatment.
"""

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""


<style>

/* Main Background */
.stApp {
    background-color: #0A192F;
    color: #FFFFFF;
}

/* Main Content */
.main .block-container {
    max-width: 900px;
    padding-top: 2rem;
}

/* Header */
.main-title {
    text-align: center;
    color: #FFFFFF;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Divider */
hr {
    border-color: #2563EB;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: #142B4A;
    border: 1px solid #2563EB;
    border-radius: 15px;
    padding: 16px;
    margin-bottom: 12px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #10233F;
    border-right: 1px solid #2563EB;
}

/* Sidebar Headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF;
}

/* Normal Text */
.stMarkdown p {
    color: #FFFFFF;
}

/* Buttons */
.stButton > button {
    background-color: #2563EB;
    color: #FFFFFF;
    border: 1px solid #3B82F6;
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
    transition: 0.3s;
}

/* Button Hover */
.stButton > button:hover {
    background-color: #FFFFFF;
    color: #1D4ED8;
    border: 1px solid #FFFFFF;
}

/* Chat Input */
[data-testid="stChatInput"] {
    background-color: #142B4A;
    border: 1px solid #2563EB;
    border-radius: 14px;
}

/* Info Box */
[data-testid="stAlert"] {
    background-color: #142B4A;
    border: 1px solid #2563EB;
    border-radius: 12px;
    color: #FFFFFF;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #2563EB;
}

/* Text Input */
input, textarea {
    background-color: #142B4A !important;
    color: #FFFFFF !important;
}

/* Headings */
h1, h2, h3 {
    color: #FFFFFF;
}

.st-emotion-cache-14vh5up {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: 0px;
    pointer-events: auto;
    position: relative;
    z-index: 999990;
    background: #000 !important;
}

.st-emotion-cache-6shykm {
    width: 100%;
    padding: 1rem 1rem 3.5rem;
    background: #000 !important;
    max-width: 736px;
}

.st-emotion-cache-1bdk92a {
    background-color: #ffff;
    
    position: relative;
    display: flex;
    flex-direction: column;
    -webkit-box-align: stretch;
    align-items: stretch;
    flex: 1 1 0%;
    padding: 0.75rem 1rem;
    gap: 0.5rem;
    border-radius: 0.5rem;
    box-sizing: border-box;
}

<style>
@su

</style>


""", unsafe_allow_html=True)

# ==========================================
# INITIALIZE CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">👁️ EyeCare AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Virtual Eye Care Assistant</div>',
    unsafe_allow_html=True
)

st.divider()

st.info(
    "Welcome to EyeCare AI! Ask questions about "
    "eye health, dry eyes, eye strain, vision care "
    "and healthy habits."
)

st.warning(
    "This chatbot provides educational information "
    "only. It cannot diagnose or treat eye conditions."
)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("👁️ EyeCare AI")

    st.write(
        "Your AI-powered eye health information assistant."
    )

    st.divider()

    st.subheader("What I Can Help With")

    st.write("👁️ Eye Health Information")
    st.write("💻 Computer Eye Strain")
    st.write("👓 Glasses & Contact Lenses")
    st.write("🥗 Eye Healthy Nutrition")
    st.write("💧 Dry Eye Care")
    st.write("🔍 Common Eye Conditions")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        st.rerun()

    st.divider()

    st.caption(
        "For urgent eye symptoms, seek professional "
        "medical attention immediately."
    )

# ==========================================
# SUGGESTED QUESTIONS
# ==========================================

st.subheader("💡 Suggested Questions")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Why do my eyes feel dry?",
        use_container_width=True
    ):

        st.session_state.user_question = (
            "Why do my eyes feel dry?"
        )

        st.rerun()

with col2:

    if st.button(
        "How can I reduce eye strain?",
        use_container_width=True
    ):

        st.session_state.user_question = (
            "How can I reduce eye strain?"
        )

        st.rerun()

col3, col4 = st.columns(2)

with col3:

    if st.button(
        "What is the 20-20-20 rule?",
        use_container_width=True
    ):

        st.session_state.user_question = (
            "Explain the 20-20-20 rule."
        )

        st.rerun()

with col4:

    if st.button(
        "Foods for healthy eyes?",
        use_container_width=True
    ):

        st.session_state.user_question = (
            "Which foods support eye health?"
        )

        st.rerun()

st.divider()

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for msg in st.session_state.messages:

    if msg["role"] != "system":

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input(
    "Ask your eye care question here..."
)

# Suggested question handling

if "user_question" in st.session_state:

    prompt = st.session_state.user_question

    del st.session_state.user_question

# ==========================================
# GENERATE AI RESPONSE
# ==========================================

if prompt:

    # Display user message

    with st.chat_message("user"):

        st.markdown(prompt)

    # Save user message

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate assistant response

    with st.chat_message("assistant"):

        with st.spinner(
            "👁️ EyeCare AI is thinking..."
        ):

            try:

                response = client.chat.completions.create(

                    model=MODEL,

                    messages=st.session_state.messages,

                    temperature=0.5,

                    max_tokens=1000
                )

                reply = (
                    response.choices[0].message.content
                    or "Sorry, I could not generate a response."
                )

                st.markdown(reply)

            except Exception as e:

                st.error(
                    f"API Error: {str(e)}"
                )

                reply = (
                    "Sorry, I am unable to respond right now. "
                    "Please check your internet connection "
                    "and try again."
                )

    # Save assistant response

    st.session_state.messages.append({

        "role": "assistant",

        "content": reply

    })
