# Import library
import bnlearn as bn

# Load example DAG with CPD
model = bn.import_DAG('./insurance/insurance.bif', CPD=True)

# Take 1000 samples from the CPD distribution
df = bn.sampling(model, n=1000, methodtype='bayes')

df.head()

df.to_csv('./insurance/insurance.csv', index=False)