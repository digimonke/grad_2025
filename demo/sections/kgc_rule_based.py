import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

def AMIE():
    st.markdown(
        """
        [AMIE: association rule mining under incomplete evidence in ontological knowledge bases](https://archives.iw3c2.org/www2013/proceedings/p413.pdf) 
        là một hệ thống khai thác quy tắc từ đồ thị tri thức để hoàn thiện các bộ ba bị thiếu. 
        AMIE khai thác (mining) các quy tắc dạng mệnh đề Horn để suy luận các mối quan hệ mới dựa trên các mẫu đã biết trong đồ thị.
        """
    )

    # atoms
    st.write("Thuật toán này bắt đầu với 1 nguyên tử (atom):")
    st.latex(r"""r(x, y)""")
    st.latex(r"""VD: capital(Viet Nam, Ha Noi)""")

    # rules
    st.write("Bộ quy tắc mà AMIE muốn khai thác được cấu thành từ một chuỗi nguyên tử và kết luận của nó cũng là một nguyên tử:")
    columns = st.columns(2)
    with columns[0]:
        st.latex(r"""B_1 \land B_2 \land ... \land B_n \rightarrow r(x, y)""")
    with columns[1]:
        st.latex(r"""B^{\rightarrow} \rightarrow r(x, y)""")

    # operators
    st.write("Nhằm thu hẹp không gian tìm kiếm, bắt đầu với 1 nguyên tử duy nhất, AMIE tuần tự áp dụng 1 trong các phép biến đổi (operators) sau để mở rộng quy tắc hiện tại:")
    st.markdown(
        """
        - **Add Dangling Atom (AD)**: thêm một nguyên tử mới với một biến mới và có chung biến còn lại với bộ quy tắc đang được khai thác.
        - **Add Closing Atom (AC)**: thêm một nguyên tử mới với hai biến của nó đã được sử dụng bởi bộ quy tắc đang được khai thác.
        - **Add Instantiated Atom (AI)**: thêm một nguyên tử mới với ít nhất 1 biến là thực thể thuộc đồ thị và có chung biến còn lại (thực thể hoặc lớp) với bộ quy tắc đang được khai thác.
        """
    )
    st.write("Trong quá trình xây dựng quy tắc, AMIE sẽ loại bỏ các quy tắc bị trùng lặp hoặc kém chất lượng dựa trên các tiêu chí như độ dài quy tắc, Head Coverage.")

    st.subheader("Minh hoạ trực quan")
    st.markdown(
        """
        Quy tắc ví dụ (mệnh đề Horn): nếu một người sống ở một thành phố và thành phố đó là thủ đô của một quốc gia, 
        thì người đó có quốc tịch của quốc gia ấy.

        Rule: livesIn(x, z) ∧ capitalOf(z, y) → citizenOf(x, y)

        Cách AMIE có thể tìm ra quy tắc (đơn giản hoá):
        - Bắt đầu với head: citizenOf(x, y)
        - AD: thêm livesIn(x, z) (thêm biến z chưa có, chia sẻ x)
        - AC: thêm capitalOf(z, y) (đóng biến z và y đang tồn tại)
        """
    )

    # --------- Cấu hình demo ---------
    c1, c2, c3 = st.columns(3)
    with c1:
        include_alice_truth = st.checkbox("Include (Alice, citizenOf, Vietnam)", value=False)
    with c2:
        show_steps = st.checkbox("Show rule steps (AD/AC)", value=True)
    with c3:
        show_tbox = st.checkbox("Show T-box (classes)", value=True, help="Thêm các lớp Person, Nation, City và cạnh kiểu (a)")

    # --- Toy KG with T-box ---
    persons = ["ex:Alice", "ex:Bob"]
    cities = ["ex:Hanoi", "ex:Tokyo"]
    nations = ["ex:Vietnam", "ex:Japan"]
    # T-box class nodes
    class_nodes = ["Person", "City", "Nation"]

    # A-box typing
    types = {**{p: "Person" for p in persons}, **{c: "City" for c in cities}, **{n: "Nation" for n in nations}}

    base_triples = [
        ("ex:Hanoi", "capitalOf", "ex:Vietnam"),
        ("ex:Tokyo", "capitalOf", "ex:Japan"),
        ("ex:Alice", "livesIn", "ex:Hanoi"),
        ("ex:Bob", "livesIn", "ex:Tokyo"),
        ("ex:Bob", "citizenOf", "ex:Japan"),  # ground truth head present for Bob
    ]
    triples = list(base_triples)
    if include_alice_truth:
        triples.append(("ex:Alice", "citizenOf", "ex:Vietnam"))

    # Type triples
    type_triples = [
        *[(p, "a", "Person") for p in persons],
        *[(c, "a", "City") for c in cities],
        *[(n, "a", "Nation") for n in nations],
    ]

    # --- Apply rule: livesIn(x,y) ∧ capitalOf(y,z) -> citizenOf(x,z) ---
    def body_matches(triples):
        by_pred = {}
        for s, p, o in triples:
            by_pred.setdefault(p, []).append((s, o))
        matches = []
        for x, y in by_pred.get("livesIn", []):
            for yy, z in by_pred.get("capitalOf", []):
                if yy == y:
                    matches.append((x, y, z))
        return matches

    body = body_matches(triples)
    predicted_heads = [(x, "citizenOf", z) for (x, y, z) in body]
    triple_set = set(triples)
    present_heads = [t for t in predicted_heads if t in triple_set]
    missing_heads = [t for t in predicted_heads if t not in triple_set]

    # --- Metrics ---
    support = len(present_heads)
    body_count = len(predicted_heads)
    head_total = sum(1 for (s, p, o) in triples if p == "citizenOf")
    confidence = support / body_count if body_count else 0.0
    head_coverage = support / head_total if head_total else 0.0

    # PCA-confidence denominator: only count body instantiations where the subject already has some head predicate
    def has_any_head_for_subject(x):
        return any(s == x and p == "citizenOf" for (s, p, o) in triples)

    denom_pca = sum(1 for (x, y, z) in body if has_any_head_for_subject(x))
    pca_conf = support / denom_pca if denom_pca else 0.0

    # Table of predictions
    df_preds = pd.DataFrame(
        [
            {
                "x": s,
                "y": o,
                "pred": f"({s}, citizenOf, {o})",
                "status": "present" if (s, "citizenOf", o) in triple_set else "predicted (missing)",
            }
            for (s, _, o) in predicted_heads
        ]
    )

    st.write("Các bộ ba suy luận được (và trạng thái hiện diện trong KG):")
    st.dataframe(df_preds, use_container_width=True)

    colm = st.columns(4)
    with colm[0]:
        st.metric("Support", support)
    with colm[1]:
        st.metric("Confidence", f"{confidence:.2f}")
    with colm[2]:
        st.metric("Head Coverage", f"{head_coverage:.2f}")
    with colm[3]:
        st.metric("PCA-Confidence", f"{pca_conf:.2f}")

    # --- Rule construction steps (variables view) ---
    if show_steps:
        st.markdown("#### Xây dựng quy tắc")
        step = st.select_slider("Bước", options=[0, 1, 2, 3], value=2, format_func=lambda i: [
            "0: Head (citizenOf)",
            "1: AD → livesIn(x,z)",
            "2: AC → capitalOf(z,y)",
            "3: Áp dụng vào KG",
        ][i])

        def draw_rule_step(k):
            net_r = Network(height="300px", width="100%", directed=True, cdn_resources="in_line")
            net_r.set_options('{"nodes":{"shape":"dot","size":16}, "edges":{"arrows":{"to":{"enabled":true}}}}')
            for v in ["x", "y", "z"]:
                net_r.add_node(v, label=v, color="#ffcc00")
            if k >= 0:
                net_r.add_edge("x", "y", label="citizenOf", color="#2ecc71")
            if k >= 1:
                net_r.add_edge("x", "z", label="livesIn", color="#3498db")
            if k >= 2:
                net_r.add_edge("z", "y", label="capitalOf", color="#9b59b6")
            return net_r.generate_html()

        html_rule = draw_rule_step(step)
        components.html(html_rule, height=320, scrolling=False)

    # --- Visualize KG with PyVis ---
    net = Network(height="560px", width="100%", directed=True, cdn_resources="in_line")
    net.set_options('''
    {"nodes": {"shape": "dot", "size": 18},
     "edges": {"arrows": {"to": {"enabled": true}}, "smooth": {"type": "dynamic"}},
     "physics": {"barnesHut": {"gravitationalConstant": -2000, "springLength": 150}}}
    ''')

    # Add class nodes (T-box)
    if show_tbox:
        for cls in class_nodes:
            net.add_node(cls, label=cls, color="#ffcc00", title=f"Class: {cls}")

    def add_node(node):
        t = types.get(node)
        if t:
            # Instances are blue
            color = "#87cefa"
        else:
            color = "#cccccc"
        net.add_node(node, label=node, color=color, title=node)

    # Add A-box relation edges
    for s, p, o in triples:
        add_node(s)
        add_node(o)
        color = {"livesIn": "#3498db", "capitalOf": "#9b59b6", "citizenOf": "#2ecc71"}.get(p, "#888888")
        net.add_edge(s, o, label=p, color=color)

    # Add type edges to T-box
    if show_tbox:
        for s, p, cls in type_triples:
            add_node(s)
            net.add_edge(s, cls, label="a", color="#7f8c8d", dashes=True)

    # Add missing predictions as dashed edges
    for s, _, o in missing_heads:
        add_node(s)
        add_node(o)
        net.add_edge(s, o, label="citizenOf (pred)", color="#e67e22", dashes=True)

    html = net.generate_html()
    components.html(html, height=600, scrolling=True)

    st.caption("Minh hoạ AMIE (đồ chơi): nét đứt là bộ ba được quy tắc suy ra nhưng còn thiếu trong KG; cạnh 'a' nối cá thể tới lớp (T-box).")



