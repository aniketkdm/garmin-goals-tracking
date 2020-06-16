#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date
from os import getenv


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

    activities = get_activities_by_date(client, '2020-06-09')

    print(type(activities))

    i = 0
    for activity in activities:
        i += 1
        print("activity "+str(i)+":"+str(activity["activityName"]))
        print(type(activity))


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
        print("Unknown error occurred during Garmin Connect Client get activities")
        quit()
    return activities


def getCreds():
    print("email: %s, password: %s", getenv("EMAIL"), getenv("PASSWORD"))
    if getenv("EMAIL") == None or getenv("PASSWORD") == None:
        raise EnvironmentError("EMAIL and PASSWORD expected as ENV variables")

    u = getenv("EMAIL")
    p = getenv("PASSWORD")

    print("email: %s, password: %s", u, p)

    return set_user(u, p)


if __name__ == "__main__":
    main()
