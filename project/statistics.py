import requests

def get_github_stats():
    commits_url = 'https://api.github.com/repos/cs373gc-fall-2016/SouthernWholesomeEducation/stats/contributors?client_id=acfa1c2e958731bb1f90&client_secret=a6c4060bd74b28cedb5e02b0a0068750d05af16f'
    output = requests.get(commits_url)
    school_dict = output.json()

    issue_count_url = 'https://api.github.com/repos/cs373gc-fall-2016/SouthernWholesomeEducation/issues?state=all&per_page=100&client_id=acfa1c2e958731bb1f90&client_secret=a6c4060bd74b28cedb5e02b0a0068750d05af16f'
    output2 = requests.get(issue_count_url)
    count_dict = output2.json()
    number_of_commits = count_dict[0]['number']

    user_statistics = dict()

    for student_count in range(len(school_dict)):
        if school_dict[student_count]['author']['login'] not in user_statistics:
            user_statistics[school_dict[student_count]['author']['login']] = {'commits': 0, 'issues': 0, 'unit_tests': 0}
        user_statistics[school_dict[student_count]['author']['login']]['commits'] = school_dict[student_count]['total']

    for num in range(len(count_dict)):
        login_name = count_dict[num]['user']['login']
        if login_name not in user_statistics:
            user_statistics[login_name] = {}
        else:
            user_statistics[login_name]['issues'] += 1

    user_statistics['mjvolk']['unit_tests'] = 23
    user_statistics['jymin94']['unit_tests'] = 14
    user_statistics['ace-jc']['unit_tests'] = 12
    user_statistics['mxavier6']['unit_tests'] = 33
    user_statistics['budang']['unit_tests'] = 19
    user_statistics['budang']['commits'] += 30
    user_statistics['ninean']['unit_tests'] = 13


    total_statistics = {'commits': 0, 'issues': 0, 'unit_tests': 0}
    for team_member in user_statistics:
        total_statistics['commits'] += int(user_statistics[team_member]['commits'])
        total_statistics['issues'] += int(user_statistics[team_member]['issues'])
        total_statistics['unit_tests'] += int(user_statistics[team_member]['unit_tests'])

    # http://localhost:5000/githubstats
    final_json = {'user_stats' : user_statistics, 'total_stats':total_statistics}
    return final_json
