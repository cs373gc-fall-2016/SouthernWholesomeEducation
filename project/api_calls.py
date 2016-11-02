import requests

# dictionaries for each model
universities = dict()
cities = dict()
majors = dict()
ethnicities = dict()

def api_call():
    # set_of_schools_nums = get_all_school_codes()
    print('testing two austin schools')
    set_of_schools_nums = {228778, 227845} # TODO: Remove this and uncomment above for all schools (not just UT and St. Edwards)
    for school_num in set_of_schools_nums:
        school_dict = call_for_data(school_num)
        setup_data(school_dict)



def setup_data(individual_school_dict):
    # Universities
    uni_temp_dict = dict()
    uni_temp_dict['university_name'] = individual_school_dict['school.name']
    uni_temp_dict['undergrand_population'] = individual_school_dict['2014.student.size']
    uni_temp_dict['cost_to_attend'] = individual_school_dict['2014.cost.avg_net_price.overall']
    uni_temp_dict['grad_rate'] = individual_school_dict['2014.completion.rate_suppressed.overall']
    uni_temp_dict['city'] = individual_school_dict['school.city']
    uni_temp_dict['public_or_private'] = 'Public' if individual_school_dict['school.ownership'] == 1 else 'Private'
    uni_temp_dict['ethnicity_count'] = ethnicity_and_major_counter(individual_school_dict, 'demographics')
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
        cities[individual_school_dict['school.city']]['population'] += new_student_population
        cities[individual_school_dict['school.city']]['university_count'] += 1
        cities[individual_school_dict['school.city']]['major_list'].update(major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.'))
        cities[individual_school_dict['school.city']]['major_count'] = len(cities[individual_school_dict['school.city']]['major_list'])
        cities[individual_school_dict['school.city']]['average_tuition'] = cities[individual_school_dict['school.city']]['average_tuition']*current_population/(current_population+new_student_population)+(new_cost_to_attend*new_student_population /
                                                                   (current_population + new_student_population))
        cities[individual_school_dict['school.city']]['ethnicity_list'].update(major_and_ethnicity_dict(individual_school_dict, 'demographics', '2014.student.demographics.race_ethnicity.'))
        cities[individual_school_dict['school.city']]['ethnicity_count'] = len(cities[individual_school_dict['school.city']]['ethnicity_list'])
    else:
        # creating a new city
        citi_temp_dict = dict()
        citi_temp_dict['city_name'] = individual_school_dict['school.city']
        citi_temp_dict['population'] = individual_school_dict['2014.student.size']
        citi_temp_dict['university_count'] = 1 #city just added
        citi_temp_dict['major_list'] = major_and_ethnicity_dict(individual_school_dict, 'program_percentage', '2014.academics.program_percentage.')
        citi_temp_dict['major_count'] = len(citi_temp_dict['major_list'])
        citi_temp_dict['average_tuition'] = individual_school_dict['2014.cost.avg_net_price.overall']
        citi_temp_dict['ethnicity_list'] = major_and_ethnicity_dict(individual_school_dict, 'demographics','2014.student.demographics.race_ethnicity.')
        citi_temp_dict['ethnicity_count'] = len(citi_temp_dict['ethnicity_list'])
        cities[individual_school_dict['school.city']] = citi_temp_dict

    # Majors
    for major in individual_school_dict:
        if major in majors:
            majors[major]['total_major_undergrad_population'] += int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
            student_count = int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
            if (majors[major]['top_city_amt'] < student_count):
                # need to update
                majors[major]['top_city_amt'] = student_count
                majors[major]['top_city_name'] = individual_school_dict['school.city']
            majors[major]['avg_percentage'] = majors[major]['total_major_undergrad_population'] / total_undergrads_all_universities()
        else:
            # Not in major dict need to create
            if '2014.academics.program_percentage.' in major and individual_school_dict[major] != None and individual_school_dict[major] > 0:
                major_temp_dict = dict()
                major_temp_dict['major_name'] = major
                major_temp_dict['total_major_undergrad_population'] = int(individual_school_dict['2014.student.size'] * individual_school_dict[major])
                major_temp_dict['top_city_amt'] = int(major_temp_dict['total_major_undergrad_population'])
                major_temp_dict['top_city_name'] = individual_school_dict['school.city']
                major_temp_dict['avg_percentage'] = major_temp_dict['total_major_undergrad_population'] / total_undergrads_all_universities()
                majors[major] = major_temp_dict

    # Ethnicities
    for ethnicity in individual_school_dict:
        if ethnicity in ethnicities:
            print('found ethnicity need to update it')
        else:
            # Did not find any data need to create
            if '2014.student.demographics.race_ethnicity.' in ethnicity and individual_school_dict[ethnicity] != None and individual_school_dict[ethnicity]:
                ethnicity_temp_dict = dict()
                ethnicity_temp_dict['ethnicity_name'] = ethnicity
                ethnicity_temp_dict['total_undergraduate_count'] = int(individual_school_dict['2014.student.size'] * individual_school_dict[ethnicity])
                # need top city
                # need top university
                # print(ethnicity_temp_dict)


    print(universities)
    print(cities)
    print(majors)
    print(ethnicities)



def total_undergrads_all_universities():
    total_undergraduates = 0
    for school in universities:
        total_undergraduates += universities[school]['undergrand_population']
    return total_undergraduates



def major_and_ethnicity_dict(dict, text_to_search, str_to_remove):
    temp_dict = {}
    key_set = [key for key, value in dict.items() if text_to_search in key.lower()]
    for key in key_set:
        if (dict[key] != None) and (dict[key] > 0):
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
    api_key = '&api_key=UvIG23p13yTXK5PTit5MZEWcNXMCoKsl5QonaV8Y'
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