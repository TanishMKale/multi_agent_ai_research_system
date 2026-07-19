import streamlit as st
from agents import search_agent, reader_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide"
)

# ---------------------------------------------------------------------------
# Session state setup
# ---------------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of state dicts, one per run

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("🔎 Research Pipeline")
    st.caption("Search Agent → Reader Agent → Writer Chain → Critic Chain")

    st.divider()
    st.subheader("Past Runs")
    if st.session_state.history:
        for i, run in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - i
            if st.button(f"{idx}. {run['topic'][:35]}", key=f"hist_{idx}"):
                st.session_state.selected_run = run
    else:
        st.caption("No runs yet.")

    st.divider()
    if st.button("🗑️ Clear history"):
        st.session_state.history = []
        st.session_state.pop("selected_run", None)
        st.rerun()

# ---------------------------------------------------------------------------
# Header + input
# ---------------------------------------------------------------------------
st.title("Multi-Agent AI Research System")
st.caption("Watch each agent work in real time, then read the final report and critique.")

topic = st.text_input("Enter a research topic", placeholder="e.g. Latest advances in solid-state batteries")
run_clicked = st.button("🚀 Run Research Pipeline", type="primary", use_container_width=False)


def render_state(state: dict, topic: str):
    """Render a completed/partial pipeline state in tabs."""
    tab_search, tab_read, tab_report, tab_feedback = st.tabs(
        ["🔍 Search Results", "📄 Scrape Results", "📝 Final Report", "🧐 Critic Feedback"]
    )

    with tab_search:
        if "search_results" in state:
            st.markdown(state["search_results"])
        else:
            st.info("No search results yet.")

    with tab_read:
        if "scrape_results" in state:
            st.markdown(state["scrape_results"])
        else:
            st.info("No scrape results yet.")

    with tab_report:
        if "report" in state:
            st.markdown(state["report"])
            st.download_button(
                "⬇️ Download report (.md)",
                data=str(state["report"]),
                file_name=f"{topic[:40].strip().replace(' ', '_') or 'report'}.md",
                mime="text/markdown",
            )
        else:
            st.info("No report generated yet.")

    with tab_feedback:
        if "feedback" in state:
            st.markdown(state["feedback"])
        else:
            st.info("No feedback yet.")


# ---------------------------------------------------------------------------
# Run pipeline (with live step-by-step UI)
# ---------------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        state = {}

        with st.status("Running research pipeline...", expanded=True) as status:

            # Step 1: Search Agent
            st.write("**Step 1 — Search Agent** is searching the web...")
            search_agent_object = search_agent()
            search_result = search_agent_object.invoke(
                {"messages": [
                    ("user", f"Please find the most relevant, reliable and recent search for the given topic:{topic}")
                ]}
            )
            state["search_results"] = search_result["messages"][-1].content
            st.write("✅ Search complete.")

            # Step 2: Reader Agent
            st.write("**Step 2 — Reader Agent** is scraping the top source...")
            reader_agent_object = reader_agent()
            reader_agent_results = reader_agent_object.invoke(
                {"messages": [
                    ("user",
                     f"Based on the search results for the '{topic}',"
                     f"Find the most relevant and reliable URL and scrape it for deeper understanding\n\n"
                     f"Search Results:\n {state['search_results'][:800]}")
                ]}
            )
            state["scrape_results"] = reader_agent_results["messages"][-1].content
            st.write("✅ Scraping complete.")

            # Step 3: Writer Chain
            st.write("**Step 3 — Writer Chain** is drafting the report...")
            research_combined = (
                f"SEARCH RESULT : {state['search_results']}\n"
                f"READING / SCRAPE RESULT : {state['scrape_results']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            st.write("✅ Report drafted.")

            # Step 4: Critic Chain
            st.write("**Step 4 — Critic Chain** is reviewing the report...")
            state["feedback"] = critic_chain.invoke({
                "topic": topic,
                "report": state["report"]
            })
            st.write("✅ Feedback ready.")

            status.update(label="Pipeline complete!", state="complete", expanded=False)

        # Save to history
        run_record = {"topic": topic, **state}
        st.session_state.history.append(run_record)
        st.session_state.selected_run = run_record

        st.success(f"Research complete for: **{topic}**")
        render_state(state, topic)

# ---------------------------------------------------------------------------
# Show a previously selected run (from sidebar) when not actively running
# ---------------------------------------------------------------------------
elif "selected_run" in st.session_state:
    run = st.session_state.selected_run
    st.info(f"Showing past run: **{run['topic']}**")
    render_state(run, run["topic"])
else:
    st.caption("👆 Enter a topic and click **Run Research Pipeline** to get started.")