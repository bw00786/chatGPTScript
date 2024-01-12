import os
import requests
import json
from chatGPT import ChatGPT

# Set up the webhook
def webhook(request):
    if request.method == 'POST':
        # Get the pull request information
        pull_request = json.loads(request.body)
        pull_request_id = pull_request['id']
        pull_request_url = pull_request['url']

        # Get the code changes
        code_changes = get_code_changes(pull_request_url)

        # Generate the code review report
        report = generate_report(code_changes)

        # Post the report as a comment on the pull request
        post_comment(pull_request_id, report)

def get_code_changes(pull_request_url):
    # Use the GitHub API to retrieve the code changes
    response = requests.get(pull_request_url + '/files')
    code_changes = response.json()
    return code_changes

def generate_report(code_changes):
    # Use chatGPT to generate the code review report
    chatgpt = ChatGPT(model_name='124M', seed=42, temperature=0.7, top_k=40)
    report = chatgpt.generate(code_changes)
    return report

def post_comment(pull_request_id, report):
    # Use the GitHub API to post the report as a comment on the pull request
    response = requests.post(
        f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/issues/{pull_request_id}/comments',
        headers={'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'},
        json={'body': report}
    )
    if response.status_code == 201:
        print('Comment posted successfully')
    else:
        print('Error posting comment:', response.text)

if __name__ == '__main__':
    webhook(request)
