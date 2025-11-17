# Automated-Debugging-Assistant
This application showcases the creation of a specialized **Applied AI Agent** designed for **structured problem-solving**.

# 🐞 Automated Debugging Assistant - Agentic LLM

[![Project Status](https://img.shields.io/badge/Status-Project%202%2F100%20Complete-green?style=for-the-badge)](<YOUR-REPOSITORY-URL>)
[![LLM Skill](https://img.shields.io/badge/LLM%20Role-Agentic%20Expert-orange?style=for-the-badge)](https://ollama.com/)
[![Desktop GUI](https://img.shields.io/badge/Desktop%20GUI-CustomTkinter%20(Pro%20Theme)-%237D00A3?style=for-the-badge)](https://customtkinter.tomschimansky.com/)
[![Web Frontend](https://img.shields.io/badge/Web%20Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

A specialized **Applied AI Agent** designed to automate the initial analysis and correction of software errors. This application takes raw code and its associated traceback message, compelling a local LLM to act as a Senior Debugging Expert and provide a structured, actionable fix.

**Developed By:** Hsini Mohamed (hsini.web@gmail.com)

---

## 💡 Project Meaning & Engineering Roles

The core challenge in LLM Engineering is moving models beyond simple chat to solve **structured problems**. This project showcases the following high-demand roles:

### 1. The Debugging Agent (LLM Role)

The Large Language Model is not used for general conversation; it is forced into a highly restricted and expert role via the **System Prompt**. Its job is to perform a multi-step reasoning process:
* **Analyze:** Read the traceback, identify the specific error type (`TypeError`, `NameError`, etc.), and find the corresponding line in the code.
* **Reason:** Determine the logical flaw or syntax mistake causing the error.
* **Generate Structured Output:** Produce a three-part report consistently, which is a key requirement for modern enterprise AI pipelines.

### 2. Dual-Environment Deployment

This project validates proficiency in delivering the same core service across different user needs:

| Deployment Method | Purpose | Technical Skill Demonstrated |
| :--- | :--- | :--- |
| **Streamlit (`debug_assistant_streamlit.py`)** | Easy access via web URL for demonstrations or small teams. | **Rapid Prototyping** and `st.session_state` management. |
| **CustomTkinter (`debug_assistant_gui.py`)** | Native desktop application where privacy and performance are prioritized. | **Non-Blocking Threading** (using `threading` to prevent GUI freeze) and **Custom Theming**. |

---

## ⚙️ Installation & Setup

### 1. Prerequisites

* **Ollama Service:** Must be running in the background.
* **Required Model:** Ensure the `llama3:8b` model is pulled:
    ```bash
    ollama pull llama3:8b
    ```

### 2. Project Setup

Clone the repository and install all required dependencies:

```bash
# Clone and enter your project folder
git clone <YOUR-REPOSITORY-URL>
cd Automated-Debugging-Assistant 

# Install dependencies (Streamlit, Ollama client, CustomTkinter)
pip install streamlit ollama customtkinter

# IMPORTANT: The custom theme file, magic_theme.json, must be in the root directory.

🚀 Running the Project (Dual Modes)
Mode 1: Streamlit Web App (URL Access)
Run the web version for a browser-based experience:

Bash

streamlit run debug_assistant_streamlit.py
Mode 2: CustomTkinter Native Desktop GUI
Run the desktop version to showcase the custom theme and non-blocking performance:

Bash

python debug_assistant_gui.py
📸 Application Walkthrough
The interface is designed for rapid diagnosis.

Input Code (1): Paste the complete source code block with the bug.

Input Traceback (2): Paste the raw error message from the terminal.

Analysis: The background LLM Agent processes the input.

Structured Output (3): The application delivers a clear report, providing the exact fix and the reasoning behind it.

