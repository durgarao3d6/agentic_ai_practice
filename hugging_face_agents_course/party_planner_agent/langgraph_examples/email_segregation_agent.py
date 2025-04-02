# import os
# from typing import TypedDict, List, Dict, Any, Optional
# from dotenv import load_dotenv
# from langgraph.graph import StateGraph, START, END
# from langchain_openai import ChatOpenAI
# from langchain_core.messages import HumanMessage, AIMessage

# from langfuse.callback import CallbackHandler

# # Initialize Langfuse CallbackHandler for LangGraph/Langchain (tracing)
# langfuse_handler = CallbackHandler()

# load_dotenv()

# class EmailState(TypedDict):
#     # The email being processed
#     email: Dict[str, Any]  # Contains subject, sender, body, etc.

#     # Category of the email
#     email_category: Optional[str]

#     # reason of spam
#     spam_reason: Optional[str]
    
#     # Analysis and decisions
#     is_spam: Optional[bool]

#     # Reason why the email was marked as spam
#     spam_reason: Optional[str]

#     # Category of the email (inquiry, complaint, etc.)
#     email_category: Optional[str]
    
#     # Response generation
#     draft_response: Optional[str]
    
#     # Processing metadata
#     messages: List[Dict[str, Any]]  # Track conversation with LLM for analysis

#     # Initialize our LLM
# model = ChatOpenAI(temperature=0)

# def read_email(state: EmailState):
#     """Alfred reads and logs the incoming email"""
#     email = state["email"]
    
#     # Here we might do some initial preprocessing
#     print(f"Alfred is processing an email from {email['sender']} with subject: {email['subject']}")
    
#     # No state changes needed here
#     return {}

# def classify_email(state: EmailState):
#     """Alfred uses an LLM to determine if the email is spam or legitimate"""
#     email = state["email"]
    
#     # Prepare our prompt for the LLM
#     prompt = f"""
#     As Alfred the butler, analyze this email and determine if it is spam or legitimate.
    
#     Email:
#     From: {email['sender']}
#     Subject: {email['subject']}
#     Body: {email['body']}
    
#     First, determine if this email is spam. If it is spam, explain why.
#     If it is legitimate, categorize it (inquiry, complaint, thank you, etc.).
#     """
    
#     # Call the LLM
#     messages = [HumanMessage(content=prompt)]
#     response = model.invoke(messages)
    
#     # Simple logic to parse the response (in a real app, you'd want more robust parsing)
#     response_text = response.content.lower()
#     is_spam = "spam" in response_text and "not spam" not in response_text
    
#     # Extract a reason if it's spam
#     spam_reason = None
#     if is_spam and "reason:" in response_text:
#         spam_reason = response_text.split("reason:")[1].strip()
    
#     # Determine category if legitimate
#     email_category = None
#     if not is_spam:
#         categories = ["inquiry", "complaint", "thank you", "request", "information"]
#         for category in categories:
#             if category in response_text:
#                 email_category = category
#                 break
    
#     # Update messages for tracking
#     new_messages = state.get("messages", []) + [
#         {"role": "user", "content": prompt},
#         {"role": "assistant", "content": response.content}
#     ]
    
#     # Return state updates
#     return {
#         "is_spam": is_spam,
#         "spam_reason": spam_reason,
#         "email_category": email_category,
#         "messages": new_messages
#     }

# def handle_spam(state: EmailState):
#     """Alfred discards spam email with a note"""
#     print(f"Alfred has marked the email as spam. Reason: {state['spam_reason']}")
#     print("The email has been moved to the spam folder.")
    
#     # We're done processing this email
#     return {}

# def draft_response(state: EmailState):
#     """Alfred drafts a preliminary response for legitimate emails"""
#     email = state["email"]
#     category = state["email_category"] or "general"
    
#     # Prepare our prompt for the LLM
#     prompt = f"""
#     As Alfred the butler, draft a polite preliminary response to this email.
    
#     Email:
#     From: {email['sender']}
#     Subject: {email['subject']}
#     Body: {email['body']}
    
#     This email has been categorized as: {category}
    
#     Draft a brief, professional response that Mr. Hugg can review and personalize before sending.
#     """
    
#     # Call the LLM
#     messages = [HumanMessage(content=prompt)]
#     response = model.invoke(messages)
    
#     # Update messages for tracking
#     new_messages = state.get("messages", []) + [
#         {"role": "user", "content": prompt},
#         {"role": "assistant", "content": response.content}
#     ]
    
