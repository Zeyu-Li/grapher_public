''''
Google Sheets Script for summarizing sheets documents
Description: This is a script summarize and plot a graph from a lot of schedule files

Note: most of code is from following Google's poorly documented documentation
* https://developers.google.com/drive
* https://developers.google.com/sheets/api

ALso, using gspread; documentation bellow:
* https://gspread.readthedocs.io/en/latest/
'''

# imports google stuff
from __future__ import print_function
import datetime
import pickle
import os.path
import os, winshell
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pprint
import json

def main():
    ''' main function
    '''


    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets.readonly','https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    # builds service interaction
    service = pickler(SCOPES)

    # inits top folder/dir
    top_folder_id = 'wf2ny4we'
    # the single template non-use sheet so it is not included in summary
    template ='y3ny4we'
    file_ids= []
    
    # if data exists, take the previous data and add to that 
    # otherswise, create array of 0s
    try:
        with open('data.json', 'r') as fp:
            data_set = json.load(fp)
    except:
        data_set = list(0 for i in range(len(categories)))


    # gets all files in folder
    folders = print_files_in_folder(service, top_folder_id)

    # get all Google sheets files
    # this is to extact a structure that is displayed below
    # top_folder_id
    #   ↳ template - will not be included
    #   ↳ April
    #       ↳19th-25th
    #       ↳25th-31st
    #   ↳ May
    #       ↳10th-15th
    #       15th-20th etc.
    for folder in folders:
        if folder != template:
            files = print_files_in_folder(service, folder)
            for file_id in files:
                file_ids.append(file_id)

    # gets data from all worksheets in Google Sheets file
    data = sheets(file_ids, SCOPES)


    # formate data so it is a list of numbers 
    # which each number is a # of hours in category
    for w in range(len(data[0])):
        column = 0
        for h in range(len(data)):
            column += float(data[h][w].value)

        data_set[w] += column


    # open data.json and write to it
    with open('data.json', 'w') as fp:
        json.dump(data_set, fp)

    return 0


def sheets(file_ids, SCOPES):
    ''' for every sheet, pull data out '''

    # inits 
    data = []

    # inits creds and authorization
    credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets.json', SCOPES)
    gc = gspread.authorize(credentials)

    for index, file_id in enumerate(file_ids):

        # if first, most recent file, skip b/c it is still being edited
        if index == 0:
            continue

        # do these in batches 
        # b/c Google API requests are 500 requests/ 100 seconds
        # if index > 10:
        #     break

        if index <= 20:
            if index > 30:
                break
            continue

        sh = gc.open_by_key(file_id)
        worksheet_list = sh.worksheets()
        for worksheet in worksheet_list:
            # change range so you pull data from different cells
            # *Note the 500 requests/ 100 seconds limit for Google API
            data.append(worksheet.range('L9:L17'))


    return data


def print_files_in_folder(service, folder_id):
    '''returns all files belonging to a folder.

    Args:
        service: Drive API service instance.
        folder_id: ID of the folder to print files from.
    '''

    files = []
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = service.children().list(
                folderId=folder_id, **param).execute()

            for child in children.get('items', []):
                files.append(child['id'])
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except:
            print('An error occurred: %s' % error)
            break

    return files


def pickler(SCOPES):
    ''' Google's pickle, No Comment '''

    creds = None
    '''The file token.pickle stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    '''
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v2', credentials=creds)

# main function call
if __name__ == '__main__':
    main()
