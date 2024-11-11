import tkinter as tk
from tkinter import messagebox
import requests

# Function to call the Flask search endpoint
def search_papers():
    query = search_entry.get()  # Get query from user input
    if query:
        response = requests.get(f'http://127.0.0.1:5000/search?query={query}')
        if response.status_code == 200:
            results = response.json()
            display_results(results)
        else:
            messagebox.showerror("Error", "Failed to fetch papers.")
    else:
        messagebox.showwarning("Input Error", "Please enter a search query.")

# Function to display search results in the GUI
def display_results(results):
    for widget in results_frame.winfo_children():
        widget.destroy()

    if not results:
        messagebox.showinfo("No Results", "No papers found.")
        return

    for paper in results:
        title = paper.get('title', 'No Title')
        authors = ', '.join(paper.get('authors', []))
        summary = paper.get('summary', 'No Summary Available')

        result_label = tk.Label(results_frame, text=f"Title: {title}\nAuthors: {authors}\nSummary: {summary}\n")
        result_label.pack(pady=10)

# Function to call the Flask QA endpoint
def answer_question():
    paper_text = question_text.get()  # Get the paper text
    question = question_entry.get()  # Get the user's question
    if paper_text and question:
        response = requests.post('http://127.0.0.1:5000/qa', json={'paper_text': paper_text, 'question': question})
        if response.status_code == 200:
            answer = response.json().get('answer', 'No answer found.')
            answer_label.config(text=f"Answer: {answer}")
        else:
            messagebox.showerror("Error", "Failed to get an answer.")
    else:
        messagebox.showwarning("Input Error", "Please enter both paper text and a question.")

# Function to call the Flask future work endpoint
def generate_future_work():
    papers = future_paper_text.get('1.0', 'end-1c')  # Get papers text from the user
    if papers:
        response = requests.post('http://127.0.0.1:5000/future_work', json={'papers': [{'abstract': papers}]})
        if response.status_code == 200:
            future_work = response.json().get('future_work', 'No future work generated.')
            future_work_label.config(text=f"Future Work: {future_work}")
        else:
            messagebox.showerror("Error", "Failed to generate future work.")
    else:
        messagebox.showwarning("Input Error", "Please enter some text for future work generation.")

# Set up the main window (GUI)
window = tk.Tk()
window.title("Research Paper Assistant")

# Create and place widgets for searching papers
search_label = tk.Label(window, text="Search Papers")
search_label.pack(pady=10)

search_entry = tk.Entry(window, width=50)
search_entry.pack(pady=10)

search_button = tk.Button(window, text="Search", command=search_papers)
search_button.pack(pady=5)

# Frame for displaying search results
results_frame = tk.Frame(window)
results_frame.pack(pady=20)

# Create and place widgets for answering questions
question_label = tk.Label(window, text="Enter Paper Text and Your Question")
question_label.pack(pady=10)

question_text = tk.Text(window, height=5, width=50)
question_text.pack(pady=10)

question_entry = tk.Entry(window, width=50)
question_entry.pack(pady=5)

qa_button = tk.Button(window, text="Ask Question", command=answer_question)
qa_button.pack(pady=5)

answer_label = tk.Label(window, text="Answer: ")
answer_label.pack(pady=10)

# Create and place widgets for generating future work suggestions
future_work_label = tk.Label(window, text="Generate Future Work Suggestions")
future_work_label.pack(pady=10)

future_paper_text = tk.Text(window, height=5, width=50)
future_paper_text.pack(pady=10)

future_work_button = tk.Button(window, text="Generate Future Work", command=generate_future_work)
future_work_button.pack(pady=5)

future_work_label = tk.Label(window, text="Future Work: ")
future_work_label.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()