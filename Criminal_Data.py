import requests
from bs4 import BeautifulSoup as bs
import json
import traceback

base_url = 'https://ujsportal.pacourts.us/CaseSearch'

session = requests.Session()

def get_criminal_data():
    '''
    Function to fetch criminal record from Peninsula court website
    Return : A list with criminal record 
    '''
    try:
        '''
        Initital get request to the website to setup the session
        '''
        response = session.get(base_url, verify=False)  # verify=False just to avoid ssl certificate error
        initial_request_soup = bs(response.content, 'html.parser')
        try:
            '''
            Get token from website to access data
            '''
            get_token = initial_request_soup.find('div', class_='singleColumn')
            token = get_token.find('input', attrs={'name':'__RequestVerificationToken'})['value'] 
            
            '''
            Create form data with required person data to be fetched
            '''
            form_data = {
                'SearchBy': 'ParticipantName',
                'ParticipantSID': '',
                'ParticipantSSN': '',
                'FiledStartDate': '', 
                'FiledEndDate': '', 
                'County': 'York',
                'ParticipantLastName': 'smith',
                'ParticipantFirstName': 'john',
                'ParticipantDateOfBirth': '1990-12-26',
                'DocketType': 'Criminal',
                'PADriversLicenseNumber': '', 
                '__RequestVerificationToken': token,
            }

            '''
            Post request to the website with form data of the person
            '''
            try:
                criminal_data_html = session.post(base_url, data=form_data)
                criminal_data_soup = bs(criminal_data_html.content, 'html.parser')
                table_rows = criminal_data_soup.find('table', id='caseSearchResultGrid').\
                             find('tbody').find_all('tr')
                cumulative_data = []
                for row in table_rows:
                    temp_dict = {}
                    temp_dict['DocketNumber'] = row.find_all('td')[2].string
                    temp_dict['CourtType'] = row.find_all('td')[3].string
                    temp_dict['CaseCaption'] = row.find_all('td')[4].string
                    temp_dict['CaseStatus'] = row.find_all('td')[5].string
                    temp_dict['FilingDate'] = row.find_all('td')[6].string
                    temp_dict['PrimaryParticipant'] = row.find_all('td')[7].string
                    temp_dict['DateOfBirth'] = row.find_all('td')[8].string
                    temp_dict['County'] = row.find_all('td')[9].string
                    temp_dict['CourtOffice'] = row.find_all('td')[10].string
                    temp_dict['OTN'] = row.find_all('td')[11].string
                    temp_dict['Complaint'] = row.find_all('td')[12].string
                    temp_dict['Incident'] = row.find_all('td')[13].string
        
                    cumulative_data.append(temp_dict) 
                
                '''
                To print data on console
                '''
                # print(cumulative_data)  

                '''
                return required criminal cumulative_data data
                '''
                return cumulative_data


            # http status not OK
            except requests.exceptions.HTTPError as e:
                print('{}'.format(e))

        except Exception as e:
            print('Exception Occurred')
            print('{}'.format(traceback.format_exc()))

    # Connection error
    except requests.ConnectionError as e:
        print('{}'.format(e))

    # http status not OK
    except requests.exceptions.HTTPError as e:
        print('{}'.format(e))

data = get_criminal_data()
if not data:
    print('No record found')