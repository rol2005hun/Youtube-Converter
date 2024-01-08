import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
from pytube import Playlist
import sys
import os

# --- Functions ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def select_folder():
    folder_path = filedialog.askdirectory()
    folder_var.set(folder_path)
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)
    
def on_type_selected(event):
    selected_type = type_var.get()
    if selected_type == 'File of links':
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        url_entry.delete(0, tk.END)
        url_entry.insert(0, file_path)

def convert_text():
    result_label.config(text='Converting...')
    root.update_idletasks()
    
    url = url_entry.get()
    format_option = format_var.get()
    download_path = folder_var.get()
    link_type = type_var.get()

    if not url:
        result_label.config(text='Please enter a YouTube link.')
        return

    try:
        if link_type == 'Playlist':
            playlist = Playlist(url)
            videos = playlist.video_urls
        elif link_type == 'File of links':
            with open(url, 'r') as file:
                videos = [line.strip() for line in file.readlines()]
        else:
            videos = [url]
        
        if not download_path:
            download_path = os.path.join(os.path.expanduser('~'), 'Downloads')

        for video_url in videos:
            yt = YouTube(video_url)

            if format_option == 'MP3':
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(download_path)
            elif format_option == 'MP4':
                video_stream = yt.streams.filter(file_extension='mp4').first()
                video_stream.download(download_path)
            else:
                result_label.config(text='Invalid format selection.')

        result_label.config(text='Conversion completed.')
    except Exception as e:
        result_label.config(text=f'Error: {str(e)}')

# --- Window Setup ---

root = tk.Tk()
root.title('Wolimby - Converter')
root.iconbitmap(resource_path('R.ico'))

# --- Format Selection ---

label = ttk.Label(root, text='Convert Youtube links to:')
label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

formats = ['MP3', 'MP4']
format_var = tk.StringVar()
format_var.set(formats[0])

format_menu = ttk.Combobox(root, textvariable=format_var, values=formats, state='readonly')
format_menu.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

# --- URL Entry ---

url_label = ttk.Label(root, text='YouTube URL:')
url_label.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')

url_entry = ttk.Entry(root, width=30)
url_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

types = ['Video', 'Playlist', 'File of links']
type_var = tk.StringVar()
type_var.set(types[0])

type_menu = ttk.Combobox(root, textvariable=type_var, values=types, state='readonly', width=9)
type_menu.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')
type_menu.bind("<<ComboboxSelected>>", on_type_selected)

# --- Folder Selection ---

folder_var = tk.StringVar()
folder_var.set(os.path.join(os.path.expanduser('~'), 'Downloads'))

folder_label = ttk.Label(root, text='Download Path:')
folder_label.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')

folder_entry = ttk.Entry(root, textvariable=folder_var, width=30)
folder_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

select_folder_button = ttk.Button(root, text='Select Folder', command=select_folder)
select_folder_button.grid(row=2, column=2, padx=10, pady=5, sticky='w')

# --- Convert Button ---

convert_button = ttk.Button(root, text='Convert', command=convert_text, style='TButton', cursor='hand2')
convert_button.grid(row=3, column=0, padx=10, pady=10, sticky='nsw')

# --- Result Label ---

result_label = ttk.Label(root, text='', foreground='#FF0000')
result_label.grid(row=4, column=0, columnspan=3, padx=10, sticky='w')

# --- Window Settings ---

root.geometry('500x200')
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# --- Run the application ---

root.mainloop()