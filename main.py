
# %%
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

dfmerged['Red Meat C02'] = dfmerged['Red Meat'].apply(lambda x: carbon.calculateCO2('red meat', x))
dfmerged['Grains C02'] = dfmerged['Grains'].apply(lambda x: carbon.calculateCO2('Grains', x))
dfmerged['Dairy C02'] = dfmerged['Dairy'].apply(lambda x: carbon.calculateCO2('Dairy', x))
dfmerged['Cellphone C02'] = dfmerged['Cellphone'].apply(lambda x: carbon.calculateCO2('Cellphone', x))
dfmerged['TV C02'] = dfmerged['TV'].apply(lambda x: carbon.calculateCO2('TV', x))
dfmerged['Computer C02'] = dfmerged['Computer'].apply(lambda x: carbon.calculateCO2('Computer', x))
dfmerged['Car C02'] = dfmerged['Car'].apply(lambda x: carbon.calculateCO2('Car', x))
dfmerged['Public Transport C02'] = dfmerged['Public Transport'].apply(lambda x: carbon.calculateCO2('Public Transport', x))
dfmerged['Walking C02'] = dfmerged['Walking'].apply(lambda x: carbon.calculateCO2('Walking', x))
print(df)

print(dfmerged)

# Convert numerical values to float
dfmerged[['Red Meat','Grains','Dairy','Cellphone','TV','Computer']] = dfmerged[['Red Meat','Grains','Dairy','Cellphone','TV','Computer']].astype(float)

# %%

food_df = dfmerged[['Red Meat','Grains','Dairy']]
electronics_df = dfmerged[['Cellphone','TV','Computer']]

# Create two subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))

# Plot the food data
food_df.plot(kind='bar',ax=axs[0])
axs[0].set_xlabel('Index')
axs[0].set_ylabel('Weight')
axs[0].set_title('Weight of food items')

# Plot the electronics data
electronics_df.plot(kind='bar',ax=axs[1])
axs[1].set_xlabel('Index')
axs[1].set_ylabel('Usage')
axs[1].set_title('Usage of electronic devices')

plt.show()
