import pandas as pd
import plotly.express as px
from datetime import datetime

url = 'https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-voc.csv'  

prov_dict = {
	"AB" : "Alberta",
	"BC" : "British Columbia",
	"CA" : "Canada",
	"MB" : "Manitoba",	
	"NB" : "New Brunswick",
	"NL" : "Newfoundland and Labrador",
	"NS" : "Nova Scotia",
	"NT" : "Northwest Territories",
	"NU" : "Nunavut",
	"ON" : "Ontario",
	"PE" : "Prince Edward Island",
	"QC" : "Quebec",
	"SK" : "Saskatchewan",
	"YK" : "Yukon",
	"YT" : "Yukon"
}

colours = ["#012169", "#E03C31", "green", "lightgray"]


df = pd.read_csv(url)
df["Province"] = df.apply(lambda r: prov_dict[r["prov"]], axis=1)

dfuk = df.copy()
dfuk["Variant"] = "B.1.1.7 (UK)"
dfuk["Count"] = dfuk["b117"].fillna(0)

dfsa = df.copy()
dfsa["Variant"] = "B.1.351 (South Africa)"
dfsa["Count"] = dfsa["b1351"].fillna(0)

dfbr = df.copy()
dfbr["Variant"] = "P.1 (Brazil)"
dfbr["Count"] = dfbr["p1"].fillna(0)

dfvoc = dfuk.append(dfsa).append(dfbr)

dfvocmax = dfvoc.groupby(["Province", "Variant"]).max().reset_index() \
[["Province", "Variant", "Count"]] \
.rename(columns={"Count" : "MaxVocCount"}) 

dfvoc = pd.merge(dfvoc, dfvocmax, how="left", left_on=["Province", "Variant"], right_on=["Province", "Variant"])
dfvoc = dfvoc.sort_values(by=["Variant", "MaxVocCount", "report_date"], ascending=[True, False, True])

dfvoc["New"] = dfvoc.groupby(["Province", "Variant"])["Count"].diff()

dfprov = dfvoc[dfvoc["Province"] != "Canada"]

figlineprov = px.line(dfprov, 
       x="report_date", y="Count", color="Variant", facet_row="Province",
       labels={"report_date" : "Time (Reported Date)", "Count" : "Cumulative cases", "Province" : "Province/Territory"},
       title="Cumulative cases with a Variant of Concern by Reported Date<br>by Province/Territory by Variant",
       height=5000, facet_row_spacing=0.01, template="simple_white", color_discrete_sequence=colours
      )

figbarprovd = px.bar(dfprov, x="report_date", y="New", color="Variant", facet_row="Province",
       labels={"report_date" : "Time (Reported Date)", "New" : "New Cases", "Province" : "Province/Territory", "Variant" : "Variant of Concern"},
       hover_name="Variant",
       title="New cases with a Variant of Concern by Reported Date<br>by Province/Territory",
       height=5000, template="plotly_white", color_discrete_sequence=colours
       )
