import requests
from requests.adapters import HTTPAdapter
from models import *
import json

# global variables containing id to name mappings
contributors_mapping = dict()
language_mapping = dict()
project_mapping = dict()


def api_call():
    # setting up url to collect all school codes
    projects_url = 'http://opensourcery.me/api/projects/?start=0&end=20' # 0-6676 is max
    companies_url = 'http://opensourcery.me/api/companies/?start=0&end=4' # 0-299 is max
    contributors_url = 'http://opensourcery.me/api/contributors/?start=0&end=20' #0-35420 is max
    languages_url = 'http://opensourcery.me/api/languages/?start=0&end=20' # 0-95 is max

    projects = setup_projects(projects_url)
    get_project_names()
    print('finished projects')
    companies = setup_companies(companies_url)
    print('finished companies')
    contributors = setup_contributors(contributors_url)
    get_contributor_names()
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


    for item in final_list:
        # add the contributor names instead of id
        if item['target'][0] == 'c':
            try:
                item['target'] = contributors_mapping[item['target']]
            except KeyError:
                pass # missing contributor
        # add the language names instead of id
        if item['target'][0] == 'l':
            try:
                item['target'] = language_mapping[item['target']]
            except KeyError:
                pass # missing language
        # add the project names instead of id
        if item['target'][0] == 'p':
            try:
                item['target'] = project_mapping[item['target']]
            except KeyError:
                pass # missing language

    print(final_list)
    print('#########################################################')


    # with open('flare-import.json', 'w') as fout:
    #     json.dump(final_list, fout)


def setup_projects(url):
    temp_projects = []
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            # [{source: "projects", target: "Contributors", type: "licensing"}, ...]
            temp_dict = dict()
            temp_dict['source'] = temp_json[item]['name']
            for indv_contributor in temp_json[item]['contributor_ids']:
                if indv_contributor < 300:
                    temp_str = 'c' + str(indv_contributor)
                    temp_dict['target'] = temp_str
                    temp_dict['type'] = 'proj_contrib'
                    temp_projects.append(temp_dict.copy())
            for indv_lang in temp_json[item]['language_ids']:
                temp_str = 'l' + str(indv_lang)
                temp_dict['target'] = temp_str
                temp_dict['type'] = 'proj_lang'
                temp_projects.append(temp_dict.copy())
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
            # [{source: "companies", target: "Project", type: "licensing"}, ...]
            temp_dict = dict()
            temp_dict['source'] = temp_json[item]['name']
            for indv_project in temp_json[item]['project_ids']:
                temp_str = 'p' + str(indv_project)
                temp_dict['target'] = temp_str
                temp_dict['type'] = 'comp_proj'
                temp_projects.append(temp_dict.copy())
            for indv_contributor in temp_json[item]['member_ids']:
                if indv_contributor < 300:
                    temp_str = 'c' + str(indv_contributor)
                    temp_dict['target'] = temp_str
                    temp_dict['type'] = 'comp_contrib'
                    temp_projects.append(temp_dict.copy())
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
            # [{source: "contributors", target: "Contributors", type: "licensing"}, ...]
            temp_dict = dict()
            temp_dict['source'] = temp_json[item]['username']
            for indv_contributor in temp_json[item]['project_ids']:
                temp_str = 'p' + str(indv_contributor)
                temp_dict['target'] = temp_str
                temp_dict['type'] = 'contrib_proj'
                temp_projects.append(temp_dict.copy())
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
            # [{source: "languages", target: "Contributors", type: "licensing"}, ...]
            temp_dict = dict()
            temp_dict['source'] = temp_json[item]['name']
            language_mapping['l' + str(temp_json[item]['id'])] = temp_json[item]['name']
            for indv_contributor in temp_json[item]['project_ids']:
                if indv_contributor < 100:
                    temp_str = 'p' + str(indv_contributor)
                    temp_dict['target'] = temp_str
                    temp_dict['type'] = 'lang_proj'
                    temp_projects.append(temp_dict.copy())
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name
    return temp_projects



def get_contributor_names():
    url = 'http://opensourcery.me/api/contributors/?start=0&end=35420' #0-35420 is max
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            contributors_mapping['c' + str(temp_json[item]['id'])] = temp_json[item]['username']
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name


def get_project_names():
    url = 'http://opensourcery.me/api/projects/?start=0&end=6676' # 0-6676 is max
    response = requests.get(url)
    temp_json = response.json()
    for item in range(0, len(temp_json)):
        try:
            project_mapping['p' + str(temp_json[item]['id'])] = temp_json[item]['name']            
        except KeyError:
            pass # no key
        except NameError:
            pass # incorrect name



if __name__ == '__main__':
    api_call()