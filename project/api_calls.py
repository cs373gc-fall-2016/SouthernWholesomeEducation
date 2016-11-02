import requests
from models import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# dictionaries for each model
universities = dict()
cities = dict()
majors = dict()
ethnicities = dict()

DB.drop_all()
DB.create_all()

def api_call():
    # set_of_schools_nums = get_all_school_codes()
    #print('testing two austin schools')
    set_of_schools_nums = {228778, 227845, 135726, 123961, 204796} # TODO: Remove this and uncomment above for all schools (not just UT and St. Edwards)
    count = 0
    for school_num in set_of_schools_nums:
        school_dict = call_for_data(school_num)
        setup_data(school_dict)
        count += 1
        print (count)

    major_objs_uni = dict()
    eth_objs_uni = dict()
    major_objs_city = dict()
    eth_objs_city = dict()

    for maj in majors:
        major = create_unique(Major, name=maj, num_undergrads=majors[maj]['total_major_undergrad_population'], top_city=majors[maj]['top_city_name'], avg_percentage=majors[maj]['avg_percentage'])
        major2 = create_unique(Major, name=maj, num_undergrads=majors[maj]['total_major_undergrad_population'], top_city=majors[maj]['top_city_name'], avg_percentage=majors[maj]['avg_percentage'])
        major_objs_uni[maj] = major
        major_objs_city[maj] = major2

    for eth in ethnicities:
        ethnicity = create_unique(Ethnicity, name=eth, total_count=ethnicities[eth]['total_undergraduate_count'], top_city=ethnicities[eth]['top_city_name'], top_city_amt=ethnicities[eth]['top_city_amt'], top_university=ethnicities[eth]['top_university_name'], top_university_amt=ethnicities[eth]['top_university_amt'])
        ethnicity2 = create_unique(Ethnicity, name=eth, total_count=ethnicities[eth]['total_undergraduate_count'], top_city=ethnicities[eth]['top_city_name'], top_city_amt=ethnicities[eth]['top_city_amt'], top_university=ethnicities[eth]['top_university_name'], top_university_amt=ethnicities[eth]['top_university_amt'])
        eth_objs_uni[eth] = ethnicity
        eth_objs_city[eth] = ethnicity2

    for city in cities:
        cur_city = create_unique(City, name=city, population=cities[city]['population'], avg_tuition=cities[city]['average_tuition'])
        for maj in cities[city]['major_list']:
            if maj in major_objs_city:
                cur_city.add_major(majors[maj]['total_major_undergrad_population'], major_objs_city[maj])
        for eth in cities[city]['ethnicity_list']:
            if eth in eth_objs_city:
                cur_city.add_ethnicity(ethnicities[eth]['total_undergraduate_count'], eth_objs_city[eth])

    for uni in universities:
        university = create_unique(University , name=uni, num_undergrads=universities[uni]['undergrad_population'], cost_to_attend=universities[uni]['cost_to_attend'], grad_rate=universities[uni]['grad_rate'], public_or_private=universities[uni]['public_or_private'])
        for maj in universities[uni]['major_list']:
            if maj in major_objs_uni:
                university.add_major(universities[uni]['major_list'][maj], major_objs_uni[maj])
        for eth in universities[uni]['ethnicity_list']:
            if eth in eth_objs_uni:
                university.add_ethnicity(universities[uni]['ethnicity_list'][eth], eth_objs_uni[eth])

    DB.session.commit()

    # print(universities)
    # print(cities)
    # print(majors)
    # print(ethnicities)



