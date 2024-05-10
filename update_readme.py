import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

with open("leetcode_query.gql", "r") as gql_file:
    graphql_query = gql(gql_file.read())

with open("leetcode_query_variables.json", "r") as params_file:
    query_variables = json.load(params_file)

http_transport = RequestsHTTPTransport(
    url="https://leetcode.com/graphql",
)

graphql_client = Client(transport=http_transport)

query_result = graphql_client.execute(graphql_query, variable_values=query_variables)

print(query_result)
