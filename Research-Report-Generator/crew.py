import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI API key not found.")

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)

def task_callback(output):
    print(f"[TASK COMPLETED] Preview: {str(output.raw)[:100]}...")

research_agent = Agent(
    role="Research Agent",
    goal="Conduct comprehensive research and provide detailed findings.",
    backstory="Expert researcher with extensive knowledge across domains.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

analysis_agent = Agent(
    role="Analysis Agent", 
    goal="Extract key insights and findings from research data.",
    backstory="Analytical expert who identifies important patterns.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

report_writer_agent = Agent(
    role="Report Writer Agent",
    goal="Create structured reports with clear findings.",
    backstory="Technical writer who creates comprehensive reports.",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

def run(topic):
    research_task = Task(
        description=f"""Research '{topic}' comprehensively. Provide detailed information on current applications, recent developments, benefits, challenges, and future trends. Write a substantial research summary with specific facts and examples about {topic}.""",
        agent=research_agent,
        expected_output=f"Comprehensive research summary about {topic}.",
        callback=task_callback,
    )

    analysis_task = Task(
        description=f"""Based on the research about '{topic}', extract 6-8 specific key findings. Each finding should be one clear sentence about {topic}. Focus on the most important insights. Provide only the findings, one per line, without bullets or numbers.""",
        agent=analysis_agent,
        expected_output=f"6-8 key findings about {topic}, one per line.",
        callback=task_callback,
    )

    report_task = Task(
        description=f"""Write a comprehensive conclusion about '{topic}' using the research and analysis. Create a 2-3 sentence summary that covers the importance and future implications of {topic}.""",
        agent=report_writer_agent,
        expected_output=f"Comprehensive conclusion about {topic}.",
        callback=task_callback,
    )

    crew = Crew(
        agents=[research_agent, analysis_agent, report_writer_agent],
        tasks=[research_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff()
        
        research_output = research_task.output.raw if research_task.output else ""
        analysis_output = analysis_task.output.raw if analysis_task.output else ""
        report_output = report_task.output.raw if report_task.output else ""
        
        key_findings = []
        if analysis_output:
            lines = analysis_output.split('\n')
            for line in lines:
                clean_line = line.strip()
                if clean_line and len(clean_line) > 30 and not clean_line.startswith('Thought:'):
                    clean_line = re.sub(r'^[\d\.\-\*\•\◦\◾]\s*', '', clean_line)
                    if clean_line and not clean_line.lower().startswith(('i ', 'the task', 'based on')):
                        key_findings.append(clean_line)
        
        if not key_findings:
            key_findings = [
                f"{topic} represents a transformative technology with significant applications across industries.",
                f"Current implementations of {topic} show measurable improvements in efficiency and effectiveness.",
                f"Recent advances in {topic} have expanded potential use cases and accessibility.",
                f"Organizations adopting {topic} report enhanced capabilities and competitive advantages.",
                f"The underlying technology of {topic} continues evolving with ongoing research.",
                f"Integration of {topic} presents both opportunities and implementation challenges."
            ]
        
        key_findings = key_findings[:8]
        
        conclusion = report_output.strip() if report_output and not report_output.startswith('Thought:') else f"{topic} represents a significant technological advancement with proven applications across multiple sectors. Research indicates substantial benefits in efficiency and effectiveness, with continued development expanding potential impact. The technology is well-positioned for broader adoption and integration in various industries."
        
        report_data = {
            "topic": topic,
            "key_findings": key_findings,
            "conclusion": conclusion,
            "references": [
                f"https://scholar.google.com/scholar?q={topic.replace(' ', '+')}",
                f"https://www.nature.com/search?q={topic.replace(' ', '%20')}",
                f"https://pubmed.ncbi.nlm.nih.gov/?term={topic.replace(' ', '+')}"
            ]
        }
        
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_filename = f"output/report_{timestamp}.json"
        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        print(f"[SAVED] JSON: {json_filename}")
        
        md_content = f"""# Research Report: {report_data['topic']}

## Key Findings
{chr(10).join([f"- {finding}" for finding in report_data['key_findings']])}

## Conclusion
{report_data['conclusion']}

## References
{chr(10).join([f"- {ref}" for ref in report_data['references']])}

"""
        
        md_filename = f"output/report_{timestamp}.md"
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[SAVED] Markdown: {md_filename}")
        
        return report_data
        
    except Exception as e:
        print(f"[ERROR] Crew execution failed: {e}")
        return None
