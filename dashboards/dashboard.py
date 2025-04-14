import streamlit as st
import yaml
import pandas as pd
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
        "🎯 Investigative Spotlight",
        "📡 Truth Network"
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
# ----------------------------
# View 5: Truth Network
# ----------------------------
elif view == "📡 Truth Network":
    import urllib.parse

    st.title("📡 Truth Network: Interest-Based Filter Explorer")

    # Load updated CSV
    truth_network_path = os.path.join(data_dir, "truth-network.csv")
    df = pd.read_csv(truth_network_path)

    # 🔍 Text Search
    search_query = st.text_input("Search by name, tag, or relation", "").strip().lower()

    # Filter controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_region = st.selectbox("🌍 Region", sorted(df["entity_1_region"].dropna().unique()), index=0)
    with col2:
        selected_conflict = st.selectbox("💣 Conflict", sorted(df["conflict"].dropna().unique()), index=0)
    with col3:
        selected_type = st.selectbox("🏷️ Entity Type", sorted(df["entity_1_type"].dropna().unique()), index=0)
    with col4:
        selected_impact = st.selectbox("⚖️ Impact Area", sorted(df["impact_area"].dropna().unique()), index=0)

    # Apply dropdown filters
    filtered_df = df[
        (df["entity_1_region"] == selected_region) &
        (df["conflict"] == selected_conflict) &
        (df["entity_1_type"] == selected_type) &
        (df["impact_area"] == selected_impact)
    ]

    # Apply search filter
    if search_query:
        filtered_df = filtered_df[
            df["entity_1_name"].str.lower().str.contains(search_query) |
            df["entity_2_name"].str.lower().str.contains(search_query) |
            df["tags"].fillna("").str.lower().str.contains(search_query) |
            df["relationship_type"].str.lower().str.contains(search_query)
        ]

    filtered_df = filtered_df.sort_values(by="relevance_score", ascending=False)

    # Display result count
    st.subheader(f"🔗 {len(filtered_df)} Relevant Connections")

    # Render filtered results
    for _, row in filtered_df.iterrows():
        st.markdown(f"**{row['entity_1_name']}** *{row['relationship_type']}* **{row['entity_2_name']}**")
        st.markdown(f"• Conflict: `{row['conflict']}` | Region: `{row['entity_1_region']}`")
        st.markdown(f"• Category: `{row['category']}` | Impact: `{row['impact_area']}`")
        if pd.notna(row['tags']):
            st.markdown(f"• Tags: _{row['tags']}_")
        if pd.notna(row['source']):
            st.markdown(f"• [Source]({row['source']})")
        st.markdown("---")

    # 🔗 URL Sharing
    st.markdown("### 📤 Share This View")
    params = {
        "region": selected_region,
        "conflict": selected_conflict,
        "type": selected_type,
        "impact": selected_impact,
        "search": search_query
    }
    query_string = urllib.parse.urlencode(params)
    base_url = "https://truthscore-nexus.streamlit.app"
    shareable_link = f"{base_url}/?{query_string}"

    if st.button("🔗 Copy Sharable Filter Link"):
        st.code(shareable_link, language="markdown")
        st.success("Link generated! You can use this as a citation in an article.")