import streamlit as st

def render():
    st.header("Tính không đầy đủ")
    st.subheader("Khái niệm")
    st.write(
        """
        Tính không đầy đủ (incompleteness) đề cập đến thực tế rằng đồ thị tri thức (KG) không bao quát đầy đủ các thực thể, thuộc tính, và quan hệ tồn tại trong thế giới thực. 
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
