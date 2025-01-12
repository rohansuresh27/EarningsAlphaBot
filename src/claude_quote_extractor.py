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
        prompt = f"""You are an expert financial analyst with deep experience in earnings call analysis. Review this transcript and identify the 10 most strategically significant quotes, prioritizing those that reveal:

HIGH PRIORITY SIGNALS:
- Major strategic shifts and market or industry trends
- New initiatives, new product launches or expansion to new markets
- Forward-looking growth projections or significant changes in financial metrics or guidance
- Market share gains or losses
- Capital allocation and investment priorities
- Customer/demand trends
- Macro headwinds or tailwinds affecting the business
- Changes in customer behavior or demand patterns
- Margin and profitability insights
- Technological innovations, technology investments, digital transformation or R&D
- Capital allocation decisions
- M&A plans or strategic partnerships
- Risk factors and mitigation strategies

QUOTE SELECTION CRITERIA:
- Favor specific, quantitative statements over general observations
- Prioritize forward-looking insights over historical performance
- Focus on structural/strategic changes over quarterly fluctuations
- Identify quotes that signal potential inflection points
- Include both positive developments and risk factors
- Highlight unexpected or contrarian viewpoints

For each quote, provide:
1. Speaker role: [SPEAKER] (Role - CEO, CFO, CTO, etc.)
2. Speaker name: [SPEAKER_NAME] (Name of the speaker)
3. Strategic Impact: [DESCRIPTION] (Brief analysis of why this quote matters for the company's future)
4. Verbatim Quote: [QUOTE] (Exact words from the transcript)
5. Hashtag: #{company_name} (One-word Hashtag of the company name with no space)

Format each quote as follows:
{company_name} [SPEAKER] on [DESCRIPTION]:
"[QUOTE]"
#{company_name}

Note: Do not include any numbering before or after the company name.

Transcript:
{text}

Please analyze and return exactly 10 quotes that represent the most strategically significant insights for investors and analysts. Focus particularly on forward-looking statements and quantitative projections.

Note: Please maintain verbatim accuracy in quotes while ensuring the social media versions preserve the core message.
"""

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

                # Extract speaker role and name from format "ROLE [NAME]"
                if '[' in speaker and ']' in speaker:
                    speaker_role = speaker.split('[')[0].strip()
                    speaker_name = speaker.split('[')[1].split(']')[0].strip()
                else:
                    speaker_role = speaker
                    speaker_name = ''
                
                quotes.append({
                    'company': company_name,
                    'speaker': speaker_role,
                    'speaker_name': speaker_name,
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
