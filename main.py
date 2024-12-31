import requests
from bs4 import BeautifulSoup
import openpyxl
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser

def scrape_google_links(query_url, num_pages):
    all_links = set()

    for page in range(1, num_pages + 1):
        page_url = f"{query_url}&start={(page - 1) * 10}"
        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for anchor in soup.find_all('a'):
                href = anchor.get('href')
                if href and href.startswith('/url?q='):
                    link = href[7:href.find('&')]
                    all_links.add(link)
    
    return all_links

def start_scraping():
    query = entry_query.get()
    num_pages = int(entry_pages.get())
    url = f"https://www.google.com/search?q={query}"
    
    links = scrape_google_links(url, num_pages)
    
    if links:
        output_file = entry_output.get()
        output_format = combo_format.get()
        
        if output_format == 'txt':
            with open(f"{output_file}.txt", 'w') as file:
                for link in links:
                    file.write(link + '\n')
            messagebox.showinfo("Success", "Links saved to a txt file.")
        elif output_format == 'excel':
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Links"
            for index, link in enumerate(links, start=1):
                ws.cell(row=index, column=1, value=link)
            excel_file = f"{output_file}.xlsx"
            wb.save(excel_file)
            messagebox.showinfo("Success", f"Links saved to an Excel file: {excel_file}")
    else:
        messagebox.showwarning("No Links Found", "No links found for the specified query.")

# Function to show initial warning and open Google
def show_warning():
    response = messagebox.askokcancel("Uyarı", "Bu uygulamanın bir yapımcısı vardır. Yapımcıdan izinsiz paylaşmayın.")
    if response:
        webbrowser.open("https://github.com/HeJo-1")  # Open Google in the browser
        open_main_window()  # Open the main application window

def open_main_window():
    # Create the main window
    global root
    root = tk.Tk()
    root.title("Google Link Scraper")
    root.geometry("400x350")
    root.configure(bg="#f0f0f0")

    # Style configuration
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", background="#f0f0f0", foreground="#333", font=("Arial", 11))
    style.configure("TEntry", font=("Arial", 11), padding=5)
    style.configure("TButton", font=("Arial", 11), padding=5)
    style.configure("TCombobox", font=("Arial", 11), padding=5)

    # Create and place widgets
    label_query = ttk.Label(root, text="Arama sorgusunu girin:")
    label_query.pack(pady=(10, 5))

    entry_query = ttk.Entry(root, width=40)
    entry_query.pack(pady=5)

    label_pages = ttk.Label(root, text="Araştırılacak sayfa sayısını girin:")
    label_pages.pack(pady=5)

    entry_pages = ttk.Entry(root, width=10)
    entry_pages.pack(pady=5)

    label_output = ttk.Label(root, text="Çıktı dosya adını girin (uzantısı olmadan):")
    label_output.pack(pady=5)

    entry_output = ttk.Entry(root, width=40)
    entry_output.pack(pady=5)

    label_format = ttk.Label(root, text="Çıktı formatını seçin:")
    label_format.pack(pady=5)

    combo_format = ttk.Combobox(root, values=["txt", "excel"], state="readonly")
    combo_format.pack(pady=5)
    combo_format.current(0)  # Set default value

    button_scrape = ttk.Button(root, text="Scrape Links", command=start_scraping)
    button_scrape.pack(pady=(20, 10))

    # Run the main loop
    root.mainloop()

# Show warning before opening the main window
show_warning()
