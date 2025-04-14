import streamlit as st
import yaml
import os

# Setup
st.set_page_config(page_title="Western Hegemony Dossier", layout="wide")
st.title("🧩 Western Hegemony Dossier")

# Paths
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, '..', 'data')
docs_dir = os.path.join(base_dir, '..', 'docs')

# Load YAML
def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# Load Markdown
def load_markdown(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

# Sidebar Navigation
view = st.sidebar.radio(
    "Select View",
    ["📖 Gaza Case Study", "📂 Structured Data"]
)

if view == "📖 Gaza Case Study":
    st.subheader("📖 Gaza: A Case Study in Western-Enabled Instability")
    markdown_path = os.path.join(docs_dir, 'gaza-case-study.md')
    st.markdown(load_markdown(markdown_path), unsafe_allow_html=True)

elif view == "📂 Structured Data":
    files = {
        "Key Actors": "actors.yml",
        "Operations": "operations.yml",
        "Financial Influence": "finances.yml",
        "Media & Narrative Control": "narratives.yml",
        "Military & Arms Flow": "military.yml"
    }

    for section_title, filename in files.items():
        st.subheader(f"📌 {section_title}")
        entries = load_yaml(os.path.join(data_dir, filename))

        for entry in entries:
            with st.expander(entry.get("name", "Unnamed Entry")):
                for key, value in entry.items():
                    if key == "references" or key == "examples":
                        st.markdown(f"**{key.capitalize()}:**")
                        for ref in value:
                            st.markdown(f"- [{ref}]({ref})")
                    elif isinstance(value, list):
                        st.markdown(f"**{key.capitalize()}:** {', '.join(value)}")
                    elif key != "name":
                        st.markdown(f"**{key.capitalize()}:** {value}")
        st.markdown("---")
