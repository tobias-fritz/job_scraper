




def word_search(description, words):
    """Search for a list of words in a job description, at least one word must be present."""
    for word in words:
        if word.lower() in " ".join(description).lower():
            return True
    return False

def word_search_strict(description, words):
    """Search for a list of words in a job description, all words must be present."""
    for word in words:
        if word.lower() not in " ".join(description).lower():
            return False
    return True