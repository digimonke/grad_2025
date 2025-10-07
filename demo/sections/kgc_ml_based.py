import streamlit as st

def TransE():
    st.divider()
    st.markdown(
        """
        [**TransE**](https://proceedings.neurips.cc/paper/2013/hash/1cecc7a77928ca8133fa24680a88d2f9-Abstract.html) lần đầu giới thiệu ý tưởng này với một hàm tính điểm bộ ba đơn giản, điểm h trên không gian đa chiều được dịch chuyển bởi vector r để đến gần điểm t. Mục tiêu là tối thiểu hoá khoảng cách giữa điểm đích t và điểm sau khi dịch chuyển h + r.
        """
    )
    st.latex(r"f_r(h, t) = {||\mathbf{h} + \mathbf{r} - \mathbf{t}||}^2_2")
    st.markdown("Kết quả thực nghiệm cho thấy, TransE chỉ phù hợp áp dụng cho các đồ thị với quan hệ 1-1, không hiệu quả với các quan hệ 1-n, n-1 hoặc n-n vì phép tịnh tiến buộc các thực thể phải bị gom cụm với nhau.")

def TransH():
    st.divider()
    st.markdown(
        """
        [**TransH**](https://ojs.aaai.org/index.php/AAAI/article/view/8870) cải tiến TransE bằng cách cho phép mỗi quan hệ có một siêu phẳng (hyperplane) riêng trong không gian đa chiều. Mỗi thực thể được chiếu lên siêu phẳng này trước khi áp dụng phép tịnh tiến, giúp mô hình linh hoạt hơn trong việc biểu diễn các quan hệ phức tạp như 1-n, n-1 và n-n.
        """
    )
    st.latex(r"f_r(h, t) = {||\mathbf{h}_{\perp} + \mathbf{r} - \mathbf{t}_{\perp}||}^2_2")
    cols = st.columns(2)
    with cols[0]:
        st.latex(r"\mathbf{h}_{\perp} = \mathbf{h} - \mathbf{w}_r^{\top} \mathbf{h} \mathbf{w}_r")
    with cols[1]:
        st.latex(r"\mathbf{t}_{\perp} = \mathbf{t} - \mathbf{w}_r^{\top} \mathbf{t} \mathbf{w}_r")
    st.markdown("Tuy thể hiện tốt hơn TransE trên các quan hệ phức tạp, TransH vẫn gặp hạn chế khi được áp dụng lên các đồ thị phức tạp. Việc này là do cả TransH và TransE đều cho rằng các thực thể và quan hệ dù cùng hay khác loại đều được biểu diễn trong cùng một không gian đa chiều. Việc nén thông tin phức tạp vào cùng một vùng không gian có hệ quả dẫn đến mất mát thông tin và giảm hiệu quả biểu diễn.")

def TransR():
    st.divider()
    st.markdown(
        """
        [**TransR**](https://www.ijcai.org/Proceedings/15/Papers/534.pdf) tiếp tục cải tiến ý tưởng của TransH bằng cách biểu diễn thực thể và quan hệ trong các không gian đa chiều riêng biệt. Mỗi quan hệ được gán một ma trận chuyển đổi để chiếu các thực thể từ không gian chung sang không gian đặc trưng của quan hệ đó trước khi áp dụng phép tịnh tiến.
        """
    )
    st.latex(r"f_r(h, t) = {||\mathbf{M}_r \mathbf{h} + \mathbf{r} - \mathbf{M}_r \mathbf{t}||}^2_2")
    cols = st.columns(3)
    with cols[0]:
        st.latex(r"\mathbf{M}_r \in \mathbb{R}^{m \times n}")
    with cols[1]:
        st.latex(r"\mathbf{h},\mathbf{t} \in \mathbb{R}^n")
    with cols[2]:
        st.latex(r"\mathbf{r} \in \mathbb{R}^m")
    st.markdown("Việc sử dụng ma trận chuyển đổi cho phép TransR linh hoạt hơn trong việc biểu diễn các quan hệ phức tạp và đa dạng. Tuy nhiên, nhược điểm của TransR là số lượng tham số lớn do mỗi quan hệ cần một ma trận riêng, dẫn đến quá khớp (overfitting) và yêu cầu tính toán cao.")

def TransD():
    st.divider()
    st.markdown(
        """
        [**TransD**](https://www.ijcai.org/Proceedings/16/Papers/534.pdf) tiếp tục cải tiến mô hình bằng cách sử dụng các vector đặc trưng riêng biệt cho cả thực thể và quan hệ để xây dựng ma trận chuyển đổi động. Điều này giúp giảm số lượng tham số cần học và tăng khả năng biểu diễn của mô hình.
        """
    )
    st.latex(r"f_r(h, t) = {||\mathbf{M}_{r,h} \mathbf{h} + \mathbf{r} - \mathbf{M}_{r,t} \mathbf{t}||}^2_2")
    cols = st.columns(4)
    with cols[0]:
        st.latex(r"\mathbf{M}_{r,h} = \mathbf{r}_p \mathbf{h}_p^{\top} + \mathbf{I}")
    with cols[1]:
        st.latex(r"\mathbf{M}_{r,t} = \mathbf{r}_p \mathbf{t}_p^{\top} + \mathbf{I}")
    with cols[2]:
        st.latex(r"\mathbf{h},\mathbf{t} \in \mathbb{R}^n")
    with cols[3]:
        st.latex(r"\mathbf{r},\mathbf{h}_p,\mathbf{t}_p \in \mathbb{R}^m")
    st.markdown("TransD khắc phục được nhược điểm về số lượng tham số bằng cách sử dụng các vector đặc trưng riêng biệt cho cả thực thể và quan hệ, từ đó giảm thiểu số lượng tham số cần học.")

def GeoTranslationals():
    st.markdown(
        """
        Các phương pháp thuộc nhóm này xem các thực thể của đồ thị là các điểm tồn tại trong không gian đa chiều, một quan hệ được biểu diễn như một phép tịnh tiến (translation) từ điểm biểu diễn thực thể này sang điểm biểu diễn thực thể khác.
        """
    )
    cols = st.columns(2)
    with cols[0]:
        st.latex(r"\mathbf{h},\mathbf{t} \in \mathbb{R}^n")
    with cols[1]:
        st.latex(r"\mathbf{r} \in \mathbb{R}^m")

    TransE()

    TransH()

    TransR()

    TransD()

def render():
    st.header("Phương pháp dựa trên học máy")
    st.info("**Phương pháp học máy (Machine Learning-based)** sử dụng các thuật toán học máy nhằm học được bộ nhúng đồ thị tối ưu chứa đựng biểu diễn của các thực thể và quan hệ trong đồ thị dưới dạng mã hoá và dùng chúng để dự đoán các thành phần còn thiếu.")
    
    with st.expander("Nhóm phương pháp dựa trên tịnh tiến (Translational) trong không gian đa chiều"):
        GeoTranslationals()