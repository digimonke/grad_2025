import streamlit as st
import bnlearn
from utils import bnlearn_dag_to_dot
import requests
import gzip
from io import BytesIO
try:
	from pgmpy.readwrite import BIFReader
except Exception:
	BIFReader = None

# 1. import example
st.header("Cấu trúc nhân quả mục tiêu")

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
				dag = {"model": model}
				st.session_state.dag = dag

				# Show basic info
				try:
					n_nodes = len(model.nodes())
					n_edges = len(model.edges())
					st.caption(f"DAG 'insurance': {n_nodes} nút, {n_edges} cạnh")
				except Exception:
					st.caption("Không đọc được thông tin nút/cạnh từ DAG.")

				# Render with Graphviz in Streamlit (no system Graphviz required)
				dot = bnlearn_dag_to_dot(dag)
				st.graphviz_chart(dot, use_container_width=True)

		
	except Exception as e:
		st.error(f"Lỗi tải DAG: {e}")
else:
	st.info("Nhấn nút để tải và hiển thị DAG 'Insurance'.")

