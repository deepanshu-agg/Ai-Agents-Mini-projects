import sys
from crew import run

if __name__ == "__main__":
    topic = "Artificial Intelligence in Healthcare"
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    
    print("=" * 80)
    print("🤖 MULTI-AGENT RESEARCH CREW - ASSIGNMENT 1")
    print("=" * 80)
    print("CrewAI Multi-Agent System for Research Report Generation")
    print("")
    print("📋 ASSIGNMENT REQUIREMENTS:")
    print("✅ Three Agents: Research → Analysis → Report Writing")
    print("")
    print(f"📄 Research Topic: {topic}")
    print("=" * 80)
    
    try:
        report = run(topic)
        
        if report:
            print("\n" + "=" * 80)
            print("✅ RESEARCH COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            
            if report.get('key_findings'):
                print("\n📋 KEY FINDINGS:")
                for i, finding in enumerate(report['key_findings'], 1):
                    print(f"  {i}. {finding}")

            if report.get('conclusion'):
                print(f"\n📝 CONCLUSION:")
                print(f"  {report['conclusion']}")

            if report.get('references'):
                print(f"\n📚 REFERENCES ({len(report['references'])} sources):")
                for i, ref in enumerate(report['references'], 1):
                    print(f"  {i}. {ref}")
            
            print("\n" + "=" * 80)
            print("ALL ASSIGNMENT REQUIREMENTS FULFILLED!")
        print("=" * 80)
                
    except Exception as e:
        print("❌ ERROR OCCURRED:")
        print(f"Error: {e}")
        print("Please check your configuration and try again.")
        import traceback
        traceback.print_exc()