#     # Return state updates
#     return {
#         "draft_response": response.content,
#         "messages": new_messages
#     }

# def notify_mr_hugg(state: EmailState):
#     """Alfred notifies Mr. Hugg about the email and presents the draft response"""
#     email = state["email"]
    
#     print("\n" + "="*50)
#     print(f"Sir, you've received an email from {email['sender']}.")
#     print(f"Subject: {email['subject']}")
#     print(f"Category: {state['email_category']}")
#     print("\nI've prepared a draft response for your review:")
#     print("-"*50)
#     print(state["draft_response"])
#     print("="*50 + "\n")
    
#     # We're done processing this email
#     return {}

# def route_email(state: EmailState) -> str:
#     """Determine the next step based on spam classification"""
#     if state["is_spam"]:
#         return "spam"
#     else:
#         return "legitimate"
    
# # Create the graph
# email_graph = StateGraph(EmailState)

# # Add nodes
# # Add nodes with unique names that don't conflict with state keys
# email_graph.add_node("read_email_step", read_email)
# email_graph.add_node("classify_email_step", classify_email)
# email_graph.add_node("handle_spam_step", handle_spam)
# email_graph.add_node("create_draft_response", draft_response)  # Changed from "draft_response"
# email_graph.add_node("notify_step", notify_mr_hugg)  # Changed from "notify_mr_hugg"

# # Start the edges
# email_graph.add_edge(START, "read_email_step")
# # Add edges - defining the flow
# email_graph.add_edge("read_email_step", "classify_email_step")

# # Add conditional branching from classify_email
# email_graph.add_conditional_edges(
#     "classify_email_step",
#     route_email,
#     {
#         "spam": "handle_spam_step",
#         "legitimate": "create_draft_response"  # Updated to match new node name
#     }
# )

# # Add the final edges
# email_graph.add_edge("handle_spam_step", END)
# email_graph.add_edge("create_draft_response", "notify_step")  # Updated to match new node name
# email_graph.add_edge("notify_step", END)

# # Compile the graph
# compiled_graph = email_graph.compile()

# # Example legitimate email
# legitimate_email = {
#     "sender": "john.smith@example.com",
#     "subject": "Question about your services",
#     "body": "Dear Mr. Hugg, I was referred to you by a colleague and I'm interested in learning more about your consulting services. Could we schedule a call next week? Best regards, John Smith"
# }

# # Example spam email
# spam_email = {
#     "sender": "winner@lottery-intl.com",
#     "subject": "YOU HAVE WON $5,000,000!!!",
#     "body": "CONGRATULATIONS! You have been selected as the winner of our international lottery! To claim your $5,000,000 prize, please send us your bank details and a processing fee of $100."
# }

# # Process the legitimate email
# print("\nProcessing legitimate email...")
# legitimate_result = compiled_graph.invoke({
#     "email": legitimate_email,
#     "is_spam": None,
#     "spam_reason": None,
#     "email_category": None,
#     "draft_response": None,
#     "messages": []
# })

# # Process the spam email
# print("\nProcessing spam email...")
# spam_result = compiled_graph.invoke({
#     "email": spam_email,
#     "is_spam": None,
#     "spam_reason": None,
#     "email_category": None,
#     "draft_response": None,
#     "messages": []
# })

# # Process legitimate email
# legitimate_result = compiled_graph.invoke(
#     input={"email": legitimate_email, "is_spam": None, "spam_reason": None, "email_category": None, "draft_response": None, "messages": []},
#     config={"callbacks": [langfuse_handler]}
# )

# compiled_graph.get_graph().draw_mermaid_png()

import os
from typing import TypedDict, List, Dict, Any, Optional
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.callback import CallbackHandler

load_dotenv()

# Initialize Langfuse CallbackHandler
langfuse_handler = CallbackHandler()

class EmailState(TypedDict):
    # The email being processed
    email: Dict[str, Any]  # Contains subject, sender, body, etc.
    
    # Analysis and decisions
    is_spam: Optional[bool]
    spam_reason: Optional[str]
    email_category: Optional[str]
    
    # Response generation
    draft_response: Optional[str]
    
    # Processing metadata
    messages: List[Dict[str, Any]]  # Track conversation with LLM for analysis

# Initialize our LLM with Langfuse callback
model = ChatOpenAI(
    temperature=0,
    callbacks=[langfuse_handler]  # Add Langfuse handler to the model
)

