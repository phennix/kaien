# src/kaien/agent/graph.py
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from kaien.agent.factory import get_llm
from kaien.tools.system import execute_shell, read_file, write_file
from kaien.memory.db import MemoryEngine

# 1. Define Tools
tools = [execute_shell, read_file, write_file]
tool_node = ToolNode(tools)


# 2. Define State
# We use 'add_messages' behavior implicitly if we used MessagesState,
# but defining explicitly helps clarity.
class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: str  # String to hold retrieved memories


# 3. Initialize Components
memory = MemoryEngine()


def retrieve_memory(state: AgentState):
    """
    Look at the last user message and fetch relevant past interactions.
    """
    messages = state["messages"]
    # Find last human message
    last_human = next((m for m in reversed(messages) if isinstance(m, HumanMessage)), None)

    context_str = ""
    if last_human:
        results = memory.search(last_human.content)
        if results:
            context_str = "\n".join([f"- {r}" for r in results])

    return {"context": context_str}


def call_model(state: AgentState):
    """
    The main reasoning node.
    """
    llm = get_llm().bind_tools(tools)

    # Construct prompt with Memory Context
    system_prompt = (
        "You are Kaien, an advanced agentic system for Ubuntu."
        "You have access to the local system via tools."
        "Use them responsibly."
    )

    if state.get("context"):
        system_prompt += f"\n\nRELAVANT MEMORY:\n{state['context']}"

    # We rebuild the message history with our dynamic system prompt
    # Note: LangGraph passes the whole history, so we prepend SystemMessage
    messages = [SystemMessage(content=system_prompt)] + state["messages"]

    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: AgentState):
    """
    Decide if we stop or run tools.
    """
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


# 4. Build Graph
workflow = StateGraph(AgentState)

workflow.add_node("retrieve_memory", retrieve_memory)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Flow: Start -> Retrieve Memory -> Agent Think -> (Tools?) -> End
workflow.set_entry_point("retrieve_memory")
workflow.add_edge("retrieve_memory", "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)
workflow.add_edge("tools", "agent")  # Loop back after tool use

app = workflow.compile()