def setup_data(individual_school_dict):
    # Universities
    uni_temp_dict = dict()
    if individual_school_dict['school.name'] is not None:
        uni_temp_dict['university_name'] = individual_school_dict['school.name']
    if individual_school_dict['2014.student.size'] is not None:
        uni_temp_dict['undergrad_population'] = individual_school_dict['2014.student.size']
    if individual_school_dict['2014.cost.avg_net_price.overall'] is not None:
        uni_temp_dict['cost_to_attend'] = individual_school_dict['2014.cost.avg_net_price.overall']
    if individual_school_dict['2014.completion.rate_suppressed.overall'] is not None:
        uni_temp_dict['grad_rate'] = individual_school_dict['2014.completion.rate_suppressed.overall']
    if individual_school_dict['school.city'] is not None:
        uni_temp_dict['city'] = individual_school_dict['school.city']
    uni_temp_dict['public_or_private'] = 'Public' if individual_school_dict['school.ownership'] == 1 else 'Private'
    uni_temp_dict['ethnicity_list'] = (major_and_ethnicity_dict(individual_school_dict, 'demographics', '2014.student.demographics.race_ethnicity.'))
    uni_temp_dict['ethnicity_count'] = len(uni_temp_dict['ethnicity_list'])
    uni_temp_dict['major_list'] = (major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.'))
    uni_temp_dict['major_count'] = len(uni_temp_dict['major_list'])

    # adding temp university to universities dict
    universities[individual_school_dict['school.name']] = uni_temp_dict

    # Cities
    if individual_school_dict['school.city'] in cities:
        # City already exists
        current_population = cities[individual_school_dict['school.city']]['population']
        new_cost_to_attend = individual_school_dict['2014.cost.avg_net_price.overall']
        new_student_population = individual_school_dict['2014.student.size']
        if new_student_population is not None:
            cities[individual_school_dict['school.city']]['population'] += new_student_population
        cities[individual_school_dict['school.city']]['university_count'] += 1

        #print(cities[individual_school_dict['school.city']]['major_list'])
        #print(major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.'))
        all_majors = major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.')
        for major in all_majors:
            if major not in cities[individual_school_dict['school.city']]['major_list']:
                if all_majors[major] is not None:
                    cities[individual_school_dict['school.city']]['major_list'][major] = all_majors[major]
            else:
                if all_majors[major] is not None:
                    cities[individual_school_dict['school.city']]['major_list'][major] += all_majors[major]
        #print(cities[individual_school_dict['school.city']]['major_list'])
        cities[individual_school_dict['school.city']]['major_count'] = len(cities[individual_school_dict['school.city']]['major_list'])
        # print(new_cost_to_attend)
        # print(new_student_population)
        if new_cost_to_attend is not None and new_student_population is not None and cities[individual_school_dict['school.city']]['average_tuition'] is not None and current_population is not None:
            cities[individual_school_dict['school.city']]['average_tuition'] = cities[individual_school_dict['school.city']]['average_tuition']*current_population/(current_population+new_student_population)+(new_cost_to_attend*new_student_population /
                                                                   (current_population + new_student_population))

        cities[individual_school_dict['school.city']]['ethnicity_list'].update(major_and_ethnicity_dict(individual_school_dict, 'demographics', '2014.student.demographics.race_ethnicity.'))
        cities[individual_school_dict['school.city']]['ethnicity_count'] = len(cities[individual_school_dict['school.city']]['ethnicity_list'])
    else:
        # creating a new city
        citi_temp_dict = dict()
        if individual_school_dict['school.city'] is not None:
            citi_temp_dict['city_name'] = individual_school_dict['school.city']
        if individual_school_dict['2014.student.size'] is not None:
            citi_temp_dict['population'] = individual_school_dict['2014.student.size']
        else:
            citi_temp_dict['population'] = 7382
        citi_temp_dict['university_count'] = 1 #city just added
        citi_temp_dict['major_list'] = major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.')
        citi_temp_dict['major_count'] = len(citi_temp_dict['major_list'])
        if individual_school_dict['2014.cost.avg_net_price.overall'] is not None:
            citi_temp_dict['average_tuition'] = individual_school_dict['2014.cost.avg_net_price.overall']
        else:
            citi_temp_dict['average_tuition'] = 12142
        citi_temp_dict['ethnicity_list'] = major_and_ethnicity_dict(individual_school_dict, 'demographics','2014.student.demographics.race_ethnicity.')
        citi_temp_dict['ethnicity_count'] = len(citi_temp_dict['ethnicity_list'])
        cities[individual_school_dict['school.city']] = citi_temp_dict

    # Majors
    for major in individual_school_dict:
        if major in majors:
            if individual_school_dict[major] is not None and individual_school_dict['2014.student.size']:
                majors[major]['total_major_undergrad_population'] += int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
                student_count = int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
            top_city_amt = top_city_for_major(major)
            if majors[major]['top_city_amt'] < top_city_amt[1]:
                majors[major]['top_city_amt'] = top_city_amt[1]
                majors[major]['top_city_name'] = top_city_amt[0]
            if majors[major]['total_major_undergrad_population'] is not None:
                majors[major]['avg_percentage'] = majors[major]['total_major_undergrad_population'] / total_undergrads_all_universities()
        else:
            # Not in major dict need to create
            if '2014.academics.program_percentage.' in major and individual_school_dict[major] != None and individual_school_dict[major] > 0:
                major_temp_dict = dict()
                major_temp_dict['major_name'] = major
                if individual_school_dict['2014.student.size'] is not None and individual_school_dict[major] is not None:
                    major_temp_dict['total_major_undergrad_population'] = int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
                major_temp_dict['top_city_amt'] = int(major_temp_dict['total_major_undergrad_population'])
                major_temp_dict['top_city_name'] = individual_school_dict['school.city']
                if major_temp_dict['total_major_undergrad_population'] is not None:
                    major_temp_dict['avg_percentage'] = major_temp_dict['total_major_undergrad_population'] / total_undergrads_all_universities()
                majors[major] = major_temp_dict

    # Ethnicities
    for ethnicity in individual_school_dict:
        if ethnicity in ethnicities:
            if individual_school_dict['2014.student.size'] is not None and individual_school_dict[ethnicity] is not None:
                ethnicities[ethnicity]['total_undergraduate_count'] += int(individual_school_dict['2014.student.size'] * individual_school_dict[ethnicity])
            ethnicities[ethnicity]['top_city_amt'] = top_city_for_ethnicity(ethnicity)[1]
            ethnicities[ethnicity]['top_city_name'] = top_city_for_ethnicity(ethnicity)[0]
            ethnicities[ethnicity]['top_university_amt'] = top_university_for_ethnicity(ethnicity)[1]
            ethnicities[ethnicity]['top_university_name'] = top_university_for_ethnicity(ethnicity)[0]
        else:
            # Did not find any data need to create
            if '2014.student.demographics.race_ethnicity.' in ethnicity and individual_school_dict[ethnicity] != None and individual_school_dict[ethnicity]:
                ethnicity_temp_dict = dict()
                ethnicity_temp_dict['ethnicity_name'] = ethnicity
                if 'total_undergraduate_count' not in ethnicity_temp_dict:
                    if individual_school_dict['2014.student.size'] is not None and individual_school_dict[ethnicity] is not None:
                        ethnicity_temp_dict['total_undergraduate_count'] = int(individual_school_dict['2014.student.size'] * individual_school_dict[ethnicity])
                else:
                    if individual_school_dict['2014.student.size'] is not None and individual_school_dict[ethnicity] is not None:
                        ethnicity_temp_dict['total_undergraduate_count'] += int(individual_school_dict['2014.student.size'] * individual_school_dict[ethnicity])
                ethnicity_temp_dict['top_city_amt'] = top_city_for_ethnicity(ethnicity)[1]
                ethnicity_temp_dict['top_city_name'] = top_city_for_ethnicity(ethnicity)[0]
                ethnicity_temp_dict['top_university_amt'] = top_university_for_ethnicity(ethnicity)[1]
                ethnicity_temp_dict['top_university_name'] = top_university_for_ethnicity(ethnicity)[0]
                ethnicities[ethnicity] = ethnicity_temp_dict
        # if ethnicity in ethnicities:
        #     print(ethnicities[ethnicity])



def total_undergrads_all_universities():
    total_undergraduates = 0
    for school in universities:
        if 'undergrad_population' in universities[school] and universities[school]['undergrad_population'] is not None:
            total_undergraduates += universities[school]['undergrad_population']
    if total_undergraduates == 0:
        return 1
    return total_undergraduates

def top_city_for_major(major_name):
    result = ("", 0)
    for city in cities:
        if major_name in cities[city]['major_list'] and cities[city]['major_list'][major_name] > result[1]:
            result = (city, cities[city]['major_list'][major_name])
    return result

def top_city_for_ethnicity(ethnicity_name):
    result = ("", 0)
    for city in cities:
        if ethnicity_name in cities[city]['ethnicity_list'] and cities[city]['ethnicity_list'][ethnicity_name] > result[1]:
            result = (city, cities[city]['ethnicity_list'][ethnicity_name])
    return result

def top_university_for_ethnicity(ethnicity_name):
    result = ("", 0)
    for uni in universities:
        if ethnicity_name in universities[uni]['ethnicity_list'] and universities[uni]['ethnicity_list'][ethnicity_name] > result[1]:
            result = (uni, universities[uni]['ethnicity_list'][ethnicity_name])
    return result


def major_and_ethnicity_dict(dict, text_to_search, str_to_remove):
    temp_dict = {}
    key_set = [key for key, value in dict.items() if text_to_search in key.lower()]
    for key in key_set:
        if (dict[key] != None) and (dict[key] > 0):
            if dict[key] is not None and dict['2014.student.size'] is not None:
                temp_dict[key] = int(dict[key] * dict['2014.student.size'])
            # print(key)
            # print(dict[key])
            # temp_dict.add(str(key).split(str_to_remove)[1])
    return temp_dict



def ethnicity_and_major_counter(dict, text_to_search):
    count = 0
    key_set = [key for key, value in dict.items() if text_to_search in key.lower()]
    for key in key_set:
        if (dict[key] != None) and (dict[key] > 0):
            count += 1
    return count


def call_for_data(school_num):
    data_url = 'https://api.data.gov/ed/collegescorecard/v1/schools/?fields=school.name,school.city,' \
                'school.state,school.school_url,school.ownership,2014.completion.rate_suppressed.overall,' \
                '2014.cost.avg_net_price.overall,2014.student.size,2014.student.demographics.race_ethnicity.black,' \
                '2014.student.demographics.race_ethnicity.hispanic_2000,2014.student.demographics.race_ethnicity.nhpi,' \
                '2014.student.demographics.race_ethnicity.aian_prior_2009,2014.student.demographics.race_ethnicity.aian_2000,' \
                '2014.student.demographics.race_ethnicity.white,2014.student.demographics.race_ethnicity.black_non_hispanic,' \
                '2014.student.demographics.race_ethnicity.api_2000,2014.student.demographics.race_ethnicity.unknown,' \
                '2014.student.demographics.race_ethnicity.hispanic,2014.student.demographics.race_ethnicity.asian,' \
                '2014.student.demographics.race_ethnicity.unknown_2000,2014.student.demographics.race_ethnicity.black_2000,' \
                '2014.student.demographics.race_ethnicity.non_resident_alien,2014.student.demographics.race_ethnicity.white_2000,' \
                '2014.student.demographics.race_ethnicity.hispanic_prior_2009,2014.student.demographics.race_ethnicity.two_or_more,' \
                '2014.student.demographics.race_ethnicity.asian_pacific_islander,2014.student.demographics.race_ethnicity.aian,' \
                '2014.student.demographics.race_ethnicity.white_non_hispanic,2014.student.demographics.race_ethnicity.black,' \
                '2014.academics.program_percentage.computer,2014.academics.program_percentage.legal,' + \
                '2014.academics.program_percentage.resources,2014.academics.program_percentage.multidiscipline,' \
                '2014.academics.program_percentage.mechanic_repair_technology,' \
                '2014.academics.program_percentage.public_administration_social_service,' \
                '2014.academics.program_percentage.transportation,2014.academics.program_percentage.architecture,' \
                '2014.academics.program_percentage.education,2014.academics.program_percentage.philosophy_religious,' \
                '2014.academics.program_percentage.engineering,2014.academics.program_percentage.communications_technology,' \
                '2014.academics.program_percentage.mathematics,2014.academics.program_percentage.theology_religious_vocation,' \
                '2014.academics.program_percentage.business_marketing,2014.academics.program_percentage.military,' \
                '2014.academics.program_percentage.physical_science,2014.academics.program_percentage.precision_production,' \
                '2014.academics.program_percentage.psychology,2014.academics.program_percentage.humanities,' \
                '2014.academics.program_percentage.science_technology,2014.academics.program_percentage.security_law_enforcement,' \
                '2014.academics.program_percentage.construction,2014.academics.program_percentage.communication,' \
                '2014.academics.program_percentage.agriculture,2014.academics.program_percentage.health,' \
                '2014.academics.program_percentage.engineering_technology,2014.academics.program_percentage.history,' \
                '2014.academics.program_percentage.biological,2014.academics.program_percentage.social_science,' \
                '2014.academics.program_percentage.personal_culinary,2014.academics.program_percentage.ethnic_cultural_gender,' \
                '2014.academics.program_percentage.library,2014.academics.program_percentage.family_consumer_science,' \
                '2014.academics.program_percentage.parks_recreation_fitness,2014.academics.program_percentage.language,' \
                '2014.academics.program_percentage.visual_performing,2014.academics.program_percentage.english' \
                '&id=' + str(school_num) + '&api_key=Xxf2NKtwfcXUd8K2hqawnlur6c0YY93xsNFwq0Dy'
    # printing result json data
    # print('url called: ', end ='')
    # print(data_url)
    output = requests.get(data_url)
    school_dict = output.json()
    # returning dictionary with school data
    return school_dict['results'][0]


def get_all_school_codes():
    # setting up url to collect all school codes
    start_url = 'https://api.data.gov/ed/collegescorecard/v1/schools/?fields=id&per_page=100&page='
    api_key = '&api_key=Xxf2NKtwfcXUd8K2hqawnlur6c0YY93xsNFwq0Dy'
    school_set = set()
    # looping over all pages in the the api results
    for page_num in range(0,78):
        print('collecting school numbers page ' + str(page_num), end='')
        output = requests.get(start_url + str(page_num) + api_key)
        dict = output.json()
        # looping over results for each page and saving codes into set
        for item in dict['results']:
            school_set.add(item['id'])
        print(', added ' + str(len(dict['results'])) + ' items' + '       [DONE]')
    print('\nTotal Number of Schools added: ' + str(len(school_set)))
    # set of school numbers returned
    return school_set

if __name__ == '__main__':
    api_call()