def render():
    st.header("Phương pháp dựa trên quy tắc")
    st.info("**Phương pháp dựa trên quy tắc (Rule-based)** khai thác các mẫu quy tắc ẩn tồn hiện hữu trong đồ thị hoặc dữ liệu để suy luận và đề xuất các bộ ba mới. Các quy tắc này thường có dạng biểu thức logic đơn giản, ví dụ: nếu A liên quan đến B và B liên quan đến C thì A có thể liên quan đến C.")

    # fundamental concepts
    st.write("Các thực thể trong một đồ thị tri thức tồn tại trong mối quan hệ với nhau. Một mối quan hệ giữa 2 thực thể trong đồ thị có thể được tổng quát hoá thông qua một hoặc nhiều mệnh đề logic bậc 1. Với quan sát này, ta có thể sử dụng mệnh đề Horn để suy luận ra các bộ ba mới dựa trên các bộ ba đã biết.")
    st.latex(r"""
    B \rightarrow H
    """)
    st.write("Một ví dụ kinh điển thể hiện việc sử dụng mệnh đề Horn để suy luận là quy tắc bắc cầu (transitive rule):")
    st.latex(r"""
    (x, \text{is\_ancestor\_of}, y) \land (y, \text{is\_ancestor\_of}, z) \rightarrow (x, \text{is\_ancestor\_of}, z)
    """)
    st.write("Hoặc quy tắc đường dẫn (path rule):")
    st.latex(r"""
    (x, \text{is\_parent\_of}, y) \land (y, \text{is\_parent\_of}, z) \rightarrow (x, \text{is\_grandparent\_of}, z)
    """)

    # pros and cons
    st.write("**Ưu điểm**: minh bạch và khả diễn, không cần dữ liệu huấn luyện lớn. Một bộ quy tắc có thể áp dụng cho nhiều đồ thị khác nhau, giúp mở rộng phạm vi suy luận.")
    st.write("**Nhược điểm**: phụ thuộc vào chất lượng và phạm vi của các quy tắc đã được định nghĩa. Khó khăn trong việc xử lý các mối quan hệ phức tạp hoặc ngữ cảnh đa nghĩa. Hiệu suất suy luận có thể giảm khi áp dụng trên đồ thị lớn với nhiều quy tắc.")

    st.divider()

    # supports
    st.write("Nhằm đảm bảo chất lượng của các quy tắc được khai thác từ đồ thị, một số độ đo được phát triển để đánh giá mức độ tin cậy và tính phổ quát của quy tắc đó.")
    st.markdown(r"""
        - **Support** số lượng bộ ba $$(x_i,r,y_i)$$ thoả mãn toàn bộ quy tắc thuộc KG.
        $$
            support(B^{\rightarrow} \rightarrow (x,r,y)) = \#(x_i,y_i) : body(x_i,y_i) \land head(x_i,y_i)
        $$
        - **Standard Confidence** tỉ lệ bộ ba $$(x_i,r,y_i)$$ thoả mãn toàn bộ quy tắc so với số bộ ba $$(x_i,r,y_i)$$ chỉ thoả mãn chuỗi suy luận (Body) của quy tắc.
        $$
            confidence(B^{\rightarrow} \rightarrow (x,r,y)) = \frac{\#(x_i,y_i) : body(x_i,y_i) \land head(x_i,y_i)}{\#(x_i,y_i) : body(x_i,y_i)}
        $$
        - **Head Coverage** tỉ lệ bộ ba $$(x_i,r,y_i)$$ thoả mãn quy tắc so với tổng số bộ ba $$(x_i,r,y_i)$$ trong KG.
        $$
            headCoverage(B^{\rightarrow} \rightarrow (x,r,y)) = \frac{support(B^{\rightarrow} \rightarrow (x,r,y))}{\#(x_i,r,y_i)}
        $$
    """)
    st.write("Ngoài ra, các thuật toán sẽ có các cơ chế đánh gía riêng như độ dài quy tắc, tính mới mẻ hoặc tẩm quan trọng của quy tắc.")

    st.divider()

    with st.expander("AMIE"):
        AMIE()
    with st.expander("Một số công trình nổi bật"):
        st.markdown(
            """
            - [AMIE+](https://dl.acm.org/doi/10.1007/s00778-015-0394-1?utm_source=chatgpt.com): mở rộng AMIE vả tối ưu hoá cách áp dụng các toán tử và loại bỏ các quy tắc thừa.
            - [AnyBURL](https://www.ijcai.org/proceedings/2019/0435.pdf?utm_source=chatgpt.com): Khác với AMIE, AnyBURL bắt đầu với việc trích xuất Horn Rule từ các đường đi ngẫu nhiên giữa hai thực thể trên đồ thị hiện hữu (bắt đầu từ các bộ ba hiện hữu và tổng quát hoá thành quy tắc).
            - Trong những năm gần đây, các nghiên cứu mới dần chuyển dịch sang kết hợp việc khai thác quy tắc và nhúng đồ thị (graph embedding) để tận dụng ưu điểm của cả hai phương pháp. Một số công trình có thể kể đến như (RUGE)[https://arxiv.org/abs/1711.11231?utm_source=chatgpt.com] và [IterE](https://arxiv.org/abs/1903.08948?utm_source=chatgpt.com).
            """
        )