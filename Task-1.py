def count_words(text):
    """
    Function takes a string and returns a dictionary where keys are unique words
    and values are the number of their occurrences
    """
    # Split text into words, remove punctuation
    words = text.lower().replace(',', ' ').replace('.', ' ').replace('!', ' ').replace('?', ' ').split()
    
    # Create a dictionary for word counting
    word_count = {}
    
    # Count each word
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    
    return word_count

def get_frequent_words(word_count, min_occurrences=3):
    """
    Function returns a list of words that occur more than the specified number of times
    """
    return [word for word, count in word_count.items() if count > min_occurrences]


if __name__ == "__main__":
    # Default text to use if no input is provided
    default_text = "This is a default text to check the function. The text contains repetitions of words that the function should count. Text test text function words words."
    
    # Get text input from user
    print("Task 1: Working with text")
    print("Please enter a text (or press Enter to use default text):")
    user_input = input()
    
    # Use default text if input is empty
    if not user_input:
        print("Using default text.")
        text_sample = default_text
    else:
        text_sample = user_input
    
    # Count words and find frequent ones
    word_counts = count_words(text_sample)
    frequent_words = get_frequent_words(word_counts)
    
    # Display results
    print("\nDictionary of words and their count:")
    print(word_counts)
    
    # Check if there are words that occur more than 3 times
    if frequent_words:
        print("\nWords that occur more than 3 times:")
        print(frequent_words)
    else:
        print("\nThere are no words that occur more than 3 times in the provided text.")
