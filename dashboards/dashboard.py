import streamlit as st
import yaml
import os

# Set up the page once
st.set_page_config(page_title="TruthScout Nexus", layout="wide")

# Define base paths
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

# Sidebar navigation
view = st.sidebar.radio(
    "Select View",
    [
        "🧩 Actor Intelligence",
        "📖 Gaza Case Study",
        "📂 Structured Data",
        "🎯 Investigative Spotlight"
    ]
)

# ----------------------------
# View 1: Actor Intelligence
# ----------------------------
if view == "🧩 Actor Intelligence":
    st.title("🌍 TruthScout Nexus: Actor Intelligence")

    actors = load_yaml(os.path.join(data_dir, "actors.yml"))
    types = list(set(actor["type"] for actor in actors if "type" in actor))
    selected_types = st.multiselect("Filter by Type", types, default=types)
    filtered_actors = [a for a in actors if a["type"] in selected_types]

    for actor in filtered_actors:
        with st.expander(actor["name"]):
            st.markdown(f"**Type:** {actor['type']}")
            if "role" in actor:
                st.markdown(f"**Roles:** {', '.join(actor['role'])}")
            if "region" in actor:
                st.markdown(f"**Region:** {actor['region']}")
            if "description" in actor:
                st.markdown(f"**Description:** {actor['description']}")
            if "linked_operations" in actor:
                st.markdown("**Linked Operations:**")
                for op in actor["linked_operations"]:
                    st.markdown(f"- {op}")
            if "verified_sources" in actor:
                st.markdown("**Evidence Links:**")
                for src in actor["verified_sources"]:
                    st.markdown(f"- [{src}]({src})")

# ----------------------------
# View 2: Gaza Markdown
# ----------------------------
elif view == "📖 Gaza Case Study":
    st.title("📖 Gaza: A Case Study in Western-Enabled Instability")
    markdown_path = os.path.join(docs_dir, 'gaza-case-study.md')
    st.markdown(load_markdown(markdown_path), unsafe_allow_html=True)

# ----------------------------
# View 3: Structured YAML Data
# ----------------------------
elif view == "📂 Structured Data":
    st.title("📂 Western Hegemony Dossier: Structured Data")
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
                    if key in ["references", "examples", "verified_sources"]:
                        st.markdown(f"**{key.replace('_', ' ').capitalize()}:**")
                        for ref in value:
                            st.markdown(f"- [{ref}]({ref})")
                    elif isinstance(value, list):
                        st.markdown(f"**{key.replace('_', ' ').capitalize()}:** {', '.join(value)}")
                    elif key != "name":
                        st.markdown(f"**{key.replace('_', ' ').capitalize()}:** {value}")
        st.markdown("---")
# ----------------------------
# View 4: Interactive Actor View
# ----------------------------
elif view == "🎯 Investigative Spotlight":
    st.title("🎯 Investigative Spotlight: BlackRock and Gaza 2014")

    actors = load_yaml(os.path.join(data_dir, "actors.yml"))
    blackrock = next((a for a in actors if a["id"] == "blackrock"), None)

    if blackrock:
        st.header(f"🔍 {blackrock['name']}")
        st.markdown(f"**Type:** {blackrock['type']}")
        st.markdown(f"**Region:** {blackrock['region']}")
        st.markdown(f"**Roles:** {', '.join(blackrock['role'])}")
        st.markdown(f"**Description:** {blackrock['description']}")

        # Profit Events
        if "profit_events" in blackrock:
            st.subheader("💰 Profit Events")
            for p in blackrock["profit_events"]:
                st.markdown(f"**Operation:** {p['operation']}")
                st.markdown(f"- Sector: {p['sector']}")
                st.markdown(f"- Estimated Profit: ${p['estimated_profit_usd']:,} USD")
                st.markdown(f"- Notes: {p['notes']}")
                st.markdown("**Evidence:**")
                for link in p["evidence_links"]:
                    st.markdown(f"- [{link}]({link})")

        # Media Ownership
        if "owned_media" in blackrock:
            st.subheader("📰 Media Influence")
            st.markdown(", ".join(blackrock["owned_media"]))

        # Execs
        if "key_executives" in blackrock:
            st.subheader("🧑‍💼 Key Executives")
            for exec in blackrock["key_executives"]:
                st.markdown(f"**{exec['name']}** — {exec['role']}")
                for role in exec.get("other_roles", []):
                    st.markdown(f"- {role}")
                for src in exec.get("verified_sources", []):
                    st.markdown(f"[Source]({src})")