#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date
from os import getenv
import datetime

"""
Enable debug logging
"""
# import logging
# logging.basicConfig(level=logging.DEBUG)

today = date.today()


def main():
    try:
        client = getCreds()
    except (
        EnvironmentError
    ) as err:
        print("Error during setting up connection: %s" % err)
        quit()

    """
    Login to Garmin Connect portal
    Only needed at start of your program
    The library will try to relogin when session expires
    """
    try:
        client.login()
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occurred during Garmin Connect Client login: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occurred during Garmin Connect Client login")
        quit()

    mondayThisWeek = datetime.datetime.today(
    ) - datetime.timedelta(days=datetime.datetime.today().weekday() % 7)

    activities = get_activities_by_date(client, str(mondayThisWeek))

    # print(type(activities)) # list[dict]
    m = dict()
    i = 0
    for activity in activities:
        i += 1
        # print("activity "+str(i)+":"+str(activity["activityName"]))
        exercise = activity["activityName"]
        if exercise in m:
            m[exercise] = m[exercise] + 1
        else:
            m[exercise] = 1
        # print(type(activity)) # dict
    print(m)


def set_user(email, password):
    try:
        client = Garmin(email, password)
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occurred during Garmin Connect Client init: %s" % err)
        return err
    except Exception:  # pylint: disable=broad-except
        print("Unknown error occurred during Garmin Connect Client init")
        return
    return client


# date format is yyyy-mm-dd
def get_activities_by_date(client, date):
    """
    Get activities data
    """
    try:
        activities = client.get_activities_by_date(date)
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print("Error occurred during Garmin Connect Client get activities: %s" % err)
        quit()
    except Exception:  # pylint: disable=broad-except
        print(
            "Unknown error occurred during Garmin Connect Client get activities: %s" % err)
        quit()
    return activities


def getCreds():
    if getenv("EMAIL") == None or getenv("PASSWORD") == None:
        raise EnvironmentError("EMAIL and PASSWORD expected as ENV variables")

    u = getenv("EMAIL")
    p = getenv("PASSWORD")

    return set_user(u, p)


if __name__ == "__main__":
    main()
