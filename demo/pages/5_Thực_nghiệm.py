import streamlit as st
from utils import bnlearn_dag_to_dot, simulate_nonlinear_sem_from_pgmpy
import requests
import gzip
from io import BytesIO
try:
	from pgmpy.readwrite import BIFReader
except Exception:
	BIFReader = None

# 1. import example
st.subheader("Cấu trúc nhân quả mục tiêu")

# Use session state to load on demand without writing anything to disk
if 'dag' not in st.session_state:
	st.session_state.dag = None

if st.session_state.dag is None:
	# Download BIF.gz on demand and parse fully in-memory
	BIF_URL = "https://www.bnlearn.com/bnrepository/insurance/insurance.bif.gz"
	try:
		with st.spinner("Đang tải Insurance.bif từ bnlearn repository..."):
			resp = requests.get(BIF_URL, timeout=20)
			resp.raise_for_status()
			compressed = BytesIO(resp.content)
			with gzip.GzipFile(fileobj=compressed, mode='rb') as gz:
				bif_text = gz.read().decode('utf-8')
		
            # Some pgmpy versions accept 'string' kw, others offer from_string
			model = None
			try:
				reader = BIFReader(string=bif_text)  # type: ignore[arg-type]
				model = reader.get_model()
			except Exception:
				try:
					reader = BIFReader.from_string(bif_text)  # type: ignore[attr-defined]
					model = reader.get_model()
				except Exception as e:
					st.error(f"Không thể parse BIF trong bộ nhớ: {e}")

			if model is not None:
				st.session_state.dag = model
	except Exception as e:
		st.error(f"Lỗi tải DAG: {e}")
	
# Show basic info
try:
    n_nodes = len(st.session_state.dag.nodes())
    n_edges = len(st.session_state.dag.edges())
    st.caption(f"DAG 'insurance': {n_nodes} nút, {n_edges} cạnh")
except Exception:
    st.caption("Không đọc được thông tin nút/cạnh từ DAG.")

# Render with Graphviz in Streamlit (no system Graphviz required)
dot = bnlearn_dag_to_dot({"model": st.session_state.dag})
st.graphviz_chart(dot, use_container_width=True)

# 2 dữ liệu mô phỏng
st.subheader("Dữ liệu mô phỏng từ DAG")

if st.session_state.dag is not None:
	with st.form(key="simulate_form"):
		c1, c2, c3 = st.columns([1.2, 1, 1])
		with c1:
			sem_type = st.selectbox("Cấu tạo hàm (functional form)", options=["Multilayer Perceptron", "Gaussian Process"], index=0)
		with c2:
			n_samples = st.number_input("Số mẫu", min_value=10, max_value=20000, value=1000, step=100)
		with c3:
			noise_scale = st.number_input("Độ lệch nhiễu (σ)", min_value=0.0, value=1.0, step=0.1)

		submitted = st.form_submit_button("Tạo dữ liệu")

	if submitted:
		with st.spinner("Đang mô phỏng dữ liệu..."):
			try:
				df_sim = simulate_nonlinear_sem_from_pgmpy(
					st.session_state.dag, n=int(n_samples), sem_type=sem_type, noise_scale=float(noise_scale)
				)
				st.session_state["simulated_df"] = df_sim
				st.success(f"Đã tạo dữ liệu: {df_sim.shape[0]}x{df_sim.shape[1]}. 20 dòng đầu tiên hiển thị bên dưới.")
			except Exception as e:
				st.error(f"Không thể mô phỏng dữ liệu: {e}")

	df_sim = st.session_state.get("simulated_df")
	if df_sim is not None:
		st.dataframe(df_sim.head(20), use_container_width=True)

else:
	st.info("Chưa có DAG để mô phỏng. Hãy tải DAG trước.")
