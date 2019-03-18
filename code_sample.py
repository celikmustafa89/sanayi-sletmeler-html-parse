#!/usr/bin/python

import json
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


totalLines = 0
totalTime = 0
firstEntryTime = 999999999999999
lastEntryTime = 0
maxTime = 0
minTime = 99999999

durations = {
    "lt100": 0,
    "lt200": 0,
    "lt300": 0,
    "lt400": 0,
    "lt500": 0,
    "ge500": 0,
}

nodeDurations = {
    "Initial": [0, 0],
    "Giris_Kontrolleri": [0, 0],
    "UpsellLimit": [0, 0],
    "Upsell": [0, 0],
    "ChurnStratejisi": [0, 0],
    "dbkStratejisi": [0, 0],
    "KurumsalStrateji": [0, 0],
    "Offer_Exclusion": [0, 0],
    "Downsell_Engelleme": [0, 0],
    "Sorting": [0, 0],
    "Offer_Consistency": [0, 0],
    "Final": [0, 0],

}

file = sys.argv[1]
with open(file) as inputFile:
    for line in inputFile:
        data = json.loads(line)
        startTime = data["startTimestamp"]
        endTime = data["endTimestamp"]
        if firstEntryTime > startTime:
            firstEntryTime = startTime
        if lastEntryTime < endTime:
            lastEntryTime = endTime
        duration = endTime - startTime
        if duration < 0:
            print("Time spent is negative for __EVENT_ID__ skipping")
            continue
        if duration < 100:
            durations["lt100"] = durations["lt100"] + 1
        elif duration < 200:
            durations["lt200"] = durations["lt200"] + 1
        elif duration < 300:
            durations["lt300"] = durations["lt300"] + 1
        elif duration < 400:
            durations["lt400"] = durations["lt400"] + 1
        elif duration < 500:
            durations["lt500"] = durations["lt500"] + 1
        elif duration >= 500:
            durations["ge500"] = durations["ge500"] + 1
            for key in nodeDurations:
                for node in data["nodeLogs"]:
                    if node["name"] == key:
                        try:
                            perNodeDuration = node["endTimestamp"] - node["startTimestamp"]
                            if perNodeDuration < 0:
                                print("Time spent per node is negative for __EVENT_ID__ " + key + " skipping")
                                continue
                            nodeDurations[key][1] = nodeDurations[key][1] + perNodeDuration
                            nodeDurations[key][0] = nodeDurations[key][0] + 1
                            # now fill the action times
                            try:
                                for actionNode in node["actionLogs"]:
                                    try:
                                        if actionNode["endTimestamp"] - actionNode["startTimestamp"] < 0:
                                            print("Time spent per node is negative for __EVENT_ID__ " + key + "->" +
                                                  actionNode["actionName"] + " skipping")
                                            continue
                                        if actionNode["actionName"] in nodeDurations[key][2]:
                                            #											print("current duration for " + actionNode["actionName"] + " is " + str(nodeDurations[key][2][actionNode["actionName"]]) +" end: " + str(actionNode["endTimestamp"]) + " start: " + str(actionNode["startTimestamp"]) + " with event id "  + data["eventParameters"]["_eventId"] )
                                            nodeDurations[key][2][actionNode["actionName"]] = nodeDurations[key][2][
                                                                                                  actionNode[
                                                                                                      "actionName"]] + \
                                                                                              actionNode[
                                                                                                  "endTimestamp"] - \
                                                                                              actionNode[
                                                                                                  "startTimestamp"]
                                        #											print("current duration for " + actionNode["actionName"] + " is " + str(nodeDurations[key][2][actionNode["actionName"]]) +" with event id " + data["eventParameters"]["_eventId"] + "set by addition" )

                                        else:
                                            nodeDurations[key][2][actionNode["actionName"]] = actionNode[
                                                                                                  "endTimestamp"] - \
                                                                                              actionNode[
                                                                                                  "startTimestamp"]
                                    #											print("current duration for " + actionNode["actionName"] + " is " + str(nodeDurations[key][2][actionNode["actionName"]]) +" with event id " + data["eventParameters"]["_eventId"] + "set by first" )
                                    except Exception as ex:
                                        template = "While adding action time for " + actionNode[
                                            "actionName"] + " an exception of type {0} occurred. Arguments:\n{1!r}"
                                        message = template.format(type(ex).__name__, ex.args)
                                        #										print message
                                        nodeDurations[key].append({actionNode["actionName"]: actionNode[
                                                                                                 "endTimestamp"] -
                                                                                             actionNode[
                                                                                                 "startTimestamp"]})
                            #										print("current duration for " + actionNode["actionName"] + " is " + str(nodeDurations[key][2][actionNode["actionName"]]) +" with event id " + data["eventParameters"]["_eventId"] + "set by exception" )

                            except Exception as ex:
                                template = "While action log check an exception of type {0} occurred. Arguments:\n{1!r}"
                                message = template.format(type(ex).__name__, ex.args)
                                print
                                message
                        except:
                            print("Exception while checking node")
                        break

        if duration > maxTime:
            maxTime = duration
        if duration < minTime:
            minTime = duration
        totalLines = totalLines + 1
        totalTime = totalTime + duration

print("total time: " + str(totalTime) + " while real time was: " + str(
    lastEntryTime - firstEntryTime) + " Average response time: " + str(totalTime / totalLines))
print("Buckets: less then 100:" + str(durations["lt100"]) + " between 100 and 200: " + str(
    durations["lt200"]) + " between 200 and 300: " + str(durations["lt300"]) + " between 300 and 400: " + str(
    durations["lt400"]) + " between 400 and 500: " + str(durations["lt500"]) + " more than 500: " + str(
    durations["ge500"]))
print("Minimum time: " + str(minTime) + ", maximum time: " + str(maxTime))
print("")
print("Per node durations for longer than 500 responses")
for key in nodeDurations:
    try:
        print(bcolors.WARNING + str(key).rjust(25) + " total: " + str(nodeDurations[key][1]).rjust(
            5) + ", run count: " + str(nodeDurations[key][0]).rjust(5) + ", average:" + str(
            nodeDurations[key][1] / nodeDurations[key][0]).rjust(9) + bcolors.ENDC)
        try:
            if len(nodeDurations[key]) == 2:
                print(bcolors.FAIL + ("No action found in node " + key).rjust(60) + bcolors.ENDC)
            else:
                for action in nodeDurations[key][2]:
                    try:
                        print((action).rjust(50) + " took total of :" + str(nodeDurations[key][2][action]).rjust(
                            9) + " and average " + str(nodeDurations[key][2][action] / nodeDurations[key][0]).rjust(4))
                    except Exception as ex:
                        template = "While printing action information of " + action + " an exception of type {0} occurred. Arguments:\n{1!r}"
                        message = template.format(type(ex).__name__, ex.args)
                        print
                        message
        except Exception as ex:
            template = "While printing action information an exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print
            message
    except:
        print(key + " didn't have information. Possible Json issue")