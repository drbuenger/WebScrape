import tkinter as tk

def search_click(event):
    search_keywords = search_entry.get("1.0",tk.END)
    print(search_keywords)
    exclude_keywords = search_companies_exclude.get("1.0",tk.END)
    print(exclude_keywords)

#gui
window = tk.Tk()
window.title("Job Searchin'")
frame = tk.Frame(master=window, relief=tk.RIDGE)
header_text = tk.Label(
    text="Job Search",
    fg="white",
    bg="black",
    width=12,
    height = 3
    )
search_label = tk.Label(master=frame,text="Searches")
search_entry = tk.Text(master=frame)
exclusions_label = tk.Label(master=frame,text="Exclusions")
search_companies_exclude = tk.Text(master=frame)
search_button = tk.Button(master=frame, text='Search')
search_button.bind("<Button-1>", search_click)

search_label.pack()
search_entry.pack()
exclusions_label.pack()
search_companies_exclude.pack()
search_entry.pack()
search_button.pack()

frame.pack()
window.mainloop()


