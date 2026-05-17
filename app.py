import streamlit as st
import requests
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

st.title("GitHub README Generator")

repo = st.text_input("Enter GitHub Repository URL")


def get_repo_data(repo_url):

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo_name = parts[-1]

    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()

    return None


def generate_readme(repo_data):

    prompt = f"""
    Generate a professional GitHub README.

    Project Name:
    {repo_data['name']}

    Description:
    {repo_data['description']}

    Language:
    {repo_data['language']}

    Include:
    - Project Overview
    - Features
    - Installation
    - Usage
    - Contribution
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

if st.button("Generate README"):

    with st.spinner("Generating README..."):

        repo_data = get_repo_data(repo)

        if repo_data:

            readme = generate_readme(repo_data)

            st.markdown(readme)

            st.download_button(
                label="Download README",
                data=readme,
                file_name="README.md",
                mime="text/markdown"
            )

        else:
            st.error("Invalid Repository URL")