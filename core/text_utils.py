"""
Shared text utilities for cleaning and formatting LLM responses.
"""

def clean_sheet(raw_text: str, filler_phrases: list[str]) -> str:
    """
    Generic function to clean up common artifacts and conversational filler from LLM output.
    
    Args:
        raw_text: The raw text response from the LLM
        filler_phrases: List of phrases to remove (exact matches only)
    
    Returns:
        Cleaned text with filler phrases removed
    """
    if not raw_text:
        return ""
    
    # Handle both literal '\\n' and real newlines
    if '\\n' in raw_text:
        lines = raw_text.split('\\n')
    else:
        lines = raw_text.split('\n')
    
    # Remove lines that exactly match any filler phrase (after stripping whitespace)
    cleaned_lines = [
        line for line in lines 
        if line.strip() not in filler_phrases
    ]
    
    # Join back with real newlines
    return '\n'.join(cleaned_lines).strip() 