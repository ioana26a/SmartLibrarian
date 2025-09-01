from http import client
from chatbot.retriever import search_books_by_theme
from tools.summaries import get_summary_by_title
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_themes_from_question(question: str) -> str:
    prompt = f"""
    Analyze the following question and extract the main themes (for example, friendship, magic, war):
    Question: "{question}"
    Answer: The themes are:
    """
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a librarian."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    
    themes = response.choices[0].message.content.strip()
    return themes

def recommend_books_by_theme(themes: str, num_recommendations: int = 3):
    # Search for relevant books using your retriever function
    books = search_books_by_theme(themes)
    return books[:num_recommendations]

def generate_recommendation_response(books, themes):
    # Build a conversational response with recommendations and titles
    book_list = "\n".join([f"{idx+1}. {book['title']}" for idx, book in enumerate(books)])
    prompt = f"""
    Recommend {len(books)} books based on the themes: {themes}.
    The recommended books are:
    {book_list}
    Write a conversational and persuasive response, mentioning the titles.
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a librarian."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def get_book_summary(book):
    # Return the book summary
    return book.get("summary", "No summary available for this book.")

# Example conversational flow:
def handle_user_request(user_input, previous_books=None):
    user_input_lower = user_input.lower()

    # 1. If the user asks for a summary of a previous recommendation
    if "summary" in user_input_lower:
        if previous_books:
            # By default, provide the summary for the first recommended book
            book = previous_books[0]
            summary = get_summary_by_title(book['title'])
            return f"📖 Full summary for '{book['title']}':\n{summary}", previous_books
        else:
            return "There are no previous recommendations to provide a summary for.", []

    # 2. If the user wants both recommendations and a summary in the same request
    if "recommend" in user_input_lower and "summary" in user_input_lower:
        themes = extract_themes_from_question(user_input)
        books = recommend_books_by_theme(themes)
        response = generate_recommendation_response(books, themes)
        if books:
            book = books[0]
            summary = get_summary_by_title(book['title'])
            response += f"\n\n📖 Full summary for '{book['title']}':\n{summary}"
        return response, books

    # 3. Only recommendations
    themes = extract_themes_from_question(user_input)
    books = recommend_books_by_theme(themes)
    response = generate_recommendation_response(books, themes)
    return response, books