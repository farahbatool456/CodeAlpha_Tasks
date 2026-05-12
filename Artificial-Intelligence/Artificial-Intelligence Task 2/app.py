# app.py
# ============================================================
# MAIN STREAMLIT APPLICATION
# 
# This is the entry point of the FAQ Chatbot.
# Run with: streamlit run app.py
#
# ARCHITECTURE:
# app.py (UI layer) → chatbot.py (NLP engine) → utils/ (helpers)
#                                              → faq_data.json (data)
# ============================================================

import streamlit as st
import time
from datetime import datetime

# Import the chatbot engine
from chatbot import FAQChatbot

# ── Page Configuration (must be first Streamlit call) ─────
st.set_page_config(
    page_title="FAQ Chatbot | AI-Powered Q&A",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ── CSS Loader ────────────────────────────────────────────
def load_css():
    """
    Loads custom CSS from the styles/chat.css file.
    Falls back to inline CSS if the file is not found.
    """
    try:
        with open("styles/chat.css", "r") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Minimal fallback CSS if the file is missing
        st.markdown("""
        <style>
        .user-bubble { background: #667eea; color: white; padding: 12px 18px;
                       border-radius: 18px 18px 4px 18px; max-width: 70%;
                       margin-left: auto; margin-bottom: 8px; }
        .bot-bubble  { background: #f0f4ff; color: #1a1f36; padding: 12px 18px;
                       border-radius: 18px 18px 18px 4px; max-width: 75%;
                       margin-bottom: 8px; }
        </style>
        """, unsafe_allow_html=True)


# ── Session State Initialization ──────────────────────────
def init_session_state():
    """
    Initializes Streamlit session state variables.
    Session state persists data across reruns (like a page refresh).
    
    Without session state, chat history would reset on every interaction.
    """
    if 'chat_history' not in st.session_state:
        # List of dicts: each dict = one message (user or bot)
        st.session_state.chat_history = []

    if 'chatbot' not in st.session_state:
        # The chatbot instance — loaded once, reused across messages
        st.session_state.chatbot = None

    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = "All Categories"

    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False

    if 'total_queries' not in st.session_state:
        st.session_state.total_queries = 0

    if 'successful_matches' not in st.session_state:
        st.session_state.successful_matches = 0

    if 'input_key' not in st.session_state:
        # Used to clear the text input after sending
        st.session_state.input_key = 0

    if 'pending_message' not in st.session_state:
        st.session_state.pending_message = None


# ── Chatbot Initialization ─────────────────────────────────
@st.cache_resource
def create_chatbot():
    """
    Creates and loads the FAQChatbot instance.
    
    @st.cache_resource means this function runs ONCE and the result
    is cached. If the app reruns (e.g., user types something),
    we reuse the same chatbot object instead of reloading.
    
    Returns:
        FAQChatbot: Initialized chatbot instance
    """
    bot = FAQChatbot(faq_filepath="faq_data.json")
    return bot


def get_or_load_chatbot(category: str = "All Categories") -> FAQChatbot:
    """
    Gets the cached chatbot or reloads it if category changed.
    
    Args:
        category (str): Currently selected FAQ category
    
    Returns:
        FAQChatbot: Ready-to-use chatbot instance
    """
    if st.session_state.chatbot is None:
        bot = create_chatbot()
        bot.load_data(category_filter=category)
        st.session_state.chatbot = bot
    elif st.session_state.chatbot.current_category != category:
        # Category changed — reload the TF-IDF model with new filter
        st.session_state.chatbot.reload_with_category(category)

    return st.session_state.chatbot


# ── Chat Message Rendering ────────────────────────────────

def render_user_message(text: str, timestamp: str):
    """Renders a user message bubble (right-aligned, purple gradient)."""
    st.markdown(f"""
    <div class="user-message">
        <div>
            <div class="user-bubble">{text}</div>
            <div class="message-time" style="text-align:right">{timestamp}</div>
        </div>
        <div class="user-avatar">👤</div>
    </div>
    """, unsafe_allow_html=True)


def render_bot_message(response: dict, timestamp: str):
    """
    Renders a bot message bubble (left-aligned, light blue).
    Also shows confidence score and category tag if available.
    """
    answer_text = response.get('answer', '')
    confidence = response.get('confidence', 0.0)
    confidence_label = response.get('confidence_label', '')
    category = response.get('category', '')
    status = response.get('status', '')

    # Choose confidence badge style
    if confidence_label == 'High':
        badge_class = 'confidence-high'
        badge_icon = '✅'
    elif confidence_label == 'Medium':
        badge_class = 'confidence-medium'
        badge_icon = '⚠️'
    else:
        badge_class = 'confidence-low'
        badge_icon = '❓'

    # Build optional badges HTML
    badges_html = ""
    if status == 'matched' or status == 'low_confidence':
        badges_html += f"""
        <span class="confidence-badge {badge_class}">
            {badge_icon} {confidence_label} Confidence ({confidence:.0%})
        </span>
        """
        if category:
            badges_html += f"""
            <span class="category-tag">📂 {category}</span>
            """

    # Replace newlines with <br> for proper HTML display
    formatted_answer = answer_text.replace('\n', '<br>')

    st.markdown(f"""
    <div class="bot-message">
        <div class="bot-avatar">🤖</div>
        <div>
            <div class="bot-bubble">{formatted_answer}</div>
            <div>{badges_html}</div>
            <div class="message-time">{timestamp}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_typing_indicator():
    """Shows a 3-dot typing animation while the bot 'processes' the query."""
    placeholder = st.empty()
    placeholder.markdown("""
    <div class="bot-message">
        <div class="bot-avatar">🤖</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return placeholder


def render_welcome_card(sample_questions: list):
    """
    Shows the welcome screen when there's no chat history yet.
    Includes sample question chips that users can click.
    """
    chips_html = ""
    for q in sample_questions[:6]:
        short_q = q[:55] + "..." if len(q) > 55 else q
        chips_html += f'<div class="sample-chip">{short_q}</div>'

    st.markdown(f"""
    <div class="welcome-card">
        <div style="font-size: 2.8rem; margin-bottom: 12px;">🤖</div>
        <h2>Hi there! I'm your FAQ Assistant</h2>
        <p>
            I can answer questions about <strong>College</strong>, <strong>E-commerce</strong>, 
            <strong>Banking</strong>, <strong>Internships</strong>, and more.<br>
            Just type your question below or click a sample question to get started.
        </p>
        <div class="sample-questions">
            {chips_html}
        </div>
        <p style="margin-top: 16px; font-size: 0.82rem; color: #94a3b8;">
            💡 Tip: Select a category from the sidebar for more focused answers
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────

def render_sidebar(chatbot: FAQChatbot) -> str:
    """
    Renders the left sidebar with:
    - App info and branding
    - Dark/light mode toggle
    - Category filter selector
    - Stats (total FAQs, queries, matches)
    - Instructions
    
    Returns:
        str: The selected category from the dropdown
    """
    with st.sidebar:
        # ── Branding ──
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px;">
            <div style="font-size: 2.5rem;">🤖</div>
            <h2 style="font-weight: 700; color: #667eea; margin: 8px 0 4px;">FAQ Chatbot</h2>
            <p style="font-size: 0.8rem; color: #94a3b8; margin: 0;">
                Powered by TF-IDF + Cosine Similarity
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Dark Mode Toggle ──
        st.session_state.dark_mode = st.toggle(
            "🌙 Dark Mode",
            value=st.session_state.dark_mode,
            help="Switch between light and dark themes"
        )

        st.divider()

        # ── Category Filter ──
        st.markdown("**📂 FAQ Category**")
        categories = ["All Categories"] + chatbot.get_all_categories()
        selected = st.selectbox(
            "Filter by category",
            options=categories,
            index=categories.index(st.session_state.selected_category)
                  if st.session_state.selected_category in categories else 0,
            help="Select a category to search only within that topic"
        )
        st.session_state.selected_category = selected

        st.divider()

        # ── Stats ──
        stats = chatbot.get_stats()
        st.markdown("**📊 Stats**")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">FAQs Loaded</div>
                <div class="stat-value">{stats['total_faqs']}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Questions Asked</div>
                <div class="stat-value">{st.session_state.total_queries}</div>
            </div>
            """, unsafe_allow_html=True)

        match_rate = (
            f"{(st.session_state.successful_matches / st.session_state.total_queries * 100):.0f}%"
            if st.session_state.total_queries > 0 else "N/A"
        )
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Match Rate</div>
            <div class="stat-value">{match_rate}</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── How It Works ──
        with st.expander("🧠 How does this work?"):
            st.markdown("""
            **1. You type a question**
            
            **2. Text Preprocessing**
            - Lowercase conversion
            - Remove punctuation & noise
            - Tokenization (split to words)
            - Stop word removal
            - Lemmatization (root forms)
            
            **3. TF-IDF Vectorization**
            - Your query → numerical vector
            - Each FAQ → numerical vector
            
            **4. Cosine Similarity**
            - Compares your query to all FAQs
            - Finds the closest match
            
            **5. Confidence Check**
            - Score ≥ 50% → confident answer
            - Score 25-50% → tentative answer
            - Score < 10% → no match found
            """)

        # ── Clear Chat ──
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
            st.session_state.chat_history = []
            st.session_state.total_queries = 0
            st.session_state.successful_matches = 0
            st.rerun()

        # ── Footer ──
        st.markdown("""
        <div style="text-align:center; padding-top:20px; font-size:0.75rem; color:#94a3b8;">
            Built with ❤️ using Python + Streamlit<br>
            NLTK · scikit-learn · TF-IDF
        </div>
        """, unsafe_allow_html=True)

    return selected


# ── Message Processing ─────────────────────────────────────

def process_user_message(user_input: str, chatbot: FAQChatbot):
    """
    Handles the full flow for processing one user message:
    1. Add user message to history
    2. Show typing animation
    3. Get bot response
    4. Add bot response to history
    5. Update stats
    
    Args:
        user_input (str): The user's raw question
        chatbot (FAQChatbot): The initialized chatbot engine
    """
    timestamp = datetime.now().strftime("%I:%M %p")

    # Add user message to chat history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': user_input,
        'timestamp': timestamp
    })

    # Track total queries
    st.session_state.total_queries += 1

    # Small artificial delay to make the typing animation visible
    # (Remove this in production if you want instant responses)
    time.sleep(0.8)

    # Get the bot's response from the NLP engine
    response = chatbot.get_response(user_input)

    # Track successful matches
    if response.get('status') == 'matched':
        st.session_state.successful_matches += 1

    # Add bot response to chat history
    st.session_state.chat_history.append({
        'role': 'bot',
        'content': response,
        'timestamp': timestamp
    })


