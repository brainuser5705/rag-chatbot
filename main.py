import tkinter as tk
from tkinter import simpledialog
import tkinter.scrolledtext as st

from redis import Redis
from rq import Queue

from process import create_workspace, upload_files, ask_model


"""
Runs the chatbot application and job queue
"""
def main():

    queue = Queue(connection=Redis())

    root = tk.Tk()
    root.title("RAG Chat")

    message_label = tk.Label(root, text="Welcome to RAG Chat!")
    message_label.pack()

    workspace_name = simpledialog.askstring(title="Name the workspace: ", prompt="What is the name of the workspace?")
    create_workspace(workspace_name)

    import_button = tk.Button(root, text="Import file(s)", command=lambda: upload_files(queue, workspace_name, message_label))
    import_button.pack()

    chat_label = tk.Label(root, text="Chat History")
    chat_history = st.ScrolledText()
    chat_history.tag_config("ai", foreground="red")
    chat_history.insert(tk.END, "AI: Hello, I am an AI chatbot enhanced with a RAG system! Upload your domain-specific files and I can answer with relevance and accuracy!", "ai")
    chat_entry = tk.Entry()
    chat_history["state"] = "disabled"

    chat_label.pack()
    chat_history.pack()
    chat_entry.pack()

    def add_chat(_):
        new_text = chat_entry.get()
        chat_history["state"] = "normal"
        chat_history.insert(tk.END, "\n\nUser: " + new_text)
        chat_history.see(tk.END)
        chat_history["state"] = "disabled"
        chat_entry.delete(0, tk.END)
        
        ans = ask_model(new_text, workspace_name)
        chat_history["state"] = "normal"
        chat_history.insert(tk.END, "\n\nAI: " + ans + "\n", "ai")
        chat_history["state"] = "disabled"

    root.bind("<Return>", lambda _ : add_chat(_))

    root.mainloop()

if __name__ == "__main__":
    main()