from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain, extract_score

MAX_REVISIONS = 2  # prevents infinite writer<->critic loops


class ResearchState(TypedDict):
    topic: str
    search_result: str
    scraped_content: str
    report: str
    feedback: str
    score: int
    revision_count: int


# ---------- NODES ----------

def search_node(state: ResearchState) -> dict:
    print("\nstep 1: Search agent working...")
    search_agent = build_search_agent()
    result = search_agent.invoke({
        "messages": [("user", f"find recent, reliable and detailed information about {state['topic']}")]
    })
    search_result = result["messages"][-1].content
    print("\n search result: ", search_result)
    return {"search_result": search_result}


def read_node(state: ResearchState) -> dict:
    print("\nstep 2: Reader agent working...")
    reader_agent = build_reader_agent()
    result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{state['topic']}',"
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Result: {state['search_result'][:800]}")]
    })
    scraped_content = result["messages"][-1].content
    print("\n scraped content: ", scraped_content)
    return {"scraped_content": scraped_content}


def write_node(state: ResearchState) -> dict:
    print(f"\nstep 3: Writer drafting report (revision {state.get('revision_count', 0)})...")
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPPED CONTENT : \n {state['scraped_content']}"
    )

    feedback_note = ""
    if state.get("feedback"):
        feedback_note = f"\n\nPrevious critic feedback to address:\n{state['feedback']}"

    report = writer_chain.invoke({
        "topic": state["topic"],
        "research": research_combined + feedback_note
    })
    print("\n Report draft:\n", report)
    return {
        "report": report,
        "revision_count": state.get("revision_count", 0) + 1
    }


def critique_node(state: ResearchState) -> dict:
    print("\nstep 4: Critic reviewing report...")
    feedback = critic_chain.invoke({"report": state["report"]})
    score = extract_score(feedback)
    print(f"\n Critic feedback (score={score}):\n", feedback)
    return {"feedback": feedback, "score": score}


# ---------- CONDITIONAL EDGE ----------

def route_after_critique(state: ResearchState) -> str:
    """If the report scores low and we haven't hit the revision cap, send it back to the writer."""
    if state["score"] < 7 and state["revision_count"] < MAX_REVISIONS:
        print(f"\n Score {state['score']}/10 is low — sending back to Writer for revision.")
        return "revise"
    print(f"\n Final score {state['score']}/10 — pipeline complete.")
    return "done"


# ---------- BUILD GRAPH ----------

graph = StateGraph(ResearchState)

graph.add_node("search", search_node)
graph.add_node("read", read_node)
graph.add_node("write", write_node)
graph.add_node("critique", critique_node)

graph.set_entry_point("search")
graph.add_edge("search", "read")
graph.add_edge("read", "write")
graph.add_edge("write", "critique")

graph.add_conditional_edges(
    "critique",
    route_after_critique,
    {
        "revise": "write",
        "done": END
    }
)

compiled_graph = graph.compile()


# ---------- ENTRY POINT (same signature as before — main.py needs no changes) ----------

def run_research_pipeline(topic: str) -> dict:
    initial_state: ResearchState = {
        "topic": topic,
        "search_result": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "score": 0,
        "revision_count": 0,
    }
    final_state = compiled_graph.invoke(initial_state)
    return final_state


if __name__ == "__main__":
    topic = input("\n Enter the topic you want to research : ")
    result = run_research_pipeline(topic)
    print("\n\n=== FINAL REPORT ===\n", result["report"])
    print("\n\n=== FINAL FEEDBACK ===\n", result["feedback"])
