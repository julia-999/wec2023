import pandas as pd
import matplotlib.pyplot as plt

# Sample data frame
df = pd.DataFrame({'Red Meat': ['100 pounds', '89 pounds', '75 pounds'],
                   'Grains': ['2 pounds', '167 pounds', '98 pounds'],
                   'Dairy': ['200 pounds', '42 pounds', '135 pounds'],
                   'Cellphone': ['55 hours', '42 hours', '75 hours'],
                   'TV': ['43 hours', '75 hours', '88 hours'],
                   'Computer': ['130 hours', '88 hours', '102 hours'],
                   })

# Function to convert to kg
def convertKg(weight):
    return round(float(weight.split()[0]) * 0.453592, 2)

# Change columns by using the conversion function
df["Red Meat"] = df["Red Meat"].apply(convertKg)
df["Grains"] = df["Grains"].apply(convertKg)
df["Dairy"] = df["Dairy"].apply(convertKg)

# Remove the word hours from data
df = df.replace(to_replace = " hours", value = "", regex = True)

# Convert numerical values to float
df[['Red Meat','Grains','Dairy','Cellphone','TV','Computer']] = df[['Red Meat','Grains','Dairy','Cellphone','TV','Computer']].astype(float)

print(df)


food_df = df[['Red Meat','Grains','Dairy']]
electronics_df = df[['Cellphone','TV','Computer']]

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



