# **Text-to-Speech Converter**  
A Python-based **Text-to-Speech (TTS) application** that allows users to convert text from files into speech using **Microsoft Edge TTS voices**. The application supports **.txt** and **.docx** files, provides multiple voice options, and allows users to play, stop, and save speech as an **MP3 file**.  

## **Features**
✅ Convert **text or Word documents (.docx) to speech**  
✅ Supports **multiple voices**, including **male & female**  
✅ Adjustable **volume control**  
✅ **Play, Stop, and Save as MP3** functionality  
✅ **Graphical User Interface (GUI)** using **Tkinter**  
✅ Uses **Microsoft Edge-TTS API** for high-quality AI voices  

## **Installation**
Before running the program, install the required dependencies:  
```sh
pip install edge-tts python-docx pygame
```

## **How to Use**
1. **Run the Program**  
   ```sh
   python text-to-speech.py
   ```
2. **Select a File**  
   - Click **"Open File"** to choose a **.txt** or **.docx** file.  
3. **Choose a Voice**  
   - Select from available **Microsoft Edge voices** in the dropdown.  
4. **Adjust Volume**  
   - Use the **slider** to set the volume level.  
5. **Convert & Play**  
   - Click **"Convert to Speech"** to generate and play the speech.  
6. **Stop Audio**  
   - Click **"Stop Audio"** to halt playback.  
7. **Save as MP3**  
   - Click **"Save as MP3"** to export the generated speech as an **MP3 file**.  

## **Dependencies**
- **`edge-tts`** → Microsoft Edge TTS API for high-quality AI voices  
- **`python-docx`** → Reads text from **.docx** files  
- **`pygame`** → Handles **audio playback**  

## **Supported File Formats**
| File Type | Description |
|-----------|------------|
| `.txt`    | Plain text files |
| `.docx`   | Microsoft Word documents |

## **Customization**
- To **change the default voice**, modify this line in the code:  
  ```python
  voice = self.voice_map.get(selected_voice_display, "en-US-AndrewNeural")
  ```
  Replace `"en-US-AndrewNeural"` with any other supported voice from Edge-TTS.

## **Known Issues**
- Requires an **internet connection** since Edge-TTS is a cloud-based service.
- Some **voices may not be available** in all regions.

## **Future Improvements**
- Add **offline voice support** using **pyttsx3**  
- Implement **real-time speech synthesis**  
- Support for **additional file formats** (PDF, EPUB, etc.)  

## **License**
This project is **open-source** and available for personal and educational use.

---

Let me know if you need modifications! 🚀
