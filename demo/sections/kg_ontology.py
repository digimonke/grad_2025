import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

def render():
    st.header("Bản thể học")
    st.info("""
    **Bản thể học (Ontology)** trong ngữ cảnh đồ thị tri thức là đặc tả hình thức của các khái niệm (classes), thuộc tính/quan hệ (properties) và các ràng buộc (constraints) giữa chúng trong một miền tri thức. 
    Nó đóng vai trò là “lược đồ ngữ nghĩa” thống nhất, giúp con người và máy tính cùng hiểu, tích hợp và suy luận trên dữ liệu.
    """)

    st.subheader("Quá trình phát triển (tóm lược)")
    st.markdown(
        """
        - Giai đoạn tiền đề: từ mạng ngữ nghĩa và frame-based systems (thập niên 70–90) đến các mô hình tri thức sớm trong AI.
        - Chuẩn hoá trên Mạng Ngữ nghĩa (Semantic Web):
          - RDF/RDFS để mô tả dữ liệu dưới dạng bộ ba (subject–predicate–object) và phân cấp khái niệm/thuộc tính.
          - OWL (Web Ontology Language) để biểu đạt giàu ngữ nghĩa hơn (lớp, ràng buộc, tính kế thừa, suy luận logic mô tả).
          - SKOS cho từ vựng điều khiển (thesaurus) và SHACL để kiểm tra ràng buộc cấu trúc/chuẩn dữ liệu.
        - Một số bộ bản thể quy mô lớn: [DBpedia Ontology](https://akswnc7.informatik.uni-leipzig.de/dstreitmatter/archivo/dbpedia.org/ontology--DEV/2020.10.09-031000/ontology--DEV_type=generatedDocu.html), [schema.org](https://schema.org/), [FIBO](https://spec.edmcouncil.org/fibo/) (tài chính), SNOMED/GO (y sinh), v.v.
        """
    )

    st.subheader("RDF/RDFS và OWL")
    st.markdown(
        """
        - RDF (Resource Description Framework): mô hình dữ liệu dựa trên bộ ba (subject–predicate–object) với định danh bằng IRI; hỗ trợ literal và blank node; phổ biến trong biểu diễn liên kết dữ liệu và truy vấn bằng SPARQL (SELECT, CONSTRUCT…).
        - RDFS (RDF Schema): mở rộng RDF với siêu dữ liệu về lớp/thuộc tính và phân cấp ngữ nghĩa: rdfs:Class, rdfs:subClassOf, rdfs:subPropertyOf, rdfs:domain, rdfs:range, rdfs:label, rdfs:comment… giúp suy luận cơ bản thông qua các lớp kế thừa.
        - OWL (Web Ontology Language): mở rộng RDFS bằng logic mô tả (Description Logic) để biểu đạt ràng buộc phong phú: tương đương lớp (owl:equivalentClass), loại trừ (owl:disjointWith), tổ hợp lớp (intersection/union/complement), ràng buộc thuộc tính (some/allValuesFrom, hasValue, cardinality/min/max), nghịch đảo (owl:inverseOf), bắc cầu (owl:TransitiveProperty), đơn trị (owl:FunctionalProperty), đối xứng (owl:SymmetricProperty)… Hỗ trợ suy luận/kiểm tra nhất quán bằng reasoner (HermiT, Pellet, ELK).
        """
    )

    # Giới thiệu ngắn về Turtle và trực quan hoá ví dụ
    st.subheader("Ví dụ: Turtle và trực quan hoá")
    st.markdown(
        """
        Turtle (Terse RDF Triple Language) là cú pháp ngắn gọn, dễ đọc để biểu diễn đồ thị RDF. 
        Một số điểm chính:
        - Dùng @prefix để rút gọn IRI, mỗi bộ ba kết thúc bằng dấu chấm.
        - Dấu chấm phẩy (;) tái sử dụng chủ ngữ, dấu phẩy (,) tái sử dụng vị ngữ.
        - Hỗ trợ đa ngôn ngữ và kiểu dữ liệu như nút rỗng và tập hợp.
        """
    )
    st.code(
        """
        @prefix ex: <http://example.org/> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dbo: <http://dbpedia.org/ontology/> .

        ex:Country a rdfs:Class .
        ex:City a rdfs:Class .
        dbo:capital rdfs:domain ex:Country ; rdfs:range ex:City .

        ex:Vietnam a ex:Country .
        ex:Hanoi a ex:City .
        ex:Vietnam dbo:capital ex:Hanoi .
        """,
        language="turtle",
    )

    # Trực quan hoá tương tác bằng PyVis: lược đồ (domain/range) + dữ liệu thể hiện
    net = Network(height="520px", width="100%", directed=True, cdn_resources="in_line")
    net.set_options('''
    {"nodes": {"shape": "dot", "size": 18},
     "edges": {"arrows": {"to": {"enabled": true}}, "smooth": {"type": "dynamic"}},
     "physics": {"barnesHut": {"gravitationalConstant": -2000, "springLength": 150}}}
    ''')

    # Nodes: classes (yellow) and individuals (blue)
    net.add_node("ex:Country", label="ex:Country", color="#ffcc00", title="http://example.org/Country")
    net.add_node("ex:City", label="ex:City", color="#ffcc00", title="http://example.org/City")
    net.add_node("ex:Vietnam", label="ex:Vietnam", color="#87cefa", title="http://example.org/Vietnam")
    net.add_node("ex:Hanoi", label="ex:Hanoi", color="#87cefa", title="http://example.org/Hanoi")

    # Edges
    net.add_edge("ex:Country", "ex:City", label="dbo:capital (domain→range)", color="#888888", dashes=True)
    net.add_edge("ex:Vietnam", "ex:Country", label="a (type)", color="#2ecc71")
    net.add_edge("ex:Hanoi", "ex:City", label="a (type)", color="#2ecc71")
    net.add_edge("ex:Vietnam", "ex:Hanoi", label="dbo:capital", color="#f39c12")

    html = net.generate_html()
    components.html(html, height=560, scrolling=True)
    st.caption("Đồ thị minh hoạ (PyVis): Lược đồ (domain→range) và dữ liệu thể hiện (type, capital)")

    