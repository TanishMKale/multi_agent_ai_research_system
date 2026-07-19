from agents import search_agent,reader_agent,writer_chain,critic_chain

# we will now create a final pipeline fucntion which will run all the agents and chains 
# we will store all the outputs, the reports etc in a dictionary called state which will be
# -returned by this function

def final_research_pipeline(topic:str)->dict:
    
    state = {}

    #step 1: lets put search agent to work as we need links and more info about the topic we desire

    #below is just a prnting pattern for neet printing
    print("\n"+" ="*50)
    print("Step 1 : Search Agent is Running")
    print("\n"+" ="*50)
    #start
    search_agent_object = search_agent()
    search_result=search_agent_object.invoke(
        {"messages":
         [("user",f"Please find the most relevant, reliable and recent search for the given topic:{topic}")]})
    
    state["search_results"] = search_result['messages'][-1].content
    print("Search Result from step1: ",state["search_results"])

    #step 2: time to put reader agent to work

    #below is just a prnting pattern for neet printing
    print("\n"+" ="*50)
    print("Step 2 : Reader Agent is Running")
    print("\n"+" ="*50)
    #start
    reader_agent_object = reader_agent()
    reader_agent_results = reader_agent_object.invoke(
        {"messages":[("user",f"Based on the search results for the '{topic}',"
                      f"Find the most relevant and reliable URL and scrape it for deeper understanding\n\n"
                      f"Search Results:\n {state['search_results'][:800]}"
                      )]}
    )
    
    state["scrape_results"]=reader_agent_results["messages"][-1].content
    print("Reader agent has scrapped the following: ",state["scrape_results"])

    #step 3: invoke the writer chain, refer to the notes, we need to combine the results from above
    # for 'research' in prompt
    
    #below is just a prnting pattern for neet printing
    print("\n"+" ="*50)
    print("Step 2 : Writer chain is invoking")
    print("\n"+" ="*50)

    research_combined = (
        f"SEARCH RESULT : {state['search_results']}\n"
        f"READING / SCRAPE RESULT : {state['scrape_results']}"
    )

    state["report"] = writer_chain.invoke({
        "topic"  : topic,
        "research" : research_combined 
    })

    print("Final report  :",state['report'])

    #step 4 : invoking critic chain
    #below is just a prnting pattern for neet printing
    print("\n"+" ="*50)
    print("Step 2 : Critic chain is invoking")
    print("\n"+" ="*50)

    state['feedback'] = critic_chain.invoke(
        {   
            "topic" : topic,
            "report" :state['report']
        }
    )

    print("Feedback :",state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("Enter the topic you desire : ")
    #call the main func
    final_research_pipeline(topic)