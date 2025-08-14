# Research Report Generator

Concise project summary

This project is a multi-agent research pipeline that automates topic research, insight extraction, and structured report generation using CrewAI and a cloud LLM.

Key features
- Sequential multi-agent workflow: Research → Analysis → Report Writing
- Structured outputs: JSON and Markdown for programmatic and human-friendly use
- Task callbacks and progress logging for observability
- Simple web-search integration (DuckDuckGo) for gathering sources

Repository layout (this folder)
```
Research-Report-Generator/
├── crew.py            # Agent definitions and orchestration (core logic)
├── main.py            # CLI entrypoint: run the pipeline for a topic
├── requirements.txt   # Dependencies specific to this project
└── output/            # Generated reports (JSON and Markdown)
```

Prerequisites
- Python 3.10+ (tested with 3.12)
- Internet connection for search and LLM API calls
- A virtual environment is highly recommended

Environment & API keys
Create a `.env` file in this project folder (or the repo root) containing your LLM API key. Example:

```text
GOOGLE_API_KEY=your_gemini_api_key
# or if the code expects GEMINI_API_KEY, set that variable instead
```

Install dependencies
Install dependencies for this project (Windows PowerShell example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

How to run
Use the `main.py` script to run a research pipeline for any topic.

```powershell
cd Research-Report-Generator
python main.py "Your Research Topic"
```

Example

```powershell
python main.py "Artificial Intelligence in Healthcare"
```

Output
- JSON: `output/report_<timestamp>.json` — structured fields: `topic`, `key_findings`, `conclusion`, `references`
- Markdown: `output/report_<timestamp>.md` — human-readable report suitable for publishing

How it works (high level)
1. Research agent gathers web content and topical information (search tool integration).
2. Analysis agent extracts and synthesizes key findings from raw research text.
3. Report writer agent composes a concise conclusion and formats results into JSON and Markdown.
4. Task callbacks print progress after each agent completes its stage.

Extending the project
- Swap or configure the LLM backend by updating environment variables and `crew.py` LLM instantiation.
- Improve the search tool to use additional data sources or an API with richer metadata.
- Add unit tests around parsing and file writing for robustness.

Notes
- The code is designed for demonstrations and educational experiments. For production use, add error handling, rate limiting, and proper secret management.

License & credits
This project was developed for coursework and learning. It uses CrewAI, DuckDuckGo search tooling, and a cloud LLM.
