from string import Template

#### RAG PROMPTS FOR LEGAL QUERIES ####

#### System ####

system_prompt = Template("\n".join([
    "You are a legal assistant designed to help interpret and summarize legal information for the user.",
    "You will be provided with a set of documents relevant to the user's legal query.",
    "Use only the information from the provided documents to formulate your response.",
    "If the documents do not contain sufficient information to respond accurately, you may inform the user accordingly.",
    "Do not speculate or provide legal advice beyond the information given.",
    "Respond in the same language as the user's query.",
    "Maintain a professional, respectful, and neutral tone.",
    "Be concise, accurate, and legally precise in your response. Avoid assumptions and generalizations.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Legal Content: $chunk_text",
    ])
)

#### Footer ####
footer_prompt = Template("\n".join([
    "Based strictly on the above legal documents, please provide a response to the user's question.",
    "## Legal Question:",
    "$query",
    "",
    "## Response:",
]))
