import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly

print("ok")


class DataLoader:
    def __init__(self):
        print("DataLoader Init")
        
    def fetch_biorxiv_papers(self,query):
        def search_biorxiv(query):
            url = f"https://www.biorxiv.org/search/=all:{query}&start=0&max_results=5"
            response = requests.get(url)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }
                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]
            return []
        
        if len(papers) < 5 and self.search_agent:  # If fewer than 5 papers, expand search
            related_topics_response = self.search_agent.generate_reply(
                messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
            )
            related_topics = related_topics_response.get("content", "").split("\n")

            for topic in related_topics:
                topic = topic.strip()
                if topic and len(papers) < 5:
                    new_papers = search_biorxiv(topic)
                    papers.extend(new_papers)
                    papers = papers[:5]  # Ensure max 5 papers

        return papers


    def fetch_google_scholar_papers(self,query):
        def search_google_scholar(query):
            papers = []
        search_results = scholarly.search_pubs(query)

        for i, paper in enumerate(search_results):
            if i >= 5:
                break
            papers.append({
                "title": paper["bib"]["title"],
                "summary": paper["bib"].get("abstract", "No summary available"),
                "link": paper.get("pub_url", "No link available")
            })
        return papers
