import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- DuckDuckGo search function ---
def duckduckgo_search(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for result in soup.select(".result__title a"):
            title = result.text.strip()
            link = result.get("href")
            if title and link:
                results.append({"title": title, "url": link})
        return results

    except Exception as e:
        st.error(f"Search failed: {e}")
        return []

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="DuckDuckGo Search", page_icon="🔍")
    st.title("🔍 DuckDuckGo Web Search (No API Key Required)")

    query = st.text_input("Enter your search query:")
    search_button = st.button("Search")

    if search_button and query:
        with st.spinner("Searching..."):
            results = duckduckgo_search(query)

        if results:
            st.success(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                st.markdown(f"**{i}. [{result['title']}]({result['url']})**")
        else:
            st.warning("No results found.")

if __name__ == "__main__":
    main()
