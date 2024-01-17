import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import sys


def scrape_links(parent_url, url, depth, max_links, links_graph):
    if depth == 0 or max_links <= 0:
        return max_links

    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return max_links
        html_content = response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return max_links

    soup = BeautifulSoup(html_content, 'html.parser')
    links = {link.get('href') for link in soup.find_all('a', href=True)}

    for link in links:
        if max_links <= 0:
            break
        if not link.startswith('http'):
            continue
        links_graph.add_edge(parent_url, link)
        max_links = scrape_links(url, link, depth-1, max_links-1, links_graph)

    return max_links



def create_network_map(start_url, depth=2, max_links=10):
    graph = nx.DiGraph()
    scrape_links(start_url, start_url, depth, max_links, graph)
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()



# Example usage
if len(sys.argv) > 1:
    start_url = sys.argv[1]
    create_network_map(start_url, depth=2, max_links=10)
else:
    print("Please provide a URL as an argument.")
