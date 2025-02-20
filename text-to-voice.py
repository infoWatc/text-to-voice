'''
pip install edge-tts python-docx pygame

'''

import asyncio
import os
import edge_tts
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pygame import mixer
from docx import Document
import re  # Import regex module for extracting text in parentheses

# Initialize pygame mixer for audio playback
mixer.init()

# Default last directory
last_directory = os.getcwd()

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Converter")
        self.root.geometry("500x450")

        # File Selection
        self.file_path = tk.StringVar()
        tk.Button(root, text="Open File", command=self.open_file).pack(pady=10)
        self.file_label = tk.Label(root, text="No file selected", wraplength=400)
        self.file_label.pack()

        # Voice Selection (Fixing Issue)
        self.voice_var = tk.StringVar()
        tk.Label(root, text="Select Voice:").pack(pady=5)
        self.voice_dropdown = ttk.Combobox(root, textvariable=self.voice_var, state="readonly", width=30)  # Adjust width for better display
        self.voice_dropdown.pack()
        self.get_voices()  # Fetch correct voices

        # Volume Control
        tk.Label(root, text="Volume:").pack(pady=5)
        self.volume_var = tk.DoubleVar(value=1.0)
        self.volume_slider = tk.Scale(root, from_=0.1, to=1.0, resolution=0.1, orient="horizontal", variable=self.volume_var)
        self.volume_slider.pack()

        # Convert, Play & Stop Buttons
        tk.Button(root, text="Convert to Speech", command=self.convert_text).pack(pady=10)
        tk.Button(root, text="Play Audio", command=self.play_audio).pack(pady=5)
        tk.Button(root, text="Stop Audio", command=self.stop_audio).pack(pady=5)
        tk.Button(root, text="Save as MP3", command=self.save_audio).pack(pady=5)

        # Text content storage
        self.text_content = ""

        # Dictionary to map displayed voice names to full voice IDs
        self.voice_map = {}

    def open_file(self):
        global last_directory
        filetypes = [("Text files", "*.txt"), ("Word files", "*.docx"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(initialdir=last_directory, title="Select a File", filetypes=filetypes)
        if file_path:
            self.file_path.set(file_path)
            self.file_label.config(text=os.path.basename(file_path))
            last_directory = os.path.dirname(file_path)
            self.read_file(file_path)

    def read_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == ".txt":
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_content = file.read()
            elif ext == ".docx":
                doc = Document(file_path)
                self.text_content = "\n".join([para.text for para in doc.paragraphs])
            else:
                messagebox.showerror("Error", "Unsupported file format.")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    async def convert_and_play(self):
        if not self.text_content:
            messagebox.showerror("Error", "No text to convert.")
            return

        selected_voice_display = self.voice_var.get()
        voice = self.voice_map.get(selected_voice_display, "en-US-AndrewNeural")  # Map display name to full voice ID
        mp3_file = "output.mp3"

        tts = edge_tts.Communicate(self.text_content, voice)
        await tts.save(mp3_file)

        self.play_audio()

    def convert_text(self):
        asyncio.run(self.convert_and_play())

    def play_audio(self):
        if os.path.exists("output.mp3"):
            mixer.music.load("output.mp3")
            mixer.music.set_volume(self.volume_var.get())
            mixer.music.play()
        else:
            messagebox.showerror("Error", "No audio file found. Convert text first.")

    def stop_audio(self):
        mixer.music.stop()

    def save_audio(self):
        if not self.text_content:
            messagebox.showerror("Error", "No text to save as speech.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            selected_voice_display = self.voice_var.get()
            voice = self.voice_map.get(selected_voice_display, "en-US-AndrewNeural")  # Map display name to full voice ID
            asyncio.run(self.save_as_mp3(save_path, voice))

    async def save_as_mp3(self, save_path, voice):
        tts = edge_tts.Communicate(self.text_content, voice)
        await tts.save(save_path)
        messagebox.showinfo("Success", f"Audio saved: {save_path}")

    async def fetch_voices(self):
        voices = await edge_tts.list_voices()
        return [voice["Name"] for voice in voices]  # Fix: Only get proper names

    def get_voices(self):
        async def fetch_and_set():
            voices = await self.fetch_voices()
            self.voice_map = {}  # Reset mapping
            display_names = []  # New display list

            for voice in voices:
                match = re.search(r"\((.*?)\)", voice)  # Extract content inside parentheses
                if match:
                    display_name = match.group(1)  # Extracted text
                    self.voice_map[display_name] = voice  # Map display name to full voice ID
                    display_names.append(display_name)

            display_names = list(set(display_names))  # Remove duplicates
            display_names.sort()  # Sort for better UI experience

            self.voice_dropdown["values"] = display_names
            if display_names:
                self.voice_var.set(display_names[0])  # Set default

        asyncio.run(fetch_and_set())

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
