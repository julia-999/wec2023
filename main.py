
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

dfmerged['Red Meat CO2'] = dfmerged['Red Meat'].apply(lambda x: carbon.calculateCO2('red meat', x))
dfmerged['Grains CO2'] = dfmerged['Grains'].apply(lambda x: carbon.calculateCO2('Grains', x))
dfmerged['Dairy CO2'] = dfmerged['Dairy'].apply(lambda x: carbon.calculateCO2('Dairy', x))
dfmerged['Cellphone CO2'] = dfmerged['Cellphone'].apply(lambda x: carbon.calculateCO2('Cellphone', x))
dfmerged['TV CO2'] = dfmerged['TV'].apply(lambda x: carbon.calculateCO2('TV', x))
dfmerged['Computer CO2'] = dfmerged['Computer'].apply(lambda x: carbon.calculateCO2('Computer', x))
dfmerged['Car CO2'] = dfmerged['Car'].apply(lambda x: carbon.calculateCO2('Car', x))
dfmerged['Public Transport CO2'] = dfmerged['Public Transport'].apply(lambda x: carbon.calculateCO2('Public Transport', x))
dfmerged['Walking CO2'] = dfmerged['Walking'].apply(lambda x: carbon.calculateCO2('Walking', x))
print(df)

print(dfmerged)

# Convert values to float
#dfmerged[['Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Walking CO2','Public Transport CO2']] = dfmerged[['Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Walking CO2','Public Transport CO2']].astype(float)

# %%

# STACKED BAR GRAPH
#fig, ax = plt.subplots()

#ax.bar(dfmerged['Username'], dfmerged['Red Meat CO2'], label='Red Meat')
#ax.bar(dfmerged['Username'], dfmerged['Grains CO2'], label='Grains', bottom=dfmerged['Red Meat CO2'])
#ax.bar(dfmerged['Username'], dfmerged['Dairy CO2'], label='Dairy')
#ax.bar(dfmerged['Username'], dfmerged['Cellphone CO2'], label='Cellphone')
#ax.bar(dfmerged['Username'], dfmerged['TV CO2'], label='TV')
#ax.bar(dfmerged['Username'], dfmerged['Computer CO2'], label='Computer')
#ax.bar(dfmerged['Username'], dfmerged['Car CO2'], label='Car')
#ax.bar(dfmerged['Username'], dfmerged['Walking CO2'], label='Walking')
#ax.bar(dfmerged['Username'], dfmerged['Public Transport CO2'], label='Public Transport')

#ax.set_ylabel('Amount of CO2')
#ax.set_title('CO2 by Director')
#ax.legend()

#plt.xticks(rotation=80)
#plt.ylim(0, 500)

#plt.show()

newDf = dfmerged[['Username','Red Meat CO2','Grains CO2','Dairy CO2','Cellphone CO2','TV CO2','Computer CO2','Car CO2','Public Transport CO2','Walking CO2']]


fig, ax = plt.subplots()

newDf.plot(kind='bar',ax=ax)
ax.set_xlabel('Name')
ax.set_ylabel('Weight')
ax.set_title('Weight of food items')
ax.set_xticklabels(newDf['Username'])

plt.show()


plt.bar(dfmerged['Username'],dfmerged['Red Meat CO2'])
plt.xlabel('Name')
plt.ylabel('Total CO2')
plt.title('Total CO2 by Director')
plt.xticks(rotation=80)

plt.show()

