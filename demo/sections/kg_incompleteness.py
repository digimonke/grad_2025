import streamlit as st
import requests
import pandas as pd
import altair as alt

def render():
    st.header("Tính không đầy đủ")
    st.info(
        """
        **Tính không đầy đủ (incompleteness)** đề cập đến thực tế rằng đồ thị tri thức (KG) không bao quát đầy đủ các thực thể, thuộc tính, và quan hệ tồn tại trong thế giới thực. 
        Nói cách khác, nhiều bộ ba (triples) đúng có thể chưa được biết hoặc có các bộ ba sai lệch do thiếu dữ liệu, lỗi trích xuất, hoặc hạn chế trong phạm vi bản thể học.
        """
    )

    st.subheader("Nguyên nhân phổ biến")
    st.markdown(
        """
        - Dữ liệu nguồn phân tán và dị thể: khó liên kết, chuẩn hoá thuật ngữ; thiếu ánh xạ giữa các hệ.
        - Giới hạn trích xuất thông tin: NER/RE/NLP chưa hoàn hảo; ngôn ngữ mơ hồ, thiếu ngữ cảnh.
        - Thiếu cập nhật theo thời gian: sự kiện mới, thay đổi thực tế không được đồng bộ kịp thời.
        - Phạm vi ontology chưa đủ: chưa mô hình hoá khái niệm/quan hệ cần thiết, thiếu domain/range/ràng buộc.
        - Chất lượng nhập liệu: quy trình nạp dữ liệu thiếu kiểm soát, bỏ sót hoặc sai kiểu dữ liệu.
        """
    )

    st.subheader("Hệ quả")
    st.markdown(
        """
        - Truy vấn không trả về kết quả đúng/đủ; khó trả lời câu hỏi năng lực (Competency Questions).
        - Suy luận yếu hoặc sai lệch; không phát hiện được ràng buộc/luận đề quan trọng.
        - Ảnh hưởng hệ gợi ý, trợ lý ảo, phân tích nguyên nhân–hệ quả do thiếu cạnh/cụm tri thức then chốt.
        - Giảm độ tin cậy khi tích hợp dữ liệu liên miền.
        """
    )

    st.subheader("Ví dụ")
    st.markdown(
        """
        - Y học: KG triệu chứng–bệnh có thể thiếu các quan hệ hiếm gặp (rare disease) do dữ liệu ít hoặc phân tán, dẫn tới chẩn đoán gợi ý không đầy đủ.
        - Địa lý: Thiếu các thuộc tính như dân số mới nhất hoặc mối quan hệ hành chính sau khi sáp nhập/tách tỉnh.
        - Doanh nghiệp: Thiếu mối quan hệ sở hữu/chức danh sau các thương vụ M&A mới công bố, làm sai lệch phân tích cấu trúc tổ chức.
        - Học thuật: Thiếu liên kết trích dẫn giữa các bài báo mới, làm yếu khả năng phân tích ảnh hưởng (impact) và phát hiện cộng đồng nghiên cứu.
        """
    )

    st.caption(
        "Lưu ý: Incompleteness khác với inconsistency (mâu thuẫn). Một KG có thể vừa thiếu, vừa chứa mâu thuẫn; cần quy trình vận hành để phát hiện và cải thiện dần."
    )

    st.divider()
    st.subheader("Ví dụ")
    st.write(
        "Theo thường thức, mỗi quốc gia nên có thủ đô. Tuy nhiên, trong DBpedia, nhiều quốc gia không có thuộc tính `dbo:capital`, thể hiện tính không đầy đủ của đồ thị tri thức."
    )

    DBPEDIA_SPARQL_ENDPOINT = "https://dbpedia.org/sparql"

    @st.cache_data(show_spinner=False, ttl=600)
    def run_sparql(query: str):
        headers = {"Accept": "application/sparql-results+json"}
        params = {"query": query, "format": "application/sparql-results+json"}
        resp = requests.get(DBPEDIA_SPARQL_ENDPOINT, headers=headers, params=params, timeout=25)
        resp.raise_for_status()
        return resp.json()

    @st.cache_data(show_spinner=False, ttl=600)
    def compute_property_completeness(class_iri: str, prop_iri: str, filter_dbpedia_ns: bool = True):
        filter_subj = (
            "FILTER(STRSTARTS(STR(?s), 'http://dbpedia.org/resource/'))"
            if filter_dbpedia_ns
            else ""
        )
        q_total = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {{
          ?s rdf:type <{class_iri}> .
          {filter_subj}
        }}
        """
        q_with = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {{
          ?s rdf:type <{class_iri}> .
          ?s <{prop_iri}> ?o .
          {filter_subj}
        }}
        """
        total = 0
        with_prop = 0
        try:
            data_total = run_sparql(q_total)
            data_with = run_sparql(q_with)
            total = int(data_total["results"]["bindings"][0]["count"]["value"]) if data_total["results"]["bindings"] else 0
            with_prop = int(data_with["results"]["bindings"][0]["count"]["value"]) if data_with["results"]["bindings"] else 0
        except Exception as e:
            raise e
        missing = max(total - with_prop, 0)
        pct = (with_prop / total * 100.0) if total else 0.0
        return {
            "total": total,
            "with_prop": with_prop,
            "missing": missing,
            "pct": pct,
        }

    # Presets
    class_presets = {
        "dbo:Country": "http://dbpedia.org/ontology/Country",
        "dbo:City": "http://dbpedia.org/ontology/City",
        "dbo:Person": "http://dbpedia.org/ontology/Person",
        "dbo:University": "http://dbpedia.org/ontology/University",
        "dbo:Film": "http://dbpedia.org/ontology/Film",
    }
    prop_presets = {
        "dbo:Country": [
            ("dbo:capital", "http://dbpedia.org/ontology/capital"),
            ("dbo:populationTotal", "http://dbpedia.org/ontology/populationTotal"),
        ],
        "dbo:City": [
            ("dbo:country", "http://dbpedia.org/ontology/country"),
            ("dbo:populationTotal", "http://dbpedia.org/ontology/populationTotal"),
        ],
        "dbo:Person": [
            ("dbo:birthPlace", "http://dbpedia.org/ontology/birthPlace"),
            ("dbo:deathPlace", "http://dbpedia.org/ontology/deathPlace"),
            ("dbo:spouse", "http://dbpedia.org/ontology/spouse"),
        ],
        "dbo:University": [
            ("dbo:numberOfStudents", "http://dbpedia.org/ontology/numberOfStudents"),
            ("dbo:foundingYear", "http://dbpedia.org/ontology/foundingYear"),
        ],
        "dbo:Film": [
            ("dbo:starring", "http://dbpedia.org/ontology/starring"),
            ("dbo:director", "http://dbpedia.org/ontology/director"),
        ],
    }

    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        class_key = st.selectbox("Chọn lớp (class)", list(class_presets.keys()), index=0)
    with c2:
        prop_options = prop_presets.get(class_key, [])
        prop_label_to_iri = {lbl: iri for lbl, iri in prop_options}
        default_prop_label = prop_options[0][0] if prop_options else ""
        prop_label = st.selectbox("Chọn thuộc tính (property)", list(prop_label_to_iri.keys()), index=0 if default_prop_label else None)
    with c3:
        filter_dbpedia_ns = st.checkbox("Chỉ tính subject thuộc DBpedia", value=True, help="Lọc ?s bắt đầu bằng http://dbpedia.org/resource/")

    # Advanced inputs
    with st.expander("Tùy chọn nâng cao: tự nhập IRI"):
        custom_class = st.text_input("Class IRI", value=class_presets[class_key])
        custom_prop = st.text_input("Property IRI", value=prop_label_to_iri.get(prop_label, ""))

    run = st.button("Chạy đo lường")
    if run:
        try:
            with st.spinner("Đang truy vấn DBpedia…"):
                result = compute_property_completeness(custom_class.strip(), custom_prop.strip(), filter_dbpedia_ns)
            st.success("Hoàn tất.")
            st.metric("Tổng số thực thể", result["total"])
            st.metric(f"Số có thuộc tính", result["with_prop"])            
            st.metric("Tỉ lệ đầy đủ (%)", f"{result['pct']:.2f}%")

            df = pd.DataFrame([
                {"Trạng thái": "Có thuộc tính", "Số lượng": result["with_prop"]},
                {"Trạng thái": "Thiếu", "Số lượng": result["missing"]},
            ])
            chart = (
                alt.Chart(df)
                .mark_bar()
                .encode(x=alt.X("Trạng thái:N", sort=None), y=alt.Y("Số lượng:Q"), color="Trạng thái:N")
                .properties(height=220)
            )
            st.altair_chart(chart, use_container_width=True)

            st.caption(
                f"Nguồn: DBpedia SPARQL Endpoint — Class: <{custom_class}>, Property: <{custom_prop}>. "
                "Kết quả được cache trong 10 phút để hạn chế tải lên endpoint."
            )
        except requests.RequestException as e:
            st.error(f"Lỗi mạng khi truy vấn DBpedia: {e}")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
