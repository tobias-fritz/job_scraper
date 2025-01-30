import re

def split_sentences(description):
    """Post-process the job description to split it into a list of sentences."""
    
    description = re.split(r'[.!?]', description)
    description = [
        re.sub(r'([^\s\w]|_)+', '', 
        re.sub(r'([a-zA-Z]):([a-zA-Z])', r'\1: \2', 
        re.sub(r'([a-z])([A-Z])', r'\1 \2', 
        sentence.strip().encode('ascii', 'ignore').decode('ascii')
        ))).replace('\n', '').replace("  ", "").replace('Show more', '').replace('Show less', '').strip()
        for sentence in description if sentence.strip()
    ]
    description = [sentence for sentence in description if sentence]  # Filter out empty strings

    return description