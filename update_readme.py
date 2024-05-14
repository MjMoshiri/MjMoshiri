import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from jinja2 import Environment, FileSystemLoader
import datetime
with open("leetcode_query.gql", "r") as gql_file:
    graphql_query = gql(gql_file.read())

with open("leetcode_query_variables.json", "r") as params_file:
    query_variables = json.load(params_file)

http_transport = RequestsHTTPTransport(url="https://leetcode.com/graphql")
graphql_client = Client(transport=http_transport)

query_result = graphql_client.execute(graphql_query, variable_values=query_variables)
total_accepted_questions = sum(d["count"] for d in query_result["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"])
query_result["totalAcceptedQuestions"] = total_accepted_questions

language_dict = {}
for language in query_result["languageStats"]["languageProblemCount"]:
    language_dict[language["languageName"]] = language["problemsSolved"]

query_result["languageStats"] = language_dict

    
query_result["streakCounter"] = 318 + (datetime.datetime.now() - datetime.datetime(2024,5,12)).days

file_loader = FileSystemLoader(".")
env = Environment(loader=file_loader)

template = env.get_template("README.Jinja")

rendered_template = template.render(data=query_result)

with open("README.md", "w") as readme_file:
    readme_file.write(rendered_template)
