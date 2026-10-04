"""Q4 v1: EDHEC calendar-year chasing under three strategy universes -> q4_res.json (+ per-year CSVs)."""
import pandas as pd, json
from q4 import run
df=pd.read_csv('hf/edhec_annual.csv',index_col=0)
out={}
out['nonover']=run(df,'nonover',exclude=('Funds Of Funds','Relative Value','Event Driven'))
out['nonover_noSS']=run(df,'nonover_noSS',exclude=('Funds Of Funds','Relative Value','Event Driven','Short Selling'))
out['all12']=run(df,'all12',exclude=('Funds Of Funds',),tops=(1,))
json.dump(out,open('q4_res.json','w'),default=float)
