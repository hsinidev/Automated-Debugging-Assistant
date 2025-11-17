import customtkinter as ctk
from tkinter import messagebox
import threading
import ollama

# --- Configuration ---
OLLAMA_MODEL = 'llama3:8b'
DEV_INFO = "powrd by Hsini Mohamed (hsini.web@gmail.com)" 
THEME_FILE = "magic_theme.json"

# --- 1. LLM Worker Thread (Non-Freezing Logic) ---
class DebugWorker(threading.Thread):
    def __init__(self, app, code, traceback):
        super().__init__()
        self.app = app
        self.code = code
        self.traceback = traceback

    def run(self):
        # The System Prompt defines the Agent's structured output
        system_prompt = (
            f"You are a Senior Software Debugging Expert. Your task is to analyze the provided code and traceback "
            f"and provide a three-part structured response ONLY. "
            f"1. A section titled 'Root Cause:' explaining the exact reason for the error. "
            f"2. A section titled 'Line of Fix:' indicating the specific line number and file. "
            f"3. A section titled 'Suggested Code Fix:' providing the corrected, complete code block using markdown syntax."
            f"Be concise, professional, and accurate."
        )
        
        user_prompt = (
            "Analyze the following:\n\n"
            f"### CODE TO ANALYZE:\n{self.code}\n\n"
            f"### TRACEBACK/ERROR MESSAGE:\n{self.traceback}\n"
        )
        
        try:
            response = ollama.generate(
                model=OLLAMA_MODEL, 
                prompt=user_prompt,
                system=system_prompt
            )
            # Safely update GUI on the main thread
            self.app.master.after(0, self.app.on_analysis_complete, True, response['response'])
            
        except Exception as e:
            error_msg = f"Error: Ensure Ollama is running and model '{OLLAMA_MODEL}' is pulled. Detail: {e}"
            self.app.master.after(0, self.app.on_analysis_complete, False, error_msg)

# --- 2. CustomTkinter Application ---
class DebuggingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🐞 Automated Debugging Assistant")
        self.geometry("1000x800")
        
        # Load the external theme JSON file
        try:
            ctk.set_default_color_theme(THEME_FILE)
        except Exception:
            messagebox.showerror("Theme Error", f"Could not load custom theme file: {THEME_FILE}. Ensure it is in the same directory.")
            self.destroy()
            return

        # Configure layout weights for responsive resizing
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(7, weight=1)
        
        self.setup_ui()

    def setup_ui(self):
        # --- Row 0: Main Title ---
        ctk.CTkLabel(self, text="🐞 Automated Debugging Assistant", font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(20, 0)
        )
        
        # --- Row 1: Developer Info ---
        ctk.CTkLabel(self, text=DEV_INFO, font=ctk.CTkFont(size=10)).grid(
            row=1, column=0, columnspan=2, pady=(0, 20)
        )
        
        # --- Row 2: Input Labels ---
        ctk.CTkLabel(self, text="1. Source Code:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=0, padx=20, pady=(5, 0), sticky="w"
        )
        ctk.CTkLabel(self, text="2. Error Traceback:", font=ctk.CTkFont(size=14)).grid(
            row=2, column=1, padx=20, pady=(5, 0), sticky="w"
        )
        
        # --- Row 3: Input Textboxes ---
        self.code_input = ctk.CTkTextbox(self, height=200, activate_scrollbars=True)
        self.code_input.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        self.code_input.insert("0.0", "def calculate(a, b):\n    return a * b\n\nresult = calculate(10, '5')")

        self.traceback_input = ctk.CTkTextbox(self, height=200, activate_scrollbars=True)
        self.traceback_input.grid(row=3, column=1, padx=20, pady=5, sticky="nsew")
        self.traceback_input.insert("0.0", "Traceback (most recent call last):\n  File \"script.py\", line 4, in <module>\n    result = calculate(10, '5')\nTypeError: can't multiply sequence by non-int of type 'str'")
        
        # --- Row 4: Status Label ---
        # NOTE: Removed hardcoded yellow color. The `text_color` is used during updates.
        self.status_label = ctk.CTkLabel(self, text="Status: Ready.")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))
        
        # --- Row 5: Action Button ---
        self.analyze_button = ctk.CTkButton(self, text="Analyze and Fix Code", command=self.start_analysis)
        self.analyze_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew", padx=20)
        
        # --- Row 6: Output Title ---
        ctk.CTkLabel(self, text="3. Debugging Report (Root Cause & Fix):", font=ctk.CTkFont(size=14)).grid(
            row=6, column=0, columnspan=2, padx=20, pady=(15, 5), sticky="w"
        )
        
        # --- Row 7: Output Textbox (Takes up remaining vertical space) ---
        self.output_text = ctk.CTkTextbox(self, state="disabled")
        self.output_text.grid(row=7, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="nsew")

    # --- UI Actions ---
    def start_analysis(self):
        code = self.code_input.get("1.0", "end-1c").strip()
        traceback = self.traceback_input.get("1.0", "end-1c").strip()
        
        if not code or not traceback:
            messagebox.showerror("Input Error", "Please provide both the code and the traceback.")
            return

        # Disable input and set status
        self.analyze_button.configure(state="disabled", text="Analyzing...")
        # FIX: Explicitly set a bright color for the busy state, then reset later
        self.status_label.configure(text="Status: Contacting Ollama...", text_color="#FFD700") # Gold color for visibility
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.insert("0.0", "Processing request, please wait...")
        self.output_text.configure(state="disabled")

        # Start analysis in a separate thread
        worker = DebugWorker(self, code, traceback)
        worker.start()

    # --- Thread Callbacks ---
    def on_analysis_complete(self, success, result):
        self.analyze_button.configure(state="normal", text="Analyze and Fix Code")
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        
        if success:
            self.output_text.insert("0.0", result)
            # FIX: Set success status color to bright green
            self.status_label.configure(text="Status: Analysis Complete.", text_color="#00FF7F") 
        else:
            self.output_text.insert("0.0", f"ERROR: {result}")
            # FIX: Set error status color to bright red
            self.status_label.configure(text="Status: Ollama Error.", text_color="#FF4500")
            
        self.output_text.configure(state="disabled")


if __name__ == "__main__":
    app = DebuggingApp()
    app.mainloop()