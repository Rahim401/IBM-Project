import pandas as pd
from pandas import read_csv
import matplotlib.pyplot as plt
from datetime import datetime

pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

dataFile = "space_missions.csv"

missionDataFrame = read_csv("space_missions.csv",encoding='ISO-8859-1')
missionDataFrame["Year"] = pd.to_datetime(missionDataFrame['Date']).dt.year


def plotMissionsStatus(dataFrame, ofCompany=None):
    if ofCompany is not None:
        dataFrame = dataFrame[dataFrame["Company"] == ofCompany]
        title = f"Success Rate of {ofCompany} Launches"
    else: title = f"Success Rate of Launches WorldWide"
    dataFrame = dataFrame.groupby(['Year','MissionStatus']).size().reset_index(name='LaunchCount')
    pivot = dataFrame.pivot(index='Year', columns='MissionStatus', values='LaunchCount').fillna(0)

    pivot.plot(stacked=True)
    plt.title(title); plt.xlabel('Year'); plt.ylabel('Launch Count')
    plt.legend(title='Mission Status', loc='upper left')
    plt.show()

def plotLaunchVehicle(dataFrame, ofCompany=None, capAmount=20):
    if ofCompany is not None:
        dataFrame = dataFrame[dataFrame["Company"] == ofCompany]
        title = f"Launch Vehicles used by {ofCompany}"
    else: title = f"Launch Vehicles Mostly used"

    topVehicles = dataFrame['Rocket'].value_counts().nlargest(capAmount).index
    dataFrame = dataFrame[dataFrame['Rocket'].isin(topVehicles)]

    dataFrame = dataFrame.groupby(['Year','Rocket']).size().reset_index(name='VehicleUsed')
    pivot = dataFrame.pivot(index='Year', columns='Rocket', values='VehicleUsed').fillna(0)

    pivot.plot(stacked=True)
    plt.title(title); plt.xlabel('Year'); plt.ylabel('Vehicle Used Count')
    plt.legend(title='Launch Vehicles', loc='upper left')
    plt.show()

def plotActiveMission(dataFrame, ofCompany=None, capAmount=20):
    if ofCompany is not None:
        dataFrame = dataFrame[dataFrame["Company"] == ofCompany]
        title = f"{capAmount} Oldest Active missions from {ofCompany}"
    else: title = f"{capAmount} Oldest Active missions WorldWide"

    current_date = datetime.now()
    dataFrame = dataFrame[dataFrame['RocketStatus']=="Active"]
    dataFrame['MissionAge'] = (current_date - pd.to_datetime(missionDataFrame['Date'])).dt.days / 365
    dataFrame = dataFrame.sort_values(by='MissionAge', ascending=False).head(capAmount)[::-1]

    plt.figure(figsize=(10, 6))
    plt.barh(dataFrame['Mission'], dataFrame['MissionAge'], color='green')
    plt.title(title)
    plt.xlabel('Mission Age (Years)')
    plt.ylabel('Mission')
    plt.show()


plotMissionsStatus(missionDataFrame, "SpaceX")
plotLaunchVehicle(missionDataFrame)
plotActiveMission(missionDataFrame, "ISRO",capAmount=10)