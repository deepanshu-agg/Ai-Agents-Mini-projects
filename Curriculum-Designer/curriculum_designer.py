import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from resource_tool import search_educational_resources

load_dotenv()
os.environ["CREWAI_TELEMETRY"] = "False"

class CurriculumDesignerSystem:
    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

        self.llm = LLM(
            model="gemini/gemini-2.5-flash",
            temperature=0.8,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.setup_agents()

    def setup_agents(self):
        self.lead_designer = Agent(role='Lead Curriculum Designer', goal='Design a comprehensive curriculum outline.', backstory='Expert educator specializing in technical subjects.', verbose=True, llm=self.llm, allow_delegation=False)
        self.content_specialist = Agent(role='Instructional Content Creator', goal='Flesh out learning materials for a curriculum outline.', backstory='Skilled writer who creates engaging educational content.', verbose=True, llm=self.llm, allow_delegation=False)
        self.assessment_specialist = Agent(role='Assessment Design Specialist', goal='Develop a comprehensive assessment strategy.', backstory='Expert in educational evaluation and creating fair assessments.', verbose=True, llm=self.llm, allow_delegation=False)
        self.resource_specialist = Agent(role='Educational Resource Curator', goal='Find and list relevant external resources.', backstory='Digital librarian skilled in finding supplementary materials.', verbose=True, llm=self.llm, tools=[search_educational_resources], allow_delegation=False)
        
    def run_curriculum_design(self, topic, target_audience="intermediate", duration="8 weeks"):
        print(f"🎯 Starting curriculum design for: {topic}")

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        safe_topic = "".join(c for c in topic if c.isalnum()).lower()
        safe_audience = "".join(c for c in target_audience if c.isalnum()).lower()
        file_prefix = f"{safe_topic}_{safe_audience}"
        past_content = None

        try:
            existing_files = sorted([f for f in os.listdir(output_dir) if f.startswith(file_prefix) and f.endswith('.json')], reverse=True)
            if existing_files:
                print(f"🧠 Found existing module for '{topic}' and '{target_audience}'.")
                action = input("Do you want to [r]e-use, [u]pdate, or [c]reate new? ").lower()
                latest_file = os.path.join(output_dir, existing_files[0])
                if action == 'r':
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                elif action == 'u':
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        past_content = f.read()
        except FileNotFoundError:
            pass

        outline_task = Task(description=f"Create a week-by-week curriculum outline for '{topic}' for '{target_audience}' over {duration}. Group weeks into logical Modules. For each week, define a title, topics, and learning outcomes.", expected_output=f"A detailed markdown-formatted weekly outline, grouped by Modules, for the '{topic}' course.", agent=self.lead_designer)
        material_task = Task(description=f"Based on the module outline for '{topic}', create a detailed list of learning materials. For each week, suggest specific content like lecture notes, code examples, and case studies.", expected_output="A markdown-formatted list of learning materials, structured week-by-week.", agent=self.content_specialist, context=[outline_task])
        assessment_task = Task(description=f"Based on the module outline for '{topic}', design a detailed assessment plan. Include a mix of quizzes, assignments, a mid-term, and a final project, with grade weights.", expected_output="A markdown-formatted assessment plan with descriptions and grade weighting.", agent=self.assessment_specialist, context=[outline_task])
        resource_task = Task(description=f"Find and curate external resources for '{topic}'. Use the Resource Search Tool to find relevant books, videos, and websites.", expected_output="A markdown-formatted list of curated resources, including books, videos, and websites.", agent=self.resource_specialist)

        crew = Crew(
            agents=[self.lead_designer, self.content_specialist, self.assessment_specialist, self.resource_specialist],
            tasks=[outline_task, material_task, assessment_task, resource_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff(inputs={"topic": topic, "target_audience": target_audience})

        if result and hasattr(result, 'tasks_output') and len(result.tasks_output) == 4:
            final_json = {
                "topic": topic, "target_audience": target_audience,
                "module_outline": result.tasks_output[0].raw,
                "learning_material": result.tasks_output[1].raw,
                "assessments": result.tasks_output[2].raw,
                "resources": result.tasks_output[3].raw
            }
            return final_json
        else:
            print("Warning: Crew did not return the expected four task outputs.")
            return {"raw_output": str(result)}