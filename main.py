
# %%
import numpy as np
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from enum import Enum
import carbonCalculationUtils as carbon

pd.set_option('display.max_rows', 1000); pd.set_option('display.max_columns', 1000); pd.set_option('display.width', 1000)

# %%
with open('file1.txt') as file:
    print("here1")

    df = pd.DataFrame()
    lines = file.readlines()
    # print(lines)
    for i in range(0, len(lines)):
        # print(line)
        line = lines[i]
        # print(line)
        if line.startswith('='):
            if str(line).strip('= ').startswith('Request'):
                # print("request")
                arr = '{"Type": "Request"'
            if str(line).strip('= ').startswith('Response'):
                # print("response")
                arr = '{"Type": "Response"'

            while lines[i+1] != '\n' and not(lines[i+1].strip() == ''):
                i = i+1
                line = lines[i].strip('\n')
                split = str(line).split(": ")
                # print(split)
                try:
                    arr += ', "' + split[0] + '":"' + split[1] + '"'
                except:
                    print("ERROR" + str(split))
                    split = str(line).split(':\t')
                    arr += ', "' + split[0] + '":"' + split[1] + '"'
            arr += '}'
            # print(arr)
            arr = json.loads(arr)
            dfnew = pd.DataFrame.from_dict(arr, orient="index")
            # dfnew = pd.pivot_table(dfnew)
            dfnew = dfnew.T
            # print("here")
            # print(dfnew)
            df = pd.concat([df, dfnew])
            # print("here2")
            # print(df)





    # print(df)
    dfrequest = df.loc[df['Type'] == 'Request']
    dfrequest['Endpoint'] = dfrequest['Endpoint'].apply(lambda x: x[5:] if x.startswith("(OWL) ") else x)
    dfrequest['Controller'] = dfrequest['Controller'].apply(lambda x: x.strip())
    dfresponse = df.loc[df['Type'] == 'Response']
    dfresponse['Endpoint'] = dfresponse['Endpoint'].apply(lambda x: x.split("(OWL) ")[1] if x.strip(" ").startswith("(") else x)
    dfresponse['Controller'] = dfresponse['Controller'].apply(lambda x: x.strip())

    dfmerged = dfrequest.merge(dfresponse, left_on=["Controller", "Endpoint"], right_on=["Controller", "Endpoint"])
    dfmerged = dfmerged.dropna(axis='columns')
    dfmerged.columns = dfmerged.columns.to_series().apply(lambda x: x.split("_")[0])

    # print(dfmerged['Controller', 'Endpoint', 'Type_x'])
    # print(dfmerged)
    dfpretty = dfmerged[['Username', 'Address', 'Red Meat', 'Grains', 'Dairy', 'Cellphone', 'TV', 'Computer', 'Car', 'Walking', 'Public Transport']]
    # print(dfmerged[['Username', 'Address', 'Red Meat', 'Grains', 'Dairy', 'Cellphone', 'TV', 'Computer', 'Car', 'Walking', 'Public Transport']])
    print(dfpretty)
    html = dfpretty.to_html()
    html = '''
    <style>
        
        table {
            font-size: 11pt; 
            font-family: Calibri;
            border-collapse: collapse; 
            border: 1px solid grey;
            background: #cee8f0;
        
        }
        
        thead th {
            background: #CBC3E3;
            text-align: center;
        }
        
        td, th {
            padding: 4px;
        }
        
        tr:nth-child(even) {
            background: #ADD8E6;
        }
        
        tr:hover {
            background: #FFFF00;
            cursor: pointer;
        }
    
        </style>
        ''' + html

    # print(dfmerged['Controller', 'Endpoint', 'Type_x'])
    # print(dfmerged)
    print(dfmerged[['Username', 'Address', 'Red Meat', 'Grains', 'Dairy', 'Cellphone', 'TV', 'Computer', 'Car', 'Walking', 'Public Transport']])

# NEW PART!!
# Function to convert to kg
def convertKg(weight):
    return round(float(weight.split()[0]) * 0.453592, 2)