def read_email(state: EmailState):
    """Alfred reads and logs the incoming email"""
    email = state["email"]
    print(f"Alfred is processing an email from {email['sender']} with subject: {email['subject']}")
    return {}

def classify_email(state: EmailState):
    """Alfred uses an LLM to determine if the email is spam or legitimate"""
    email = state["email"]
    
    prompt = f"""
    As Alfred the butler, analyze this email and determine if it is spam or legitimate.
    
    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}
    
    First, determine if this email is spam. If it is spam, explain why.
    If it is legitimate, categorize it (inquiry, complaint, thank you, etc.).
    """
    
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages, config={"callbacks": [langfuse_handler]})
    
    response_text = response.content.lower()
    is_spam = "spam" in response_text and "not spam" not in response_text
    
    spam_reason = None
    if is_spam and "reason:" in response_text:
        spam_reason = response_text.split("reason:")[1].strip()
    
    email_category = None
    if not is_spam:
        categories = ["inquiry", "complaint", "thank you", "request", "information"]
        for category in categories:
            if category in response_text:
                email_category = category
                break
    
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content}
    ]
    
    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "email_category": email_category,
        "messages": new_messages
    }

def handle_spam(state: EmailState):
    """Alfred discards spam email with a note"""
    print(f"Alfred has marked the email as spam. Reason: {state['spam_reason']}")
    print("The email has been moved to the spam folder.")
    return {}

def draft_response(state: EmailState):
    """Alfred drafts a preliminary response for legitimate emails"""
    email = state["email"]
    category = state["email_category"] or "general"
    
    prompt = f"""
    As Alfred the butler, draft a polite preliminary response to this email.
    
    Email:
    From: {email['sender']}
    Subject: {email['subject']}
    Body: {email['body']}
    
    This email has been categorized as: {category}
    
    Draft a brief, professional response that Mr. Hugg can review and personalize before sending.
    """
    
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages, config={"callbacks": [langfuse_handler]})
    
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content}
    ]
    
    return {
        "draft_response": response.content,
        "messages": new_messages
    }

def notify_mr_hugg(state: EmailState):
    """Alfred notifies Mr. Hugg about the email and presents the draft response"""
    email = state["email"]
    print("\n" + "="*50)
    print(f"Sir, you've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print(f"Category: {state['email_category']}")
    print("\nI've prepared a draft response for your review:")
    print("-"*50)
    print(state["draft_response"])
    print("="*50 + "\n")
    return {}

def route_email(state: EmailState) -> str:
    """Determine the next step based on spam classification"""
    if state["is_spam"]:
        return "spam"
    else:
        return "legitimate"

# Create the graph
workflow = StateGraph(EmailState)

# Add nodes with unique names
workflow.add_node("read_email", read_email)
workflow.add_node("classify_email", classify_email)
workflow.add_node("handle_spam", handle_spam)
workflow.add_node("create_response", draft_response)
workflow.add_node("notify_user", notify_mr_hugg)

# Set up edges
workflow.add_edge(START, "read_email")
workflow.add_edge("read_email", "classify_email")
workflow.add_conditional_edges(
    "classify_email",
    route_email,
    {
        "spam": "handle_spam",
        "legitimate": "create_response"
    }
)
workflow.add_edge("handle_spam", END)
workflow.add_edge("create_response", "notify_user")
workflow.add_edge("notify_user", END)

# Compile the graph
app = workflow.compile()

# Example emails
legitimate_email = {
    "sender": "john.smith@example.com",
    "subject": "Question about your services",
    "body": "Dear Mr. Hugg, I was referred to you by a colleague..."
}

spam_email = {
    "sender": "winner@lottery-intl.com",
    "subject": "YOU HAVE WON $5,000,000!!!",
    "body": "CONGRATULATIONS! You have been selected..."
}

# Process emails with Langfuse tracing
print("\nProcessing legitimate email...")
legitimate_result = app.invoke(
    {"email": legitimate_email, "is_spam": None, "spam_reason": None, 
     "email_category": None, "draft_response": None, "messages": []},
    config={"callbacks": [langfuse_handler]}
)

print("\nProcessing spam email...")
spam_result = app.invoke(
    {"email": spam_email, "is_spam": None, "spam_reason": None, 
     "email_category": None, "draft_response": None, "messages": []},
    config={"callbacks": [langfuse_handler]}
)

mermaid_code = app.get_graph().draw_mermaid()
print(mermaid_code)