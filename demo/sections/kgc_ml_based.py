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
        [**TransR**](https://ojs.aaai.org/index.php/AAAI/article/view/9491/9350) tiếp tục cải tiến ý tưởng của TransH bằng cách biểu diễn thực thể và quan hệ trong các không gian đa chiều riêng biệt. Mỗi quan hệ được gán một ma trận chuyển đổi để chiếu các thực thể từ không gian chung sang không gian đặc trưng của quan hệ đó trước khi áp dụng phép tịnh tiến.
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
        [**TransD**](https://aclanthology.org/P15-1067.pdf) tiếp tục cải tiến mô hình bằng cách sử dụng các vector đặc trưng riêng biệt cho cả thực thể và quan hệ để xây dựng ma trận chuyển đổi động. Điều này giúp giảm số lượng tham số cần học và tăng khả năng biểu diễn của mô hình.
        """
    )
    st.markdown("Mỗi thành phần (thực thể hoặc quan hệ) trong đồ thị được cấu thành bởi một cặp vector, một vector để mã hoá ý nghĩa của thành phần đó, và một vector đặc trưng để xây dựng ma trận chuyển đổi.")
    st.latex(r"\mathbf{h}, \mathbf{h}_p, \mathbf{r}, \mathbf{r}_p, \mathbf{t}, \mathbf{t}_p")
    cols = st.columns(2)
    with cols[0]:
        st.latex(r"\mathbf{h}, \mathbf{h}_p, \mathbf{t}, \mathbf{t}_p \in \mathbb{R}^n")
    with cols[1]:
        st.latex(r"\mathbf{r}, \mathbf{r}_p \in \mathbb{R}^m")
    
    st.markdown("Với mỗi bộ ba (h, r, t), ta có một cặp ma trận chuyển đổ để ánh xạ thực thể vào không gian đặc trưng của quan hệ:")
    cols = st.columns(2)
    with cols[0]:
        st.latex(r"\mathbf{M}_{rh} = \mathbf{r}_p \mathbf{h}_p^{\top} + \mathbf{I}^{m \times n}")
    with cols[1]:
        st.latex(r"\mathbf{M}_{rt} = \mathbf{r}_p \mathbf{t}_p^{\top} + \mathbf{I}^{m \times n}")

    st.markdown("Với cặp ma trận chuyển đổi trên, ta có vector của thực thể h và t trong không gian đặc trưng của quan hệ r và hàm tính điểm của TransD như sau")
    st.latex(r"f_r(h, t) = {||\mathbf{h}_{\perp} + \mathbf{r} - \mathbf{t}_{\perp}||}^2_2")
    cols = st.columns(2)
    with cols[0]:
        st.latex(r"\mathbf{h}_{\perp} = \mathbf{M}_{rh} \mathbf{h}")
    with cols[1]:
        st.latex(r"\mathbf{t}_{\perp} = \mathbf{M}_{rt} \mathbf{t}")

def GeoTranslationalsModels():
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

    with st.expander("Minh hoạ trực quan"):
        st.image("resources/trans.png")

def Rescal():
    st.divider()
    st.markdown(
        r"""
        [**RESCAL**](http://www.cip.ifi.lmu.de/~nickel/data/slides-icml2011.pdf) là một trong những mô hình tương thích nhúng đầu tiên được đề xuất. Mỗi quan hệ được biểu diễn bằng một ma trận, và hàm tính điểm của bộ ba (h, r, t) được định nghĩa là tích vô hướng giữa vector thực thể h, ma trận quan hệ r và vector thực thể t.
        Mô hình này hoạt động dựa trên 2 ma trận nhúng:
        - $$\mathbf{A} \in \mathbb{R}^{n \times d}$$: ma trận nhúng của tập thực thể thuộc đồ thị với d là kích thước của chiều ẩn (latent dimension).
        - $$\mathbf{R} \in \mathbb{R}^{m \times d \times d}$$: ma trận nhúng của quan hệ thứ k trong đồ thị.
        """
    )

    st.markdown("Ma trận kề của quan hệ thứ k được xấp xỉ bởi tích của ma trận nhúng thực thể và ma trận nhúng quan hệ:")
    st.latex(r"\mathbf{X}^{(k)} \approx \mathbf{A}^{\top} \mathbf{R}^{(k)} \mathbf{A}")

    st.markdown("Xác xuất của bộ ba (h,r,t) tồn tại trong đồ thị:")
    st.latex(r"f_r(h, t) = \mathbf{a}_h^{\top} \mathbf{R}^{(k)} \mathbf{a}_t")

    st.markdown("Hàm lỗi của RESCAL được định nghĩa như sau:")
    st.latex(r"\min_{A, \{R^{(k)}\}} \sum_{k=1}^{m} \left\| X^{(k)} - A R^{(k)} A^\top \right\|_{F}^{2} + \lambda \left( \|A\|_{F}^{2} + \sum_{k} \|R^{(k)}\|_{F}^{2} \right)")

def DisMult():
    st.divider()
    st.markdown(
        r"""
        [**DistMult**](https://arxiv.org/pdf/1412.6575) đơn giản hoá RESCAL bằng cách giả định rằng ma trận quan hệ là ma trận chéo. Điều này làm giảm số lượng tham số cần học và tăng hiệu quả tính toán, nhưng giới hạn khả năng biểu diễn các quan hệ không đối xứng.
        Ma trận thực thể và quan hệ của DistMult có dạng
        - $$ \mathbf{A} \in \mathbb{R}^{n \times d} $$: ma trận nhúng của tập thực thể thuộc đồ thị với d là kích thước của chiều ẩn (latent dimension).
        - $$ \mathbf{R} \in \mathbb{R}^{m \times d} $$: ma trận nhúng quan hệ của tập quan hệ thuộc đồ thị.
        """
    )
    st.markdown(
        """
        Ma trận kề của quan hệ thứ k được xấp xỉ bởi tích của ma trận nhúng thực thể và ma trận đường chéo được xây dựng từ vector đặc trưng cảu quan hệ thứ k:
        """
    )
    st.latex(r"\mathbf{X}^{(k)} \approx \mathbf{A}^{\top} \text{diag}(\mathbf{r}_k) \mathbf{A}")

    st.markdown("Xác xuất của bộ ba (h,r,t) tồn tại trong đồ thị:")
    st.latex(r"f_r(h, t) = \mathbf{a}_{h}^{\top} \text{diag}(\mathbf{r}) \mathbf{a}_{t}")

    st.markdown(r"""DisMult tạo mẫu dữ liệu lỗi từ tập dữ liệu huấn luyện bằng cách thay thế ngẫu nhiên chủ thể hoặc đối tượng trong bộ ba. Hàm lỗi của DisMult được định nghĩa như sau:""")
    st.latex(r"\mathcal{L} = - \sum_{(h,r,t) \in \mathcal{T}} \log \sigma(f_r(h,t)) - \sum_{(h', r, t') \notin \mathcal{T}} \log(1 - \sigma(f_r(h', t')))")

    st.markdown("DisMult cải thiện đáng kể so với RESCAL về hiệu quả tính toán và khả năng mở rộng, đặc biệt trên các đồ thị lớn. Tuy nhiên, do giả định ma trận quan hệ là ma trận chéo, DistMult không thể biểu diễn hiệu quả đồ thị có quan hệ bất đối xứng.")

def ComPlex():
    st.divider()
    st.markdown(
        r"""
        [**ComplEx**](http://proceedings.mlr.press/v48/trouillon16.pdf) mở rộng DistMult bằng cách đưa biểu diễn của thực thể và quan hệ vào không gian phức.
        Điều này cho phép mô hình biểu diễn các quan hệ không đối xứng, nhưng vẫn giữ được tính đơn giản và hiệu quả tính toán mà DisMult mang lại.
        Ma trận thực thể và quan hệ của ComplEx có dạng
        - $$ \mathbf{A} \in \mathbb{C}^{n \times d} $$: ma trận nhúng của tập thực thể thuộc đồ thị với d là kích thước của chiều ẩn (latent dimension).
        - $$ \mathbf{R} \in \mathbb{C}^{m \times d} $$: ma trận nhúng quan hệ của tập quan hệ thuộc đồ thị.
        """
    )
    st.markdown(
        """
        Ma trận kề của quan hệ thứ k được xấp xỉ bởi tích của ma trận nhúng thực thể và ma trận đường chéo được xây dựng từ vector đặc trưng cảu quan hệ thứ k:
        """
    )
    st.latex(r"\mathbf{X}^{(k)} \approx Re(\langle \mathbf{A}, \mathbf{R}^{k}, \overline{\mathbf{A}} \rangle)")

    st.markdown("Xác xuất của bộ ba (h,r,t) tồn tại trong đồ thị:")
    st.latex(r"f_r(h, t) = Re(\langle \mathbf{a}_{h}, \mathbf{r}, \overline{\mathbf{a}_{t}} \rangle) = Re(\sum_{i=1}^{d} a_{h,i} r_i \overline{a_{t,i}})")

    st.markdown(
        r"""
        Ý tưởng chính của ComPlex trong việc sử dụng không gian nhúng phức là vận dụng phép liên hợp cho vector nhúng đối tượng t.
         Việc sử dụng phép liên hợp cho phép mô hình biểu diễn quan hệ không đối xứng (có chiều) được cho thấy thông qua ví dụ sau.
        """
    )
    st.markdown("Ta có")
    st.latex(r"f_r(h,t) = Re(\sum_{i=1}^{d} a_{h,i} r_i \overline{a_{t,i}})")
    cols = st.columns(3)
    with cols[0]:
        st.latex(r"a_{h,i} = a + ib")
    with cols[1]:
        st.latex(r"\overline{a_{t,i}} = c - id")
    with cols[2]:
        st.latex(r"r_i = e + if")

    st.latex(r"\implies a_{h,i} \overline{a_{t,i}} = (a + ib)(c - id) = ac + bd + i(bc - ad)")
    st.latex(r"\implies a_{h,i} r_i \overline{a_{t,i}} = (ac + bd)e - (bc - ad)f + i((ac + bd)f + (bc - ad)e)")
    st.latex(r"\implies Re(a_{h,i} r_i \overline{a_{t,i}}) = (ac + bd)e - (bc - ad)f")
    
    st.markdown(r"Nếu ta hoán đổi vị trí h và t (đảo chiều quan hệ), ta có")
    st.latex(r"f_r(t,h) = Re(a_{t,i} r_i \overline{a_{h,i}}) = (ac + bd)e + (bc - ad)f")

def SemanticMatchingModels():
    st.markdown(
        """
        Trong khi các mô hình thuộc nhóm phương pháp tịnh tiến vector xem việc biểu diễn một bộ ba là một phép toán vector trong không gian đa chiều. Nhóm phương pháp dựa trên tương thích nhúng
        xem việc phân lớp một bộ ba (h,r,t) là một phép đo tương thích (similarity) giữa các vector nhúng của thực thể và quan hệ thông qua việc sử dụng phân rã tensor và hàm tính điểm song tuyến tính.
        """
    )
    st.markdown(
        r"""
        Một bộ ba (h,r,t) được biểu diễn bởi một tensor bậc 3 $$\mathbf{X} \in \mathbb{R}^{n \times n \times m}$$ 
        - $$\mathbf{n}$$ là số lượng thực thể của đồ thị
        - $$\mathbf{m}$$ là số lượng quan hệ của đồ thị
        - Mỗi mặt cắt $$\mathbf{X}^{(k)} \in \mathbb{R}^{n \times n}$$ biểu diễn ma trận quan hệ thứ k trong đồ thị. Giá trị của phần tử (i,j) trong ma trận này biểu diễn mức độ tương thích giữa thực thể i và thực thể j thông qua quan hệ k.
        """
    )

    Rescal()

    DisMult()

    ComPlex()

def RNN():
    st.divider()
    st.markdown(
        """ 
        [**Các mô hình dựa vào mạng neuron hồi quy (RNN)**](https://proceedings.neurips.cc/paper_files/paper/2017/file/0e55666a4ad822e0e34299df3591d979-Paper.pdf) khác với các mô hình tịnh tiến hay song tuyến tính chỉ hoạt động trong phạm vi một bộ ba, các mô hình dựa trên RNN suy luận **theo đường đi (path)** trong KG — tức là chuỗi các quan hệ nối hai thực thể.  
        Một đường đi như:
        """
    )
    st.latex(r"h \xrightarrow{r_1} e_1 \xrightarrow{r_2} e_2 \xrightarrow{r_3} t")
    st.markdown(
        """
        mang thông tin thành phần (compositional): nếu $h$ là "Obama", $r_1$ là "born\_in", và $r_2$ là "located\_in" thì đường đi có thể gợi ý quan hệ mục tiêu như $(Obama,\ citizen\_of,\ USA)$.  
        Một RNN (GRU/LSTM) có thể học cách các vector quan hệ **kết hợp tuần tự** để dự đoán các quan hệ ngầm như vậy.
        """
    )

    st.markdown(r"RNN xét một đường đi (path) giữ hai thực thể $$\mathbf{h}$$ và $$\mathbf{t}$$")
    st.latex(r"(r_1, r_2, \ldots, r_L)")
    
    st.markdown(r"Với trạng thái ẩn ở bước số 0 là nhúng của thực thể $$\mathbf{h}$$, RNN cập nhật trạng thái ẩn này với mỗi quan hệ trong đường đi tới $$\mathbf{t}$$:")
    st.latex(r"\mathbf{h}_0 = \mathbf{h}")
    st.latex(r"\mathbf{h}_i = f_{RNN}(\mathbf{h}_{i-1}, \mathbf{r}_i), \quad i=1,2,\ldots,L")
    st.latex(r"f_{RNN} = \sigma(\mathbf{W}_{rh}\mathbf{r}_t + \mathbf{W}_{hh}\mathbf{h}_{t-1} + \mathbf{b}_h)")
    st.markdown(
        """
        Trong đó
        - $$W_{rh}$$ là ma trận trọng số kết nối giữa đầu vào quan hệ và trạng thái ẩn
        - $$W_{hh}$$ là ma trận trọng số kết nối giữa trạng thái ẩn trước đó và trạng thái ẩn hiện tại
        - $$b_h$$ là vector bias cho trạng thái ẩn
        - $$\sigma$$ là hàm kích hoạt phi tuyến (ví dụ ReLU hoặc tanh)
        """
    )
    st.caption("Vì RNN có thể gặp vấn đề tiêu biến thông tin (vanishing gradient) với các đường đi dài, các biến thể như LSTM hoặc GRU thường được sử dụng để cải thiện khả năng học các phụ thuộc xa (long-range dependencies).")

    st.markdown("Sau khi xử lý toàn bộ đường đi, trạng thái ẩn cuối cùng $$\mathbf{h}_L$$ sẽ được sử dụng để dự đoán quan hệ giữa $$\mathbf{h}$$ và $$\mathbf{t}$$:")
    st.latex(r"f_r(h, t) = \underset{r}{\arg \max} \ \text{sim}(\mathbf{h}_L, \mathbf{r})")
    st.caption(r"Trong đó $$\text{sim}$$ là hàm đo độ tương đồng giữa hai vector.")

def CNN():
    st.divider()
    st.markdown(
        """
        [**ConvE (Convolutional Embeddings for Link Prediction)**](https://ojs.aaai.org/index.php/AAAI/article/download/11573/11432) vận dụng mạng neuron tích chập (CNN), thường được sử dụng trong xử lý ảnh, vào tác vụ dự đoán liên kết trong đồ thị tri thức.
        Thay vì tịnh tiến (TransE) hay tích song tuyến tính (DistMult), ConvE **biến đổi nhúng thành ma trận 2D** và áp dụng các bộ lọc tích chập để trích xuất các mẫu đặc trưng cục bộ (local feature patterns) trong vùng lận cận của thực thể thuộc đồ thị.
        """
    )

    st.markdown(r"Bắt đầu với nhúng của chủ thể $$\mathbf{h} \in \mathbb{R}^{d}$$ và quan hệ $$\mathbf{r} \in \mathbb{R}^{d}$$, CNN thực hiện nối vector và biến đổi vector thành ma trận 2D:")
    st.latex(r"\mathbf{h}, \mathbf{r} \in \mathbb{R}^{d}")
    st.latex(r"\mathbf{x} = [\mathbf{h};\mathbf{r}] \in \mathbb{R}^{2d}")

    st.markdown(r"""
        ConvE định nghĩa hai tham số $$\mathbf{m}$$ và $$\mathbf{n}$$ sao cho $$\mathbf{m} \times \mathbf{n} = 2d$$, và định nghĩa một hàm $$\text{reshape(x)}$$ biến đổi vector $$\mathbf{x}$$ thành ma trận 2D:
    """)
    st.latex(r"\mathbf{X} = \text{reshape}(\mathbf{x}) \in \mathbb{R}^{m \times n}")
    st.caption("Ví dụ, nếu kích thước nhúng $$d=200$$, ta có thể chọn $$m=20$$ và $$n=20$$ để biến đổi vector nhúng thành ma trận 20x20.")

    st.markdown("Sau khi biến đổi, ConvE áp dụng các lớp tích chập (convolutional layers) để trích xuất các đặc trưng cục bộ từ ma trận 2D này:")
    st.latex(r"\mathbf{Y} = \text{Conv2D}(\mathbf{X})")
    st.markdown("""
        Kết quả của phép tích chập là một tập hợp các bản đồ đặc trưng (feature maps) biểu diễn các mẫu đặc trưng cục bộ trong vùng lân cận của thực thể và quan hệ.
    """)

    st.markdown("Hàm tính điểm của 1 bộ ba cũng là xác suất bộ ba đó tồn tại trong đồ thị:")
    st.latex(r"f_r(h, t) = \sigma(vec(\mathbf{Y})\mathbf{W})^\top \mathbf{t}")
    st.caption(r"Trong đó $$\mathbf{W}$$ là ma trận ánh xạ để đưa vector $$vec(\mathbf{Y})$$ về không gian nhúng của thực thể, và $$\sigma$$ là hàm kích hoạt phi tuyến (ví dụ ReLU).")

def GCN():
    st.divider()
    st.markdown(
        """
        [**R‑GCN (Relational Graph Convolutional Networks)**](https://arxiv.org/pdf/1703.06103) áp dụng kiến trúc GCN vào **đồ thị tri thức** nhằm giải quyết bài toán dự đoán dữ liệu đa quan hệ. 
        Nhúng của mỗi thực thể được cập nhật bằng cách tổng hợp thông tin từ vùng lân cận, mỗi loại quan hệ có một ma trận biến đổi (transformation matrix) riêng.  
        Mỗi nút nhận thông điệp từ láng giềng theo các biến đổi phụ thuộc quan hệ sử dụng các ma trận chuyển đổi này.
        """
    )

    st.markdown(r"""
        Với mô hình [GCN](https://bibbase.org/service/mendeley/bfbbf840-4c42-3914-a463-19024f50b30c/file/25dbdd06-4704-a33f-23d9-c626b08adc1e/160902907.pdf.pdf) nguyên bản,
        nhúng của các thực thể là một tổng hợp thông tin từ vùng lân cận của nó với các quan hệ có giá trị tổng hợp như nhau.
    """)
    st.latex(r"\mathbf{h}_i^{(l+1)} = \sigma\!\left( \sum_{j \in \mathcal{N}_i} \mathbf{W}^{(l)} \mathbf{h}_j^{(l)}\right)")
    st.caption("Tuy nhiên, đồ thị tri thức có nhiều loại quan hệ khác nhau, và mỗi loại quan hệ có thể mang thông tin khác nhau. R-GCN mở rộng GCN bằng cách sử dụng các ma trận biến đổi phụ thuộc quan hệ để xử lý đa dạng các loại quan hệ trong đồ thị tri thức.")

    st.markdown(r"""
        R-GCN cải tiến GCN bằng cách sử dụng các ma trận biến đổi phụ thuộc quan hệ để xử lý đa dạng các loại quan hệ trong đồ thị tri thức.
    """)
    st.latex(r"h_i^{(l+1)} = \sigma \left( \sum_{r \in \mathcal{R}} \sum_{j \in \mathcal{N}_i^r} \frac{1}{c_{i,r}} W_r^{(l)} h_j^{(l)} + W_0^{(l)} h_i^{(l)} \right)")
    st.markdown(r"""
        Trong đó:
        - $$\mathcal{R}$$ là tập hợp các loại quan hệ trong đồ thị.
        - $$\mathcal{N}_i^r$$ là tập hợp các nút láng giềng của nút $$i$$ kết nối với nó qua quan hệ $$r$$.
        - $$c_{i,r}$$ là hệ số chuẩn hoá, thường là số lượng nút láng giềng của nút $$i$$ qua quan hệ $$r$$.
        - $$W_r^{(l)}$$ là ma trận biến đổi phụ thuộc quan hệ cho quan hệ $$r$$ ở lớp $$l$$.
        - $$W_0^{(l)}$$ là ma trận biến đổi cho nút $$i$$ để giữ thông tin của chính nó.
        - $$\sigma$$ là hàm kích hoạt phi tuyến (ví dụ ReLU).
    """)

    st.markdown(r"""R-GCN thường được huấn luyện chung với một module dự đoán liên kết (link prediction module) như DistMult hoặc ComPlex để dự đoán các bộ ba (h,r,t) trong đồ thị tri thức.""")

def DeepLearningModels():
    st.markdown(
        """
        Nhận thấy rằng các phương pháp thuộc hai nhóm còn lại chưa khai thác được thông tin từ các thực thể và quan hệ trong vùng lân cận trên đồ thị, 
        nhóm phương pháp dựa trên học sâu nhắm đến việc khai thác lượng thông tin dồi dào về cấu trúc và ngữ cảnh từ vòng lân cận của một cặp thực thể để dự đoán quan hệ giữa chúng.
        """
    )

    RNN()

    CNN()

    GCN()

def render():
    st.header("Phương pháp dựa trên học máy")
    st.info("""
        **Phương pháp học máy (Machine Learning-based)** sử dụng các thuật toán học máy nhằm học được bộ nhúng 
        đồ thị tối ưu chứa đựng biểu diễn của các thực thể và quan hệ trong đồ thị dưới dạng mã hoá và dùng chúng để dự đoán các thành phần còn thiếu. 
        Trong quá trình huấn luyện, các mô hình này tối ưu hoá bộ nhúng của thực thể và quan hệ dựa trên một hàm tính điểm bộ ba (h,r,t) 
        sao cho các bộ ba đúng có điểm số cao hơn các bộ ba sai.
    """)
    
    with st.expander("Nhóm phương pháp dựa trên tịnh tiến (Translational) vector trong không gian đa chiều"):
        GeoTranslationalsModels()
    with st.expander("Nhóm phương pháp dựa trên tương thích nhúng (Semantic Matching)"):
        SemanticMatchingModels()
    with st.expander("Nhóm phương pháp dựa trên học sâu (Deep Learning-based)"):
        DeepLearningModels()