# Change columns by using the conversion function
dfmerged["Red Meat"] = dfmerged["Red Meat"].apply(convertKg)
dfmerged["Grains"] = dfmerged["Grains"].apply(convertKg)
dfmerged["Dairy"] = dfmerged["Dairy"].apply(convertKg)
dfmerged["Cellphone"] = dfmerged["Cellphone"].apply(convertKg)
dfmerged["TV"] = dfmerged["TV"].apply(convertKg)
dfmerged["Computer"] = dfmerged["Computer"].apply(convertKg)
dfmerged["Car"] = dfmerged["Car"].apply(convertKg)
dfmerged["Public Transport"] = dfmerged["Public Transport"].apply(convertKg)
dfmerged["Walking"] = dfmerged["Walking"].apply(convertKg)

# Remove the word hours from data
dfmerged = dfmerged.replace(to_replace = " hours", value = "", regex = True)
dfmerged = dfmerged.replace(to_replace = " hour", value = "", regex = True)

# remove percentage sign
dfmerged['New Year Resolution'] = dfmerged['New Year Resolution'].replace(to_replace= "%", value = "", regex = True)

dfmerged['Red Meat CO2'] = dfmerged['Red Meat'].apply(lambda x: carbon.calculateCO2('red meat', x))
dfmerged['Grains CO2'] = dfmerged['Grains'].apply(lambda x: carbon.calculateCO2('Grains', x))
dfmerged['Dairy CO2'] = dfmerged['Dairy'].apply(lambda x: carbon.calculateCO2('Dairy', x))
dfmerged['Cellphone CO2'] = dfmerged['Cellphone'].apply(lambda x: carbon.calculateCO2('Cellphone', x))
dfmerged['TV CO2'] = dfmerged['TV'].apply(lambda x: carbon.calculateCO2('TV', x))
dfmerged['Computer CO2'] = dfmerged['Computer'].apply(lambda x: carbon.calculateCO2('Computer', x))
dfmerged['Car CO2'] = dfmerged['Car'].apply(lambda x: carbon.calculateCO2('Car', x))
dfmerged['Public Transport CO2'] = dfmerged['Public Transport'].apply(lambda x: carbon.calculateCO2('Public Transport', x))
dfmerged['Walking CO2'] = dfmerged['Walking'].apply(lambda x: carbon.calculateCO2('Walking', x))

dfmerged['Total'] = dfmerged['Red Meat CO2'] + dfmerged['Grains CO2'] + dfmerged['Dairy CO2'] + dfmerged['Cellphone CO2'] + dfmerged['TV CO2'] + dfmerged['Computer CO2'] + dfmerged['Car CO2'] + dfmerged['Public Transport CO2'] + dfmerged['Walking CO2']
dfmerged['Resolution Total'] = (1 - (dfmerged['New Year Resolution'].astype(float))/100) * dfmerged['Total']

print(df)

print(dfmerged)

# Convert values to float
#dfmerged[['Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Walking CO2','Public Transport CO2']] = dfmerged[['Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Walking CO2','Public Transport CO2']].astype(float)

# %%

newDf = dfmerged[['Username','Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Public Transport CO2','Walking CO2']]


fig, ax = plt.subplots()

# Create graph and set names
newDf.plot(kind='bar',ax=ax)
ax.set_xlabel('Name')
ax.set_ylabel('CO2 Amount')
ax.set_title('CO2 Amounts by Director')
ax.set_xticklabels(newDf['Username'])

#plt.show()
# Save plot
plt.xticks(rotation=90, fontsize=5)
plt.savefig('allData.png',dpi=300)

totalNewDf = dfmerged[['Username','Total','Resolution Total']]

fig, ax = plt.subplots()

totalNewDf.plot(kind='bar',ax=ax)
ax.set_xlabel('Name')
ax.set_ylabel('CO2 Amount')
ax.set_title('Total vs Resolution Total')
ax.set_xticklabels(totalNewDf['Username'])

#plt.show()
plt.xticks(rotation=90,fontsize=5)
plt.savefig('totalData.png')


html += '''<img src="allData.png" alt="First Graph"><img src="totalData.png" alt="Second Graph">'''

f = open("table.html", "w")
f.write(html)
f.close()

