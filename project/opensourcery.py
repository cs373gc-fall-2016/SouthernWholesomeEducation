import requests
from requests.adapters import HTTPAdapter
from models import *
import json


def api_call():
    # setting up url to collect all school codes
    projects_url = 'http://opensourcery.me/api/projects/?start=0&end=4' # 0-6676
    companies_url = 'http://opensourcery.me/api/companies/?start=0&end=3' # 0-299
    contributors_url = 'http://opensourcery.me/api/contributors/?start=0&end=10' #0-35420
    languages_url = 'http://opensourcery.me/api/languages/?start=0&end=10' # 0-95

    
    projects = setup_projects(projects_url)
    print('finished projects')
    companies = setup_companies(companies_url)
    print('finished companies')
    contributors = setup_contributors(contributors_url)
    print('finished contributors')
    languages = setup_languages(languages_url)
    print('finished languages')

    print('starting lists')
    final_list = []
    final_list.extend(projects)
    final_list.extend(companies)
    final_list.extend(contributors)
    final_list.extend(languages)
    print('finised lists')

    print(final_list)
    print('#########################################################')

    name_list = list()
    for item in final_list:
        name_list.append(item['name'])

    
    for item_list in final_list:
        imports_list = item_list['imports']
        temp_list = []
        # print(imports_list)
        for individual_item in imports_list:
            if individual_item in name_list:
                temp_list.append(individual_item)
        item_list['imports'] = temp_list


    print(final_list)
    print('#########################################################')

    with open('flare-import.json', 'w') as fout:
        json.dump(final_list, fout)


def setup_projects(url):
    temp_projects = []
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            temp_dict = dict()
            temp_list_contrib = list()
            project_id = temp_json[item]['id']
            temp_proj_id = 'p' + str(project_id)
            for contrib in temp_json[item]['contributor_ids']:
                temp_val = 'c' + str(contrib)
                temp_list_contrib.append(temp_val)
            for language in temp_json[item]['language_ids']:
                temp_val = 'l' + str(language)
                temp_list_contrib.append(temp_val)
            temp_dict['name'] = temp_proj_id
            temp_dict['imports'] = temp_list_contrib
            temp_projects.append(temp_dict)
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name
    return temp_projects



def setup_companies(url):
    temp_projects = []
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            temp_dict = dict()
            temp_list_contrib = list()
            project_id = temp_json[item]['id']
            temp_proj_id = 'i' + str(project_id) # c was used i for "inc."
            for project in temp_json[item]['project_ids']:
                temp_val = 'p' + str(project)
                temp_list_contrib.append(temp_val)
            temp_dict['name'] = temp_proj_id
            temp_dict['imports'] = temp_list_contrib
            temp_projects.append(temp_dict)
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name
    return temp_projects



def setup_contributors(url):
    temp_projects = []
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            temp_dict = dict()
            temp_list_contrib = list()
            project_id = temp_json[item]['id']
            temp_proj_id = 'c' + str(project_id)
            for project in temp_json[item]['project_ids']:
                temp_val = 'p' + str(project)
                temp_list_contrib.append(temp_val)
            temp_dict['name'] = temp_proj_id
            temp_dict['imports'] = temp_list_contrib
            temp_projects.append(temp_dict)
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name
    return temp_projects



def setup_languages(url):
    temp_projects = []
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            temp_dict = dict()
            temp_list_contrib = list()
            project_id = temp_json[item]['id']
            temp_proj_id = 'l' + str(project_id)
            for project in temp_json[item]['project_ids']:
                temp_val = 'p' + str(project)
                temp_list_contrib.append(temp_val)
            temp_dict['name'] = temp_proj_id
            temp_dict['imports'] = temp_list_contrib
            temp_projects.append(temp_dict)
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name
    return temp_projects


if __name__ == '__main__':
    api_call()