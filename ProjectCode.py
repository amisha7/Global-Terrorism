#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 20:37:30 2024

@author: patel
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("/Users/patel/Documents/3.Winter2023/599-Research/globalterrorismdb.csv", encoding='ISO-8859-1')



df.isnull().sum()
# Drop columns with too many missing values
data_new = df.dropna(thresh=160000,axis=1)

data_new.duplicated()
#We observe that there are no duplicate values, but still to be on safer side we drop the duplicates, given the fact that number of features and rows are extensive

data_new.drop_duplicates()


# Drop rows with missing target values (e.g., rows without information on attacks)
data_new = data_new.dropna(subset=["nkill"])

data_new


# ######  1. Some basic analysis
data_new['casualities']=data_new['nkill']+data_new['nwound']

print('Country with Highest Terrorist Attacks:',data_new['country_txt'].value_counts().index[0])
print('Regions with Highest Terrorist Attacks:',data_new['region_txt'].value_counts().index[0])
print('Maximum people killed in an attack are:',data_new['nkill'].max(),'that took place in',data_new.loc[data_new['nkill'].idxmax()].country_txt)
print("Year with the most attacks:",data_new['iyear'].value_counts().idxmax())
print("Month with the most attacks:",data_new['imonth'].value_counts().idxmax())
print("Most Attack Types:",data_new['attacktype1_txt'].value_counts().idxmax())


##########   2.  Terrorist Groups with most attacks¶
plt.figure(figsize=(10, 10))  # Increase figure size

# Group and sort data
top_groups = data_new.groupby("gname")["nkill"].sum().nlargest(10)
top_groups = top_groups.reset_index()

# Define colors
colors = sns.color_palette("pastel")[0:len(top_groups)]

# Create a pie chart
pie, texts, autotexts = plt.pie(top_groups["nkill"], labels=top_groups["gname"], colors=colors, autopct='%1.1f%%', startangle=140)

# Set title with bold font and increased font size
plt.title("Total Killings by Groups in Percentage", pad=20, fontweight='bold', fontsize=16)

# Adjust labels
for text in texts:
    text.set_fontsize(12)  # Adjust font size
for autotext in autotexts:
    autotext.set_fontsize(12)  # Adjust font size

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# Show the plot
plt.show()




#########  3. Countries with highest terrorist attacks
print(f"The highest terrorist attacks were commited in {data_new.country_txt.value_counts().index[0]} with {data_new.country.value_counts().max()} attacks")

print('\nThe other 9 countries with highest terrorist attacks are:')
for i in range(1,10):
    print(f"{i+1}. {data_new.country_txt.value_counts().index[i]} with {data_new.country_txt.value_counts()[i]} attacks")

#Visualization
plt.subplots(figsize=(15,6))
sns.barplot(x=data_new['country_txt'].value_counts()[:10].index,y=data_new['country_txt'].value_counts()[:10].values,palette='Set1')
plt.title('Top Countries Affected')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation= 90)
plt.show()



########### 4. Total killing by year
# Attacks by Year
plt.figure(figsize=(18, 6))
attacks_by_year = df.groupby("iyear")["nkill"].sum()
plt.plot(attacks_by_year.index, attacks_by_year.values, marker="o")
plt.title("Total Killings by Year")
plt.xlabel("Year")
plt.ylabel("Total Killings")
plt.grid(True)

# Set x-axis labels to display every 5 years
plt.xticks(range(1970, 2023, 5))  # Adjust the range as needed

plt.show()

######## 5. Killing by attack type
plt.figure(figsize=(12, 6))
attacks_by_attack_type = data_new.groupby("attacktype1_txt")["nkill"].sum().sort_values(ascending=False)
sns.barplot(x=attacks_by_attack_type.values, y=attacks_by_attack_type.index)
plt.title("Total Killings by Attack Type")
plt.xlabel("Total Killings")
plt.ylabel("Attack Type")
plt.show()


#Most number of killings were due to Bombing/Explosion and Armed Assualt.

###### 6. Killing by target Type
plt.figure(figsize=(12, 6))
attacks_by_target_type = data_new.groupby("targtype1_txt")["nkill"].sum().sort_values(ascending=False)
sns.barplot(x=attacks_by_target_type.values, y=attacks_by_target_type.index)
plt.title("Total Killings by Target Type")
plt.xlabel("Total Killings")
plt.ylabel("Target Type")
plt.show()
# Majority of the deaths were observed when the target was citizens of the country, specific property, military or the police.



#######  7. Terrorist Activities by Region each Year¶
reg=pd.crosstab(data_new.iyear,data_new.region_txt)
reg.head()
reg.plot(kind="area", stacked=False, alpha=0.5,figsize=(20,10))
plt.title("Region wise attacks",fontsize=20)
plt.xlabel("Years",fontsize=20)
plt.ylabel("Number of Attacks",fontsize=20)
plt.show()

######  8. Number Of Casualities Each Year
plt.subplots(figsize=(10,7))
year_casual = data_new.groupby('iyear').casualities.sum().to_frame().reset_index()
year_casual.columns = ['Year','Casualities']
plt.title('Number Of Casualities Each Year')
sns.lineplot(x='Year', y='Casualities', data=year_casual,palette="Set2",color="g")
# Set x-axis labels to display every 5 years
plt.xticks(range(1970, 2023, 5))  # Adjust the range as needed

plt.show()




#### 9. Attacks vs Killed

coun_terror=data_new['country_txt'].value_counts()[:15].to_frame()
coun_terror.columns=['Attacks']
coun_kill=data_new.groupby('country_txt')['nkill'].sum().to_frame()
coun_terror.merge(coun_kill,left_index=True,right_index=True,how='left').plot.bar(width=0.9)
fig=plt.gcf()
fig.set_size_inches(18,6)
plt.show()

#### 10. Success rate of terrorist attacks

noa = data_new.groupby('iyear').size().reset_index(name='count')
sum_of_attacks = noa['count'].sum()
succ = data_new.groupby(['success']).size().reset_index(name='count')
succ['percentage'] =  succ['count']/sum_of_attacks *100
sns.barplot(x = 'success', y = 'percentage', data=succ)
plt.title("Outcome of Terrorist Attacks over the World")
plt.xlabel("Outcome")
## Of all the 181691 attacks 89% were successful, while 11% was unsuccessful.




