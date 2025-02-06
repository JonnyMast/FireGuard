import datetime
import os

# Do not push your client ID or SECRET to github.
os.environ['MET_CLIENT_ID'] = 'YOUR MET CLIENT ID'
os.environ['MET_CLIENT_SECRET'] = 'YOUR MET CLIENT SECRET'


from frcm.frcapi import METFireRiskAPI
from frcm.datamodel.model import Location

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    frc = METFireRiskAPI()

    location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    # location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund

    # days into the past to retrieve observed weather data
    obs_delta = datetime.timedelta(days=2)

    wd = frc.get_weatherdata_now(location, obs_delta)
    print(wd)

    predictions = frc.compute_now(location, obs_delta)

    print(predictions)
