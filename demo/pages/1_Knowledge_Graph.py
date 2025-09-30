import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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

def tab_introduction():
    st.header("Định nghĩa")
    st.write("""
    Đồ thị tri thức, tiền thân là mạng ngữ nghĩa là cấu trúc dữ liệu đồ thị được phát triển nhằm hỗ trợ suy luận (reasoning) cho các thuật toán trí tuệ nhân tạo.
    """)
    st.write("""
    Theo định nghĩa của Resource Description Framework (RDF), đồ thị tri thức là một tập hợp các bộ ba (triple) có dạng (chủ thể, quan hệ, đối tượng) hay (subject, predicate, object).
    Mỗi bộ ba này biểu diễn một mối quan hệ giữa hai thực thể (entities) trong đồ thị. Chẳng hạn, bộ ba (Hút Thuốc, dẫn đến, Ung Thư Phổi) biểu diễn mối quan hệ "dẫn đến" giữa thực thể "Hút Thuốc" và thực thể "Ung Thư Phổi".
    """)
    example_1()
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

def tab_ontology():
    st.header("Bản thể học")
    st.write("""
    Bản thể học (Ontology) trong ngữ cảnh của đồ thị tri thức đề cập đến một tập hợp các khái niệm và mối quan hệ giữa chúng trong một lĩnh vực cụ thể.
    Nó cung cấp một khung cấu trúc để tổ chức và phân loại thông tin, giúp định nghĩa rõ ràng các thực thể và cách chúng tương tác với nhau.
    """)

def tab_incompleteness():
    st.header("Tính không đầy đủ")
    st.write("""
    Tính không đầy đủ của đồ thị tri thức đề cập đến thực tế rằng không phải tất cả các mối quan hệ và thực thể trong thế giới thực đều được biểu diễn trong đồ thị.
    Điều này có thể do nhiều nguyên nhân, bao gồm hạn chế trong việc thu thập dữ liệu, sai sót trong quá trình trích xuất thông tin, hoặc sự phức tạp vốn có của các mối quan hệ ngữ nghĩa.
    """)
    st.write("""
    Ví dụ, trong một đồ thị tri thức về y học, có thể thiếu các mối quan hệ quan trọng giữa các triệu chứng và bệnh tật do dữ liệu không đầy đủ hoặc lỗi trong quá trình trích xuất thông tin từ văn bản y khoa.
    Tính không đầy đủ này có thể ảnh hưởng đến hiệu quả của các ứng dụng dựa trên đồ thị tri thức, như hệ thống gợi ý hoặc trợ lý ảo, khi chúng không thể truy xuất thông tin cần thiết để đưa ra quyết định chính xác.
    """)

st.title("Đồ thị tri thức")
tab = st.tabs(["Định nghĩa", "Bản thể học", "Vấn đề"])

with tab[0]:
    tab_introduction()
with tab[1]:
    tab_ontology()
with tab[2]:
    tab_incompleteness()