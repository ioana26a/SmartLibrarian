import gradio as gr
from chatbot.chatbot import extract_themes_from_question, generate_recommendation_response
from chatbot.retriever import search_books_by_theme
from tools.summaries import get_summary_by_title

def smart_librarian(user_input):
    themes = extract_themes_from_question(user_input)
    res = search_books_by_theme(themes)

    if not res["documents"][0]:
        return "I couldn't find a suitable book. Could you rephrase your request?", ""

    book_title = res["metadatas"][0][0]["title"]
    book_summary = res["documents"][0][0]
    books = [{"title": book_title, "summary": book_summary}]
    recommendation = generate_recommendation_response(books, themes)
    full_summary = get_summary_by_title(book_title)

    return recommendation, f"Summary for '{book_title}':\n{full_summary}"

# Defineste tema
custom_theme = gr.themes.Default(primary_hue="blue", neutral_hue="gray")

# Interfata Gradio
with gr.Blocks(theme=custom_theme) as demo:
    gr.Markdown("# 📚 Smart Librarian")

    with gr.Row():
        user_input = gr.Textbox(label="What kind of book are you looking for?", lines=2, placeholder="e.g. I want a book about friendship and adventure")

    with gr.Row():
        recommendation_output = gr.Textbox(label="Librarian's Recommendation", lines=5)
        summary_output = gr.Textbox(label="Summary", lines=8)

    submit_btn = gr.Button("Submit")

    submit_btn.click(
        fn=smart_librarian,
        inputs=user_input,
        outputs=[recommendation_output, summary_output]
    )

if __name__ == "__main__":
    demo.launch()
