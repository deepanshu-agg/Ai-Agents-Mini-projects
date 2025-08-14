# Curriculum Designer

Project summary

This project is a hierarchical multi-agent system that automates the creation of educational modules. A lead designer agent orchestrates specialist agents to produce structured course content, assessments, and curated resources.

Key features
- Orchestrator (lead) agent delegating to content, assessment, and resource curator agents
- Persistent memory to store and reuse previously generated modules with an option to update
- Structured outputs: JSON for programmatic consumption and DOCX for ready-to-use documents
- A mock `ResourceSearchTool` that can be extended to integrate real resource APIs

Repository layout (this folder)
```
Curriculum-Designer/
├── curriculum_designer.py   # Orchestration and agent setup
├── main.py                  # CLI entrypoint: generate a curriculum module
├── resource_tool.py         # Custom tool for resource curation (mock implementation)
├── requirements.txt         # Dependencies for this mini project
└── output/                  # Generated modules (.json, .docx)
```

Prerequisites
- Python 3.10+ (tested with 3.12)
- Internet connection for LLM and any external tools
- Virtual environment recommended

Environment & API keys
Create a `.env` file in this folder or repo root with your LLM API key:

```text
GOOGLE_API_KEY=your_gemini_api_key
```

Install dependencies (PowerShell example)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

How to run
Run the main script and pass topic and target audience:

```powershell
cd Curriculum-Designer
python main.py "Topic" "Target Audience"
```

Example

```powershell
python main.py "Digital Logic Design" "Undergraduate Students"
```

Output
- JSON: `output/<topic>_<audience>_<timestamp>.json` — includes: `topic`, `target_audience`, `module_outline`, `learning_material`, `assessments`, `resources`
- DOCX: `output/<topic>_<audience>_<timestamp>.docx` — formatted curriculum document ready for distribution

How it works (high level)
1. Lead Designer agent receives topic and target audience and creates an outline.
2. Content Creator fills out learning material per outline sections.
3. Assessment Designer generates quizzes and assignments.
4. Resource Curator uses `resource_tool.py` to assemble suggested readings and multimedia links.
5. Outputs are combined and saved; persistent memory allows reuse of existing modules.

Extending the project
- Replace or enhance `resource_tool.py` to query books, video platforms, or academic APIs.
- Persist modules into a database or vector store for richer retrieval and updates.
- Add more specialist agents (e.g., Accessibility Specialist, Pedagogy Reviewer).

Notes
- The provided resource tool is a mock. For production use, implement robust scraping or API integrations and follow copyright/licensing rules for curated materials.

License & credits
Developed for learning purposes. Uses CrewAI, python-docx, and a cloud LLM.
