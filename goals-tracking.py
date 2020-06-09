#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date


"""
Enable debug logging
"""
#import logging
# logging.basicConfig(level=logging.DEBUG)

today = date.today()


def main():
    client = set_user("aniketkdm@gmail.com", "ShriGanesha_17")
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

    activities = get_activities(client, 0, 1)

    i = 0
    for activity in activities:
        i += 1
        print("activity "+str(i)+":"+str(activity))


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


def get_activities(client, start, end):
    """
    Get activities data
    """
    try:
        activities = client.get_activities(start, end)  # 0=start, 1=limit
        """print(activities)"""
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


if __name__ == "__main__":
    main()
