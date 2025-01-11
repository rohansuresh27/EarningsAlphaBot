import nltk
from typing import List
import re
from nlp_setup import initialize_nltk

class QuoteExtractor:
    """Handles extraction of relevant quotes from text content."""

    def __init__(self):
        """Initialize the quote extractor."""
        # Initialize NLTK
        initialize_nltk()

    def extract_quotes(self, text: str) -> List[str]:
        """
        Extract relevant quotes from the text content.

        Args:
            text (str): Input text content

        Returns:
            List[str]: List of extracted quotes
        """
        quotes = []

        try:
            # Simple sentence splitting as fallback
            if '\n' in text:
                sentences = [s.strip() for s in text.split('\n') if s.strip()]
            else:
                sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]

            # Keywords that might indicate important quotes
            keywords = [
                'revenue', 'profit', 'growth', 'margin',
                'guidance', 'forecast', 'outlook',
                'increase', 'decrease', 'decline',
                'strategy', 'performance'
            ]

            for sentence in sentences:
                # Check if sentence contains any keywords
                if any(keyword in sentence.lower() for keyword in keywords):
                    # Clean the quote
                    clean_quote = self._clean_quote(sentence)
                    if clean_quote:
                        quotes.append(clean_quote)

        except Exception as e:
            print(f"Warning: Quote extraction failed: {str(e)}")
            return []

        return quotes

    def _clean_quote(self, quote: str) -> str:
        """
        Clean and format a quote.

        Args:
            quote (str): Raw quote text

        Returns:
            str: Cleaned quote
        """
        # Remove extra whitespace
        quote = ' '.join(quote.split())

        # Remove common PDF artifacts
        quote = re.sub(r'\s*\([^)]*\)', '', quote)

        # Remove any remaining special characters
        quote = re.sub(r'[^\w\s.,!?-]', '', quote)

        return quote.strip()