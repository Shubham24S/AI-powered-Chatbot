def truncate_text(text, max_length=1000):
    """
    Truncate text to a maximum length while preserving whole sentences.
    
    Args:
        text (str): The text to truncate
        max_length (int): Maximum length of the truncated text
    
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Find the last sentence boundary before max_length
    truncated = text[:max_length]
    last_period = truncated.rfind('.')
    
    if last_period > 0:
        return truncated[:last_period + 1]
    else:
        return truncated