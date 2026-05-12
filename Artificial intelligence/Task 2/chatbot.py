# chatbot.py
# ============================================================
# CHATBOT ENGINE — THE BRAIN OF THE APPLICATION
# 
# This module handles:
# 1. Building the TF-IDF matrix from FAQ questions
# 2. Processing user queries
# 3. Computing cosine similarity scores
# 4. Returning the best matching answer
#
# HOW IT WORKS (in simple words):
# Imagine each FAQ question is described by a "fingerprint" of
# numbers — each number represents how important a word is in
# that question. When a user asks something, we create the same
# kind of fingerprint for their query. Then we measure how
# similar the user's fingerprint is to each FAQ's fingerprint.
# The most similar FAQ is our best match.
# ============================================================

import numpy as np
from typing import Optional

# TF-IDF Vectorizer converts text into numerical vectors
# Cosine similarity measures the "angle" between two vectors
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

# Our custom preprocessing pipeline
from utils.preprocessor import preprocess_text
from utils.faq_loader import load_faq_data, flatten_faqs, get_category_names, get_faq_count


# ── Confidence thresholds ──────────────────────────────────
# If the best match score is below this, we say "I don't know"
HIGH_CONFIDENCE_THRESHOLD = 0.5    # Score ≥ 0.5: confident answer
MEDIUM_CONFIDENCE_THRESHOLD = 0.25  # Score 0.25–0.5: tentative answer
LOW_CONFIDENCE_THRESHOLD = 0.10    # Score < 0.10: no match found


