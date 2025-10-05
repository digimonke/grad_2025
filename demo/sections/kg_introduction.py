import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import requests
from pyvis.network import Network
import streamlit.components.v1 as components

DBPEDIA_SPARQL_ENDPOINT = "https://dbpedia.org/sparql"

def run_sparql(query: str):
    headers = {"Accept": "application/sparql-results+json"}
    params = {
        "query": query,
        "format": "application/sparql-results+json",
    }
    resp = requests.get(DBPEDIA_SPARQL_ENDPOINT, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()

def _escape_sparql_string_literal(value: str) -> str:
    # Escape backslashes and quotes for SPARQL string literal within double quotes
    return value.replace("\\", "\\\\").replace('"', '\\"')

@st.cache_data(show_spinner=False, ttl=600)
def resolve_dbpedia_resource(label: str):
    # Try Vietnamese label first, then English as fallback
    for lang_label in [(label, "vi"), (label, "en")]:
        text, lang = lang_label
        text = _escape_sparql_string_literal(text)
        q = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?s WHERE {{
          ?s rdfs:label "{text}"@{lang} .
          FILTER(STRSTARTS(STR(?s), "http://dbpedia.org/resource/"))
        }} LIMIT 1
        """
        data = run_sparql(q)
        bindings = data.get("results", {}).get("bindings", [])
        if bindings:
            return bindings[0]["s"]["value"]
    return None

@st.cache_data(show_spinner=False, ttl=600)
def fetch_neighbors_with_ratio(resource_uri: str, outgoing_limit: int = 1, incoming_limit: int = 2):
        q = f"""
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        # Outgoing sample
        SELECT DISTINCT ?neighbor ?p ?dir WHERE {{
            {{
                SELECT DISTINCT ?neighbor ?p ?dir WHERE {{
                    <{resource_uri}> ?p ?neighbor .
                    FILTER(isIRI(?neighbor))
                    FILTER(STRSTARTS(STR(?neighbor), "http://dbpedia.org/resource/"))
                    FILTER(STRSTARTS(STR(?p), "http://dbpedia.org/ontology/"))
                    FILTER(!STRSTARTS(STR(?p), "http://dbpedia.org/ontology/wikiPage"))
                    ?p a owl:ObjectProperty .
                    BIND("out" AS ?dir)
                }} ORDER BY RAND() LIMIT {outgoing_limit}
            }}
            UNION
            # Incoming sample
            {{
                SELECT DISTINCT ?neighbor ?p ?dir WHERE {{
                    ?neighbor ?p <{resource_uri}> .
                    FILTER(isIRI(?neighbor))
                    FILTER(STRSTARTS(STR(?neighbor), "http://dbpedia.org/resource/"))
                    FILTER(STRSTARTS(STR(?p), "http://dbpedia.org/ontology/"))
                    FILTER(!STRSTARTS(STR(?p), "http://dbpedia.org/ontology/wikiPage"))
                    ?p a owl:ObjectProperty .
                    BIND("in" AS ?dir)
                }} ORDER BY RAND() LIMIT {incoming_limit}
            }}
        }}
        """
        data = run_sparql(q)
        results = []
        for b in data.get("results", {}).get("bindings", []):
                results.append({
                        "neighbor": b["neighbor"]["value"],
                        "predicate": b["p"]["value"],
                        "dir": b["dir"]["value"],
                })
        return results

@st.cache_data(show_spinner=False, ttl=600)
def fetch_labels(uris):
    if not uris:
        return {}
    values = " ".join(f"<{u}>" for u in uris)
    q = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?s (COALESCE(?lvi, ?len) AS ?label) WHERE {{
      VALUES ?s {{ {values} }}
      OPTIONAL {{ ?s rdfs:label ?lvi . FILTER(LANG(?lvi) = "vi") }}
      OPTIONAL {{ ?s rdfs:label ?len . FILTER(LANG(?len) = "en") }}
    }}
    """
    data = run_sparql(q)
    out = {}
    for b in data.get("results", {}).get("bindings", []):
        s = b["s"]["value"]
        lbl = b.get("label", {}).get("value")
        out[s] = lbl if lbl else s.split("/")[-1].replace("_", " ")
    return out

def draw_dbpedia_graph_interactive(center_label: str, limit: int = 3):
    try:
        resource = resolve_dbpedia_resource(center_label)
        if not resource:
            st.error(f"Không tìm thấy thực thể DBpedia cho nhãn: {center_label}")
            return
        # Fetch exactly 1 outgoing and 2 incoming neighbors (if available)
        neighbors = fetch_neighbors_with_ratio(resource, outgoing_limit=1, incoming_limit=2)
        if not neighbors:
            st.warning("Không tìm thấy quan hệ ontology (dbo:ObjectProperty) kề với thực thể này.")
        neighbor_uris = [n["neighbor"] for n in neighbors]
        predicate_uris = [n["predicate"] for n in neighbors]
        labels_map = fetch_labels([resource] + neighbor_uris + predicate_uris)

        # Build interactive network
        net = Network(height="600px", width="100%", directed=True, notebook=False, cdn_resources="in_line")
        # nicer physics/layout
        net.set_options('''
        {
          "physics": {"barnesHut": {"gravitationalConstant": -2000, "springLength": 150}},
          "nodes": {"shape": "dot", "size": 18},
          "edges": {"arrows": {"to": {"enabled": true}}, "smooth": {"type": "dynamic"}}
        }
        ''')

        center_text = labels_map.get(resource, center_label)
        net.add_node(resource, label=center_text, title=resource, color="#ffcc00")
        added_nodes = {resource}

        for n in neighbors:
            n_uri = n["neighbor"]
            p_uri = n["predicate"]
            n_text = labels_map.get(n_uri, n_uri.split("/")[-1].replace("_", " "))
            p_text = labels_map.get(p_uri, p_uri.split("/")[-1].replace("_", " "))
            if n_uri not in added_nodes:
                net.add_node(n_uri, label=n_text, title=n_uri, color="#87cefa")
                added_nodes.add(n_uri)
            if n["dir"] == "out":
                net.add_edge(resource, n_uri, label=p_text, title=p_uri)
            else:
                net.add_edge(n_uri, resource, label=p_text, title=p_uri)

        st.caption(f"DBpedia resource: {resource}")
        html = net.generate_html()
        # Inject click handler to open node/edge URIs in a new tab
        click_js = """
        network.on("click", function(params) {
          try {
            if (params.nodes && params.nodes.length > 0) {
              var nodeId = params.nodes[0];
              var node = nodes.get(nodeId);
              var url = (node && (node.title || node.id)) || null;
              if (url && url.startsWith('http')) { window.open(url, '_blank'); }
            } else if (params.edges && params.edges.length > 0) {
              var edgeId = params.edges[0];
              var edge = edges.get(edgeId);
              var url = (edge && edge.title) || null;
              if (url && url.startsWith('http')) { window.open(url, '_blank'); }
            }
          } catch (e) { console.error(e); }
        });
        """
        anchor = "new vis.Network(container, data, options);"
        idx = html.find(anchor)
        if idx != -1:
            insert_pos = idx + len(anchor)
            html = html[:insert_pos] + "\n" + click_js + "\n" + html[insert_pos:]
        components.html(html, height=650, scrolling=True)
    except requests.RequestException as e:
        st.error(f"Lỗi khi truy vấn DBpedia: {e}")
    except Exception as e:
        st.error(f"Đã xảy ra lỗi: {e}")

def example_1():
    G = nx.DiGraph()
    G.add_edge("Hút thuốc", "Ung thư phổi", label="dẫn đến")
    G.add_edge("Di truyền", "Ung thư phổi", label="dẫn đến")
    G.add_edge("Stress", "Hút thuốc", label="tương quan")

    pos = nx.spring_layout(G)
    plt.figure(figsize=(4,2))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, font_size=6, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.axis('off')

    st.pyplot(plt)

def render():
    st.write("""
    Đồ thị tri thức, tiền thân là mạng ngữ nghĩa là cấu trúc dữ liệu đồ thị được phát triển nhằm hỗ trợ suy luận (reasoning) cho các thuật toán trí tuệ nhân tạo.
    """)
    st.info("""
    Đồ thị tri thức được xây dựng dựa trên **Resource Description Framework (RDF)**, là một tập hợp các bộ ba (triple) có dạng **(chủ thể, quan hệ, đối tượng)** hay **(subject, predicate, object)**.
    Mỗi bộ ba này biểu diễn một mối quan hệ giữa hai thực thể (entities) trong đồ thị. Chẳng hạn, bộ ba (Việt Nam, thủ đô, Hà Nội) biểu diễn mối quan hệ "thủ đô" giữa thực thể "Việt Nam" và thực thể "Hà Nội".
    """)

    st.write("""
    Hiện nay, đồ thị tri thức được sử dụng rộng rãi trong nhiều lĩnh vực như tìm kiếm thông tin (information retrieval), hệ thống gợi ý (recommendation systems), và trợ lý ảo (virtual assistants) để cung cấp ngữ cảnh và hiểu biết sâu sắc hơn về dữ liệu.
    Ví dụ có thể kể đến như:
    - [Google Knowledge Graph](https://blog.google/products/search/introducing-knowledge-graph-things-not/): Được sử dụng để cải thiện kết quả tìm kiếm bằng cách cung cấp thông tin ngữ cảnh về các thực thể như người, địa điểm, sự kiện.
    - [Facebook Graph](https://www.facebook.com/notes/facebook-engineering/the-facebook-graph/10150906780248920/): Mô hình hóa mối quan hệ giữa người dùng, bài viết, và các tương tác khác trên nền tảng mạng xã hội.
    - [LLM + Knowledge Graphs](https://ieeexplore.ieee.org/abstract/document/10387715/): Nghiên cứu tích hợp đồ thị tri thức với mô hình ngôn ngữ lớn để tăng khả năng suy luận và độ chính xác thông tin.
    - [IBM Watson Discovery](https://www.aaai.org/ojs/index.php/aimagazine/article/view/2303): Sử dụng đồ thị tri thức để tìm kiếm và suy luận trên dữ liệu doanh nghiệp.
    """)
    st.write("""
    Một số đồ thị tri thức mã nguồn mở được cộng đồng nghiên cứu xây dựng cho các lĩnh vực khác nhau như:
    - [DBpedia](https://wiki.dbpedia.org/): Trích xuất dữ liệu có cấu trúc từ Wikipedia, cung cấp một đồ thị tri thức phong phú về các thực thể và mối quan hệ của chúng.
    - [YAGO](https://yago-knowledge.org/): Đồ thị tri thức kết hợp thông tin từ Wikipedia, WordNet, và GeoNames, nổi bật với độ chính xác cao và phạm vi rộng lớn.
    - [WordNet](https://wordnet.princeton.edu/): Mặc dù không hoàn toàn là một đồ thị tri thức, WordNet là một cơ sở dữ liệu từ vựng lớn của tiếng Anh, tổ chức các từ thành các nhóm đồng nghĩa (synsets) và biểu diễn các mối quan hệ ngữ nghĩa giữa chúng.
    """)

    st.divider()
    
    st.subheader("Ví dụ")
    col1, col2 = st.columns([3, 1])
    with col1:
        label = st.text_input("Nhãn thực thể", value="Việt Nam")
    with col2:
        st.write("")
        st.write("")
        run = st.button("Truy vấn DBpedia")

    if run:
        draw_dbpedia_graph_interactive(label, limit=3)