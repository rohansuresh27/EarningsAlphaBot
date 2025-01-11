import os
import json
import anthropic
from typing import List, Dict

if not os.getenv("ANTHROPIC_API_KEY"):
    raise Exception("Missing ANTHROPIC_API_KEY in secrets")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


class ClaudeQuoteExtractor:
    """Extract quotes from earnings call transcripts using Claude API."""

    def __init__(self):
        """Initialize the Claude client."""
        self.client = client  # Use the already initialized client

    def extract_quotes(self, text: str, company_name: str) -> List[Dict]:
        """
        Extract the most compelling quotes using Claude API.
        
        Args:
            text (str): The earnings call transcript text
            company_name (str): Name of the company
            
        Returns:
            List[Dict]: List of extracted quotes with metadata
        """
        prompt = f"""You are an expert financial analyst. Analyze this earnings call transcript and identify the 10 most compelling quotes.
        
Context: Focus on most compelling insights, strategic shifts, and market observations. Look for forward-looking statements, CEO/executive perspectives, future outlooks, growth projections and emerging trends that could impact stock performance.

For each quote, provide:
1. The speakers name, i.e Who said it (e.g., CEO, CFO): [SPEAKER]
2. A brief and catchy description of the quote's significance.
3. The exact quote from the transcript
4. Make it Twitter-friendly

Format each quote as:
"{company_name} [SPEAKER] on [DESCRIPTION]:
[QUOTE]
#{company_name}"

Transcript:
{text}

Return exactly 10 quotes in this format, focusing on the most impactful insights."""

        # Get Claude's analysis
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            temperature=0.5,
            messages=[{
                "role": "user",
                "content": prompt
            }])

        # Parse response and structure quotes
        quotes = []
        raw_quotes = message.content[0].text.strip().split('\n\n')

        for quote in raw_quotes:
            if not quote.strip():
                continue

            # Parse the quote components
            try:
                header, quote_text, hashtag = quote.split('\n')
                speaker = header.split(' on ')[0].replace(
                    f"{company_name} ", "")
                description = header.split(' on ')[1].rstrip(':')

                quotes.append({
                    'company': company_name,
                    'speaker': speaker,
                    'description': description,
                    'quote': quote_text.strip('"'),
                    'hashtag': hashtag.strip()
                })
            except Exception as e:
                print(f"Warning: Failed to parse quote: {str(e)}")

        return quotes

    def save_quotes_to_json(self, quotes: List[Dict], output_path: str):
        """Save extracted quotes to a JSON file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(quotes, f, indent=2)
        except Exception as e:
            print(f"Error saving quotes to JSON: {str(e)}")
