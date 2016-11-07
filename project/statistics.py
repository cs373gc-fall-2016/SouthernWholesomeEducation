import requests

commits_url = 'https://api.github.com/repos/cs373gc-fall-2016/SouthernWholesomeEducation/stats/contributors?client_id=acfa1c2e958731bb1f90&client_secret=a6c4060bd74b28cedb5e02b0a0068750d05af16f'
output = requests.get(commits_url)
school_dict = output.json()

issue_count_url = 'https://api.github.com/repos/cs373gc-fall-2016/SouthernWholesomeEducation/issues?state=closed&client_id=acfa1c2e958731bb1f90&client_secret=a6c4060bd74b28cedb5e02b0a0068750d05af16f'
output2 = requests.get(issue_count_url)
count_dict = output2.json()
number_of_commits = count_dict[0]['number']

each_issue_part1 = 'https://api.github.com/repos/cs373gc-fall-2016/SouthernWholesomeEducation/issues/'
each_issue_part2 = '?client_id=acfa1c2e958731bb1f90&client_secret=a6c4060bd74b28cedb5e02b0a0068750d05af16f'

user_statistics = dict()

for student_count in range(len(school_dict)):
    if school_dict[student_count]['author']['login'] not in user_statistics:
        user_statistics[school_dict[student_count]['author']['login']] = [0,0,0]
    user_statistics[school_dict[student_count]['author']['login']][0] = school_dict[student_count]['total']


for num in range(number_of_commits):
    output3 = requests.get(each_issue_part1 + str(num+1) + each_issue_part2) #github has no zero based indexing
    count_dict = output3.json()
    login_name = count_dict['user']['login']
    if login_name not in user_statistics:
        user_statistics[login_name] = [0,0,0]
    else:
        user_statistics[login_name][1] += 1

user_statistics['mjvolk'][2] = 23
user_statistics['jymin94'][2] = 14
user_statistics['ace-jc'][2] = 12
user_statistics['mxavier6'][2] = 33
user_statistics['budang'][2] = 19
user_statistics['ninean'][2] = 13


total_statistics = [0,0,0]
for team_member in user_statistics:
    for num in range(0,3):
        total_statistics[num] += int(user_statistics[team_member][num])

# {'user_stats': [<commits>,<issues>,<unit tests>], 'total_stats':[<commits>,<issues>,<unit tests>] }
final_json = {'user_stats' : user_statistics, 'total_stats':total_statistics}
print(final_json)
