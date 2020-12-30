#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : Request LinkedIn's API to retrieve JSON data of the given URL

import requests
import pprint
import csv
import json

from config.config import *
posts = []

with requests.session() as session:
    session.cookies['li_at'] = LI_ACCESS_TOKEN
    session.cookies["JSESSIONID"] = LI_CSRF_TOKEN
    session.headers = LI_REQUEST_HEADER
    session.headers["csrf-token"] = session.cookies["JSESSIONID"].strip('"')
    response = session.get(LI_REQUEST_URL).json()
    response_elements = response['elements']
    for element in response_elements:
        SOCIAL_DETAIL_URL = LI_SOCIAL_DETAIL_URL + element['updateMetadata']['urn']
        print(SOCIAL_DETAIL_URL)
        social_detail_response = session.get(SOCIAL_DETAIL_URL).json()
        if social_detail_response.get('status') is None:
            post = {
                'URN': "https://www.linkedin.com/feed/update/" + element['updateMetadata']['urn'],
                'DATE': str(social_detail_response['createdOn']['day']) + '/' + str(social_detail_response['createdOn']['month']) + '/' + str(social_detail_response['createdOn']['year']),
                'LIKES': social_detail_response['totalSocialActivityCounts']['numLikes'],
                'VIEWS': social_detail_response['totalSocialActivityCounts']['numViews'],
                'SHARES': social_detail_response['totalSocialActivityCounts']['numShares'],
                'COMMENTS': social_detail_response['totalSocialActivityCounts']['numComments'],
            }
            posts.append(post)

data_file = open('logs/linkedin-social-detail.csv', 'w')
csv_writer = csv.writer(data_file)
count = 0
for post in posts:
    if count == 0:

        # Writing headers of CSV file
        header = post.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(post.values())

data_file.close()
