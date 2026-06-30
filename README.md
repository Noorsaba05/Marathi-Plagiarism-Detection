# Hybrid Semantic & Cross-Language Plagiarism Detection System for Marathi Academic Text 📝

A plagiarism detection system for Marathi academic writing, combining monolingual semantic similarity with cross-language (Marathi–English) detection. Built during a research internship under Dr. Rucha Samant and extended as an MCA Problem-Based Learning (PBL) project.

📄 Paper accepted at **ICETES-2026** (Paper ID 184), presented at JIT Nashik, April 2026.

## Overview

Most plagiarism detection tools are built for English and struggle with Indic languages like Marathi, and they generally don't catch plagiarism that's been translated across languages. This project addresses both gaps by combining two detection pipelines into a single weighted verdict.

## Tech Stack

- **Language:** Python
- **Monolingual detection:** MahaSBERT (semantic similarity within Marathi text)
- **Cross-language detection:** IndicTrans2 / Google Translate (translate, then compare)
- **Similarity search:** FAISS

## How It Works

1. **Monolingual check** — Marathi input text is embedded using MahaSBERT and compared against a Marathi reference corpus for semantic similarity.
2. **Cross-language check** — Text is translated (via IndicTrans2 / Google Translate) and compared against English/Marathi sources to catch cross-language plagiarism.
3. **Weighted scoring** — Final plagiarism score is computed as:
   ```
   Final Score = 0.6 × Monolingual Score + 0.4 × Cross-Language Score
   ```
4. **Verdict tiers** — The final score is mapped to one of five verdict tiers (e.g. Original, Minor Similarity, Moderate Plagiarism, High Plagiarism, Severe Plagiarism).

## Project Status

This repository documents the system built during the research internship and PBL coursework. (Update this section with current setup/run instructions once the code is finalized and uploaded.)

## Getting Started

```bash
git clone https://github.com/Noorsaba05/Marathi-Plagiarism-Detection.git
cd Marathi-Plagiarism-Detection
pip install -r requirements.txt
```
*(Add exact dependencies — e.g. sentence-transformers, faiss-cpu, indictrans2 client/SDK — once finalized.)*

## What I Learned

- Working with transformer-based semantic similarity models (MahaSBERT) for a low-resource language
- Building a cross-language NLP pipeline using machine translation
- Designing a weighted, tiered scoring system for a real-world academic integrity problem
- Taking a research idea from prototype to a peer-reviewed, conference-presented paper

## Publication

**Paper Title:** Hybrid Semantic and Cross-Language Plagiarism Detection System for Marathi Academic Text
**Conference:** ICETES-2026, JIT Nashik (April 2026)
**Paper ID:** 184

## Author

**Noorsaba Shaikh**
📧 noorsabashaikh03@gmail.com
🔗 [GitHub](https://github.com/Noorsaba05) | [LinkedIn](https://www.linkedin.com/in/noorsaba-shaikh-2949682b1)

*Research guided by Dr. Rucha Samant.*