class FAQChatbot:
    """
    The main chatbot class that encapsulates all NLP logic.
    
    Usage:
        bot = FAQChatbot()
        bot.load_data()
        response = bot.get_response("How do I reset my password?")
    """

    def __init__(self, faq_filepath: str = "faq_data.json"):
        self.faq_filepath = faq_filepath
        
        # Raw data from JSON
        self.raw_data = None
        
        # Parallel lists: question[i] maps to answer[i] and category[i]
        self.questions = []
        self.answers = []
        self.categories = []
        
        # Preprocessed questions (cleaned text for TF-IDF)
        self.processed_questions = []
        
        # TF-IDF components
        # The vectorizer learns vocabulary from all FAQ questions
        self.vectorizer = None
        
        # The TF-IDF matrix: shape = (num_faqs, vocab_size)
        # Each row = a FAQ question represented as TF-IDF scores
        self.tfidf_matrix = None
        
        # Track which category filter is currently active
        self.current_category = "All Categories"
        
        # Track if the bot is ready to answer
        self.is_ready = False
        self.error_message = ""

    # ── DATA LOADING ────────────────────────────────────────

    def load_data(self, category_filter: str = "All Categories") -> bool:
        """
        Loads FAQ data and builds the TF-IDF model.
        Called once at startup or when the user changes category filter.
        
        Args:
            category_filter (str): Category to filter by. "All Categories" = use all.
        
        Returns:
            bool: True if successful, False if any error occurred
        """
        try:
            # Step 1: Load raw JSON data
            self.raw_data = load_faq_data(self.faq_filepath)
        except FileNotFoundError as e:
            self.error_message = str(e)
            self.is_ready = False
            return False
        except ValueError as e:
            self.error_message = str(e)
            self.is_ready = False
            return False

        # Step 2: Flatten nested JSON into parallel lists
        self.current_category = category_filter
        self.questions, self.answers, self.categories = flatten_faqs(
            self.raw_data,
            selected_category=category_filter if category_filter != "All Categories" else None
        )

        if len(self.questions) == 0:
            self.error_message = f"No FAQs found for category: {category_filter}"
            self.is_ready = False
            return False

        # Step 3: Preprocess all FAQ questions
        # This creates cleaned versions that TF-IDF will work with
        self.processed_questions = [
            preprocess_text(q) for q in self.questions
        ]

        # Step 4: Build TF-IDF model
        success = self._build_tfidf_model()
        return success

    # ── TF-IDF MODEL BUILDING ────────────────────────────────

    def _build_tfidf_model(self) -> bool:
        """
        Builds the TF-IDF vectorizer and computes the matrix.
        
        WHAT IS TF-IDF? (simple explanation)
        
        TF = Term Frequency: How often a word appears in a question.
             "apply" appears 3 times → high TF
        
        IDF = Inverse Document Frequency: How rare a word is across ALL FAQs.
              If "the" appears in every FAQ → low IDF (not useful)
              If "lemmatization" appears in 1 FAQ → high IDF (very useful)
        
        TF-IDF = TF × IDF
        Words that are common in ONE question but rare across ALL questions
        get the highest TF-IDF scores. These are the "signature words."
        
        Returns:
            bool: True if model built successfully
        """
        if not SKLEARN_AVAILABLE:
            self.error_message = (
                "scikit-learn is not installed. "
                "Run: pip install scikit-learn"
            )
            self.is_ready = False
            return False

        try:
            # Create the TF-IDF Vectorizer
            # ngram_range=(1,2) means it looks at single words AND word pairs
            # Example: "bank account" is treated as one feature, not just "bank" + "account"
            # min_df=1: include a word even if it appears in just 1 question
            # max_df=0.95: ignore words that appear in 95%+ of questions (too common)
            # sublinear_tf=True: applies log scaling to term frequency (reduces impact of very frequent words)
            self.vectorizer = TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                max_df=0.95,
                sublinear_tf=True,
                analyzer='word'
            )

            # FIT: The vectorizer learns the vocabulary from all FAQ questions
            # TRANSFORM: Converts each question into a TF-IDF vector
            # Result: a 2D matrix of shape (num_faqs × vocab_size)
            self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)

            self.is_ready = True
            self.error_message = ""
            return True

        except Exception as e:
            self.error_message = f"Failed to build TF-IDF model: {str(e)}"
            self.is_ready = False
            return False

    # ── QUERY PROCESSING AND MATCHING ────────────────────────

    def get_response(self, user_query: str) -> dict:
        """
        The main method that takes a user's question and returns the best answer.
        
        STEP-BY-STEP PROCESS:
        1. Preprocess user query (same cleaning as FAQ questions)
        2. Convert query to TF-IDF vector (using the already-fitted vectorizer)
        3. Compute cosine similarity between query vector and all FAQ vectors
        4. Find the FAQ with the highest similarity score
        5. If score > threshold → return that FAQ's answer
           If score < threshold → return fallback message
        
        WHAT IS COSINE SIMILARITY? (simple explanation)
        
        Think of each text as an arrow (vector) pointing in a certain direction.
        If two texts are about the same topic, their arrows point in similar directions.
        Cosine similarity measures the ANGLE between two arrows.
        
        Angle ≈ 0°  → similarity ≈ 1.0 (very similar, almost identical)
        Angle = 90° → similarity = 0.0 (completely unrelated)
        
        We DON'T care about the length (how long the text is),
        only the DIRECTION (what words it uses).
        
        Args:
            user_query (str): The raw user question
        
        Returns:
            dict: {
                'answer': str,          # The best matching answer
                'matched_question': str, # The FAQ question we matched
                'confidence': float,    # Similarity score (0 to 1)
                'confidence_label': str, # "High", "Medium", or "Low"
                'category': str,        # Which category the match came from
                'status': str           # 'matched', 'low_confidence', or 'no_match'
            }
        """
        # Guard: Check if the chatbot is properly initialized
        if not self.is_ready:
            return self._build_error_response(
                f"Chatbot is not ready. {self.error_message}",
                status="error"
            )

        # Guard: Check if the query is not empty
        if not user_query or not user_query.strip():
            return self._build_error_response(
                "It looks like you sent an empty message. Please type your question!",
                status="empty"
            )

        # STEP 1: Preprocess the user's query
        # Apply the same cleaning pipeline used on FAQ questions
        processed_query = preprocess_text(user_query)

        # Guard: If preprocessing left nothing meaningful
        if not processed_query.strip():
            return self._build_error_response(
                "I couldn't understand that input. Please try rephrasing your question.",
                status="empty"
            )

        try:
            # STEP 2: Convert the user query to a TF-IDF vector
            # We use TRANSFORM only (not fit_transform) because the vocabulary
            # was already learned during the FAQ loading step
            query_vector = self.vectorizer.transform([processed_query])

            # STEP 3: Compute cosine similarity
            # Compare the query vector against every FAQ's vector
            # Result: array of shape (1, num_faqs) — one score per FAQ
            similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix)

            # Flatten to 1D array for easier indexing
            scores = similarity_scores.flatten()

            # STEP 4: Find the best match
            # argmax gives us the INDEX of the highest score
            best_match_index = int(np.argmax(scores))
            best_score = float(scores[best_match_index])

            # STEP 5: Decide what to return based on confidence score
            if best_score >= HIGH_CONFIDENCE_THRESHOLD:
                return {
                    'answer': self.answers[best_match_index],
                    'matched_question': self.questions[best_match_index],
                    'confidence': round(best_score, 3),
                    'confidence_label': 'High',
                    'category': self.categories[best_match_index],
                    'status': 'matched'
                }

            elif best_score >= MEDIUM_CONFIDENCE_THRESHOLD:
                # Tentative match — show the answer but with a warning
                return {
                    'answer': (
                        f"I'm not entirely sure, but here's what might help:\n\n"
                        f"{self.answers[best_match_index]}\n\n"
                        f"*If this doesn't answer your question, try rephrasing it.*"
                    ),
                    'matched_question': self.questions[best_match_index],
                    'confidence': round(best_score, 3),
                    'confidence_label': 'Medium',
                    'category': self.categories[best_match_index],
                    'status': 'low_confidence'
                }

            else:
                # No good match found
                return self._build_error_response(
                    "I'm sorry, I couldn't find a good answer to your question. "
                    "Try rephrasing it, or select a specific category from the sidebar "
                    "to narrow down the search. You can also browse sample questions below.",
                    status="no_match",
                    confidence=round(best_score, 3)
                )

        except Exception as e:
            return self._build_error_response(
                f"An unexpected error occurred while processing your question. "
                f"Please try again. (Error: {str(e)})",
                status="error"
            )

    # ── UTILITY METHODS ─────────────────────────────────────

    def _build_error_response(
        self,
        message: str,
        status: str = "error",
        confidence: float = 0.0
    ) -> dict:
        """Helper to build a consistent error/fallback response dictionary."""
        return {
            'answer': message,
            'matched_question': None,
            'confidence': confidence,
            'confidence_label': 'None',
            'category': None,
            'status': status
        }

    def get_sample_questions(self, category: str = "All Categories", count: int = 5) -> list:
        """
        Returns a sample of FAQ questions for display in the UI.
        Helps users understand what they can ask the bot.
        
        Args:
            category (str): Category to sample from
            count (int): How many sample questions to return
        
        Returns:
            list: Sample question strings
        """
        if not self.questions:
            return []

        filtered = []
        for i, q in enumerate(self.questions):
            if category == "All Categories" or self.categories[i] == category:
                filtered.append(q)

        # Return first `count` questions (or all if fewer available)
        return filtered[:min(count, len(filtered))]

    def get_all_categories(self) -> list:
        """Returns all available category names from loaded data."""
        if not self.raw_data:
            return []
        from utils.faq_loader import get_category_names
        return get_category_names(self.raw_data)

    def get_stats(self) -> dict:
        """Returns statistics about the loaded FAQ dataset."""
        return {
            'total_faqs': len(self.questions),
            'categories': list(set(self.categories)),
            'current_filter': self.current_category,
            'is_ready': self.is_ready
        }

    def reload_with_category(self, category: str) -> bool:
        """
        Rebuilds the TF-IDF model when the user changes category filter.
        This ensures the chatbot only searches within the selected category.
        
        Args:
            category (str): New category to filter by
        
        Returns:
            bool: True if reload was successful
        """
        return self.load_data(category_filter=category)