# ── Main App ───────────────────────────────────────────────

def main():
    """
    Main function that assembles and runs the Streamlit application.
    Streamlit reruns this entire function every time the user interacts.
    """
    # Initialize session state on first run
    init_session_state()

    # Load custom CSS
    load_css()

    # Apply dark mode body styling if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp { background-color: #0f1724; color: #e2e8f0; }
        .bot-bubble { background: #1e2a3a !important; border-color: #2d3f55 !important; color: #e2e8f0 !important; }
        .welcome-card { background: linear-gradient(135deg, #1e2a3a, #0f1724); border-color: #2d3f55; }
        .welcome-card h2, .welcome-card p { color: #e2e8f0; }
        </style>
        """, unsafe_allow_html=True)

    # ── Initialize chatbot ──────────────────────────────────
    try:
        chatbot = get_or_load_chatbot(st.session_state.selected_category)
    except Exception as e:
        st.error(f"⚠️ Failed to initialize chatbot: {str(e)}")
        st.info("Please make sure `faq_data.json` is in the project root directory and try again.")
        st.stop()

    # ── Render Sidebar and get selected category ────────────
    selected_category = render_sidebar(chatbot)

    # Reload chatbot if category changed
    if selected_category != chatbot.current_category:
        chatbot.reload_with_category(selected_category)

    # ── Page Header ────────────────────────────────────────
    st.markdown("""
    <div style="padding-bottom: 8px;">
        <h1 style="font-size: 1.8rem; font-weight: 700; color: #1a1f36; margin: 0;">
            💬 FAQ Assistant
        </h1>
        <p style="color: #64748b; font-size: 0.9rem; margin: 4px 0 0;">
            Ask me anything — I'll find the best answer from our knowledge base
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Chat History Display ────────────────────────────────
    if not st.session_state.chat_history:
        # Show welcome screen for new users
        sample_qs = chatbot.get_sample_questions(
            category=st.session_state.selected_category,
            count=6
        )
        render_welcome_card(sample_qs)
    else:
        # Render each message in the chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                render_user_message(
                    text=message['content'],
                    timestamp=message['timestamp']
                )
            else:
                render_bot_message(
                    response=message['content'],
                    timestamp=message['timestamp']
                )

    # ── Process Pending Message ─────────────────────────────
    # Messages are queued here before the chat input rerenders
    if st.session_state.pending_message:
        pending = st.session_state.pending_message
        st.session_state.pending_message = None

        # Show typing animation while processing
        typing_placeholder = render_typing_indicator()
        process_user_message(pending, chatbot)
        typing_placeholder.empty()  # Remove typing animation
        st.rerun()  # Rerun to display new message in history

    # ── Input Section ──────────────────────────────────────
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
    st.divider()

    # Use columns to layout input + send button side by side
    input_col, button_col = st.columns([5, 1])

    with input_col:
        user_input = st.text_input(
            label="Type your question",
            placeholder="✍️  Ask me anything... (press Enter to send)",
            label_visibility="collapsed",
            key=f"user_input_{st.session_state.input_key}"  # Dynamic key clears input after send
        )

    with button_col:
        send_clicked = st.button("Send ➤", use_container_width=True, type="primary")

    # ── Handle Send Action ──────────────────────────────────
    # Triggered by clicking Send button OR pressing Enter
    if (send_clicked or user_input) and user_input and user_input.strip():
        # Validate input
        from utils.preprocessor import is_valid_input
        is_valid, error_msg = is_valid_input(user_input)

        if not is_valid:
            st.warning(f"⚠️ {error_msg}")
        else:
            # Queue the message and increment key to clear input field
            st.session_state.pending_message = user_input.strip()
            st.session_state.input_key += 1
            st.rerun()

    # ── Bottom Quick-Ask Buttons ────────────────────────────
    if not st.session_state.chat_history:
        st.markdown("**💡 Try asking:**")
        quick_questions = [
            "How do I apply for financial aid?",
            "How can I track my order?",
            "How do I reset my banking password?",
            "Is the internship paid?",
        ]
        cols = st.columns(len(quick_questions))
        for i, q in enumerate(quick_questions):
            with cols[i]:
                if st.button(q, key=f"quick_{i}", use_container_width=True):
                    st.session_state.pending_message = q
                    st.session_state.input_key += 1
                    st.rerun()

    # ── Chat Export (bonus feature) ──────────────────────────
    if st.session_state.chat_history:
        with st.expander("📥 Export Chat History"):
            chat_text = ""
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    chat_text += f"[{msg['timestamp']}] YOU: {msg['content']}\n\n"
                else:
                    answer = msg['content'].get('answer', '')
                    chat_text += f"[{msg['timestamp']}] BOT: {answer}\n\n"
                    chat_text += "─" * 60 + "\n\n"

            st.download_button(
                label="⬇️ Download as .txt",
                data=chat_text,
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


# ── Entry Point ────────────────────────────────────────────
if __name__ == "__main__":
    main()
