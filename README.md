# ⚡ SecOps AI Command Center: Attacker vs Defender Agents

An autonomous, multi-agent cybersecurity framework that performs real-time vulnerability scanning, language identification, and self-healing code remediation. Built with **Flask**, **Ollama**, and **Qwen2.5-Coder**, this project provides a dual-panel Cyber SOC Command Center UI to demonstrate live adversarial probing and automated DevSecOps patching across multiple programming languages.

## 🌟 Key Features

* **🌐 Multi-Language Support:** Automatically detects the target source code language (Python, JavaScript, C++, Java, PHP, Go, etc.) and preserves the original programming language during patching.

* **🤖 Attacker Agent (Offensive Recon):** Scans code for critical vulnerabilities (SQL Injection, XSS, Command Injection, Insecure Deserialization) and generates comprehensive security audit reports.

* **🛡️ Defender Agent (DevSecOps Remediation):** Generates targeted patches to fix identified security flaws and automatically overwrites the vulnerable file on disk.

* **💻 Interactive Cyber Command Center UI:** A responsive split-screen terminal interface built with Flask that displays real-time execution logs and dynamic threat status badges (`VULNERABLE` / `SECURE`).

* **🏠 100% Local & Privacy-First:** Powered locally by **Ollama**, ensuring no source code is sent to external third-party cloud services.

## 🏗️ Architecture & Workflow

```
       [ Target Source File ]
                 │
                 ▼
   ┌──────────────────────────┐
   │  0. Language Classifier  │ ──► Identifies language (Python, JS, C++, etc.)
   └──────────────────────────┘
                 │
                 ▼
   ┌──────────────────────────┐
   │  1. Attacker Agent Audit │ ──► Audits code & extracts vulnerability flags
   └──────────────────────────┘
                 │
                 ▼
   ┌──────────────────────────┐
   │  2. Defender Agent Patch │ ──► Generates fix & rewrites source file on disk
   └──────────────────────────┘
                 │
                 ▼
   ┌──────────────────────────┐
   │  3. Re-Audit & Verify    │ ──► Confirms fix success and zero residual flags
   └──────────────────────────┘

```

## 🛠️ Tech Stack

* **Backend Engine:** Python 3.10+

* **LLM Engine:** [Ollama](https://ollama.com/) running `qwen2.5-coder:7b`

* **Web Framework:** Flask

* **Frontend UI:** Custom HTML5 / CSS3 (Terminal SOC Theme)

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have [Ollama installed](https://ollama.com/) and download the recommended model:

```
ollama pull qwen2.5-coder:7b

```

### 2. Clone the Repository

```
git clone https://github.com/your-username/secops-ai-orchestrator.git
cd secops-ai-orchestrator

```

### 3. Install Dependencies

```
pip install flask ollama

```

### 4. Running the Application

Start the Flask server:

```
python app.py

```

Open your web browser and navigate to:

```
http://127.0.0.1:5000

```

## 🕹️ Usage Instructions

1. **Specify Target:** Enter the full absolute path of any source code file on your machine (e.g., `C:\projects\vulnerable_app.py` or `/home/user/app.js`).

2. **Step 0: Detect Language:** Click **`0. Detect Language`** to run the classifier agent and verify syntax identification.

3. **Step 1: Run Attacker Audit:** Click **`1. Run Attacker Audit`** to perform offensive reconnaissance. If vulnerabilities are detected, the status badge updates to `VULNERABLE` with detailed explanations.

4. **Step 2: Run Defender Patch:** Click **`2. Run Defender Patch`** to automatically generate a secure fix and overwrite the target file on disk.

5. **Step 3: Verify Fix:** Click **`3. Verify Fix`** to run a post-remediation re-audit and confirm that zero security flags remain.

## 📁 Repository Structure

```
├── agents.py     # Core agent logic (Classifier, Attacker, Universal Defender)
├── app.py        # Flask server routes & cyber command-center HTML/CSS UI
└── README.md     # Project documentation
