import streamlit as st

def AIME():
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
    st.write("Bộ quy tắc mà AIME muốn khai thác được cấu thành từ một chuỗi nguyên tử và kết luận của nó cũng là một nguyên tử:")
    columns = st.columns(2)
    with columns[0]:
        st.latex(r"""B_1 \land B_2 \land ... \land B_n \rightarrow r(x, y)""")
    with columns[1]:
        st.latex(r"""B^{\rightarrow} \rightarrow r(x, y)""")

    # operators
    st.write("Nhằm thu hẹp không gian tìm kiếm, bắt đầu với 1 nguyên tử duy nhất, AIME tuần tự áp dụng 1 trong các phép biến đổi (operators) sau để mở rộng quy tắc hiện tại:")
    st.markdown(
        """
        - **Add Dangling Atom (AD)**: thêm một nguyên tử mới với một biến mới và có chung biến còn lại với bộ quy tắc đang được khai thác.
        - **Add Closing Atom (AC)**: thêm một nguyên tử mới với hai biến của nó đã được sử dụng bởi bộ quy tắc đang được khai thác.
        - **Add Instantiated Atom (AI)**: thêm một nguyên tử mới với ít nhất 1 biến là thực thể thuộc đồ thị và có chung biến còn lại (thực thể hoặc lớp) với bộ quy tắc đang được khai thác.
        """
    )
    st.write("Quá trình rule mining sẽ được thực hiện tuần tự ")

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

    with st.expander("AMIE"):
        AIME()