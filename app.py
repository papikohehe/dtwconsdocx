import streamlit as st
import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    }
    data = {"q": query}

    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        results = []
        for a in soup.select(".result__a"):
            title = a.text.strip()
            href = a["href"]
            results.append({"title": title, "url": href})
        return results

    except Exception as e:
        st.error(f"Search failed: {e}")
        return []

def main():
    st.set_page_config(page_title="DuckDuckGo Search", page_icon="🔍")
    st.title("🔍 DuckDuckGo Search (No API Key Required)")

    query = st.text_input("Enter a search query:")
    search_button = st.button("Search")

    if search_button and query:
        with st.spinner("Searching..."):
            results = duckduckgo_search(query)

        if results:
            st.success(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                st.markdown(f"**{i}. [{result['title']}]({result['url']})**")
        else:
            st.warning("No results found or request was blocked.")

if __name__ == "__main__":
    main()
