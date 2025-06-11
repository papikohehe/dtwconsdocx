import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
]

def search_google(query, user_agent):
    headers = {"User-Agent": user_agent}
    url = f"https://www.google.com/search?q={query}&hl=en"

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            title = g.find('h3')
            link = g.find('a', href=True)
            if title and link:
                results.append({
                    "title": title.text,
                    "url": link['href']
                })
        return results

    except Exception as e:
        st.warning(f"Search failed: {e}")
        return []

def main():
    st.title("🔍 Simple Google Search (No Proxy)")

    query = st.text_input("Enter your search query:")
    run = st.button("Search")

    if run and query:
        st.write(f"Searching Google for: **{query}**")
        with st.spinner("Fetching results..."):
            user_agent = random.choice(USER_AGENTS)
            results = search_google(query, user_agent)
            time.sleep(random.uniform(2.0, 4.0))  # avoid getting blocked

        if results:
            st.success(f"Found {len(results)} results")
            for i, result in enumerate(results, 1):
                st.markdown(f"**{i}. [{result['title']}]({result['url']})**")
        else:
            st.warning("No results found or blocked by Google.")

if __name__ == "__main__":
    main()
