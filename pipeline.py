from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
def run_research_pipeline(topic : str) -> dict:
    state = {}

    #search agent working

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"find recent, reliable and detailed information about {topic}")]
    })

    state["search_result"] = search_result['messages'][-1].content
    print("\n search result: ", state['search_result'])

    #reader agent working

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user",
             f"Based on the following search results about '{topic}',"
             f"pick the most relevant URL and scrape it for deeper content.\n\n"
             f"Search Result: {state['search_result'][:800]}"       )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\n scraped content: ", state['scraped_content'])

    #step 3 - writer chain
    print("step 3 : Writer is drafting the report.....")
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_result']} \n\n"
        f"DETAILED SCRAPPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report
    print("step 4 : Critic is reviewing the report")
    state["feedback"] = critic_chain.invoke({
        "report" : state['report']
    })

    print("\n critic report \n" , state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter the topic you want to research : ")
    run_research_pipeline(topic)