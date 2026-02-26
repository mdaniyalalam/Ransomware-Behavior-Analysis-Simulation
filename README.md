# 🛡️ Ransomware Behavior Analysis Simulation

**Internal backend reference:** Cryptox  
**Authors:** Muhammad Daniyal Alam, Muhammad Rohaan Zaidi, Hassan Arif  
**University:** National University of Computer and Emerging Sciences, Karachi Campus  
**Course:** Cyber Security (CY2004)  
**Instructor:** Ms. Abeer Gauher

---

## ⚠️ Ethical & Safety Disclaimer

> **This project is strictly an educational tool designed for behavioral analysis and cybersecurity awareness.**  
>
> All low-level C++ file I/O operations and memory manipulations have been **strictly abstracted into architectural pseudocode**.  
>
> This repository is completely **defanged** and poses **no threat to host systems**.  
>
> It demonstrates defensive programming concepts, including **non-bypassable pre-encryption automated backups** (a "Kill Switch").

---

## 📖 Project Overview

Encryption is a double-edged sword: it protects sensitive information, but can be weaponized by malicious actors to hold data hostage.

This repository contains an **educational simulation** that demonstrates the mechanics of modern ransomware attacks in a **controlled, fail-safe environment**.

By deconstructing the attack vector into its core components:

- **Cryptography**  
- **File system manipulation**  
- **Social engineering**

…the project provides a structured view of the ransomware threat model.

**Objectives:**

- Study behavioral patterns of cryptographic threats  
- Demonstrate hybrid encryption workflows  
- Highlight the importance of robust backup strategies

---

## ⚙️ System Architecture

The project is divided into **two conceptual layers**, demonstrating modular software design and inter-process communication (IPC):

### 1️⃣ Behavioral Frontend (Python)

- Built using **CustomTkinter**  
- Simulates real-world ransomware psychological tactics:
  - Dynamic glitch effects  
  - High-pressure countdown timer  
  - Full-screen ransom interface  
  - Simulated payment gateway  

This layer models the **social engineering component** of ransomware attacks.

### 2️⃣ Cryptographic Engine (C++ Architecture Blueprint)

An abstracted backend design outlining a hybrid encryption workflow using **Crypto++ concepts**:

- AES-256-CBC for file encryption  
- RSA-2048 for secure session key locking  
- HMAC-SHA256 for integrity verification  
- Controlled memory management design  

> 📌 The backend is intentionally provided as **architectural pseudocode only**.  
> See `backend_architecture_pseudocode.md` for details.

---

## 🔍 Core Concepts Demonstrated

### 🔐 Hybrid Cryptography
- Symmetric encryption (**AES-256-CBC**) for fast file processing  
- Asymmetric encryption (**RSA-2048**) to secure AES session keys

### 🧾 Data Integrity
- Encrypt-then-MAC workflow  
- HMAC-SHA256 for tamper detection

### 🛡️ Failsafe Mechanisms
- Automated pre-encryption backup routine  
- Zero data loss design  
- Built-in recovery workflow

### 🧠 Social Engineering Simulation
- Countdown pressure tactics  
- Threat-style ransom messaging  
- Fake payment portal  
- Psychological UI manipulation patterns

---

## 🔄 Execution Flow

The simulation models the full lifecycle of a ransomware attack:

### 1️⃣ Initialization Phase
- Persistent RSA Master Keys are generated  
- System prepares controlled simulation environment

### 2️⃣ Simulation Phase (Infection)
- Target files are automatically backed up  
- AES encryption is simulated  
- AES session key is locked using RSA Public Key

### 3️⃣ Extortion Phase
- Full-screen ransomware UI activates  
- Glitch animations & visual distortion effects  
- 24-hour countdown timer begins  
- Simulated ransom instructions displayed

### 4️⃣ Resolution Phase
- User accesses the mock **"Nexus Payment Gateway"**  
- Enters simulated payment credentials  
- Payment authorization is faked for demonstration

### 5️⃣ Recovery Phase
- RSA Private Key unlocks AES session key  
- HMAC integrity verification is performed  
- Files are restored from backup

---


**File Descriptions:**

- `main.py` – Complete Python source code for the behavioral simulation frontend.  
- `backend_architecture_pseudocode.md` – Abstracted C++ architectural blueprint and cryptographic workflow logic.    
- `assets/` – Screenshots of the CustomTkinter UI.

---

## 🧪 Educational Objectives

This project was developed to:

- Analyze ransomware behavioral patterns  
- Demonstrate secure cryptographic architecture  
- Emphasize defense-first design  
- Showcase modular system separation  
- Promote cybersecurity awareness

---

## 🏫 Academic Context

Developed as part of the Cyber Security (CY2004) course requirement.

This project demonstrates applied knowledge of:
- Cryptography
- Secure System Design
- Threat Modeling
- Human-Centered Security
- Defensive Programming

---

## 📜 License

**MIT License** – Use strictly for educational and research purposes. Do not attempt to deploy or misuse for malicious purposes.
