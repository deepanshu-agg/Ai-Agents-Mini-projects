# resource_tool.py

from crewai.tools import tool
import json

@tool("Resource Search Tool")
def search_educational_resources(topic: str, target_audience: str = "general") -> str:
    """
    Returns a curated list of educational resources (books, videos, websites)
    for a given topic. This is a mock tool with pre-defined data.
    """
    resources = {
        "books": [],
        "videos": [],
        "websites": []
    }
    topic_lower = topic.lower()

    if "digital logic" in topic_lower:
        resources["books"] = [
            "Digital Design by M. Morris Mano (6th Edition)",
            "Fundamentals of Digital Logic with VHDL Design by Brown and Vranesic"
        ]
        resources["videos"] = [
            "Ben Eater's 8-bit computer project on YouTube",
            "NPTEL lectures on Digital Circuits & Systems"
        ]
        resources["websites"] = [
            "All About Circuits - Digital Logic Section",
            "TutorialsPoint - Digital Circuits Tutorials"
        ]
    elif "machine learning" in topic_lower:
        resources["books"] = [
            "Hands-On Machine Learning by Aurélien Géron",
            "Pattern Recognition and Machine Learning by Christopher Bishop"
        ]
        resources["videos"] = ["Andrew Ng's Machine Learning course on Coursera/YouTube"]
        resources["websites"] = ["Kaggle Learn Courses", "Towards Data Science"]
    else:
        resources["books"] = [f"A Beginner's Guide to {topic}"]
        resources["videos"] = [f"Introduction to {topic} on Khan Academy"]
        resources["websites"] = [f"Official documentation website for {topic}"]

    return json.dumps(resources, indent=2)