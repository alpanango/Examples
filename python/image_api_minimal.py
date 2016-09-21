#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import requests

ip = "api.peat-cloud.com"
version = "v1"
route = "image_analysis"
url = "http://%s/%s/%s" % (ip, version, route)


def main():
    # Header of our requst. Replace <YOUR_API_KEY> with your api key.
    headers = {"api_key": "<YOUR_API_KEY>", "variety": "TOMATO"}

    # make a dict with the picture
    image = "data/tomato_nutrient/iron1.jpg"
    files = {"picture": open(image, "rb")}

    # post both files to our API
    result = requests.get(url, files=files, headers=headers, timeout=10)

    if result.status_code == 401:
        print "Authentication failed"
    elif result.status_code == 500:
        print "Internal server error..."
    elif result.status_code == 200:
        # load response that comes in JSON format and print the result
        json_data = result.json()
        for data in json_data["image_analysis"]:
            print "Disease name: %s\n\tProbability: %s%%" % (data["name"], data["similarity"])
    print ""
    return


def batch_processing(directory):
    '''
    this example is a bit more sophisticated than the simple "main" function,
    it needs a base folder as argument
    and will iterate over every image in all subfolders of this directory
    '''

    # define a header
    headers = {"api_key": "<YOUR_API_KEY>", "variety": "TOMATO"}

    # get a list of all the subfolders
    folderlist = [x[0] for x in os.walk(directory)]

    # iterate over all folder in a given directory
    for folder in folderlist:
        filelist = [i for i in os.listdir(folder) if i.endswith(".jpg")]
        for f in filelist:
            filepath = os.path.join(folder, f)
            files = {"picture": open(filepath, "rb")}
            result = requests.get(url, files=files, headers=headers, timeout=10)
            json_data = result.json()
            
            #just printing
            print "filename:", f
            print "input from folder:", folder
            print "image API result:", json_data["image_analysis"][0]["name"], \
                  json_data["image_analysis"][0]["similarity"], "\n"
    return


if __name__ == "__main__":
    main()
    batch_processing("data")
