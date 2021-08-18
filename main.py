#!/usr/bin/env python3

import os
from pathlib import Path

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = Path.cwd() / "templates"
OUTPUT_DIR = Path.cwd() / "output"
TEMPLATE_ROWS = 6


def get_repos(client, after=None):
    query = gql(f"""{{
        viewer {{
            repositories(first: 100, isFork: false{f"" if after is None else f", after: {after}"}) {{
                pageInfo {{
                    endCursor
                    hasNextPage
                }}
                nodes {{
                    stargazerCount
                    forkCount
                    languages(first: 100, orderBy: {{field: SIZE, direction: DESC}}) {{
                        edges {{
                            size
                        }}
                        nodes {{
                            name
                            color
                        }}
                    }}
                }}
            }}
        }}
    }}""")

    result = client.execute(query)

    repos = result["viewer"]["repositories"]["nodes"]
    page_info = result["viewer"]["repositories"]["pageInfo"]

    if page_info["hasNextPage"]:
        repos.extend(get_repos(client, after=page_info["endCursor"]))

    return repos


def get_contribs(client):

    query = gql(f"""{{
        viewer {{
            contributionsCollection {{
                contributionCalendar {{
                    totalContributions
                }}
                totalIssueContributions
                totalPullRequestContributions
                totalRepositoriesWithContributedCommits
            }}
        }}
    }}""")

    result = client.execute(query)

    return result["viewer"]["contributionsCollection"]


def get_stats(token):

    client = Client(transport=RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {token}"},
    ))

    repos = get_repos(client)

    langs = {}
    for repo in repos:
        edges, nodes = repo["languages"]["edges"], repo["languages"]["nodes"]
        for edge, node in zip(edges, nodes):
            name = node["name"]
            count = edge["size"]
            color = node["color"]
            langs[name] = {
                "name": name,
                "count": count + (langs[name]["count"] if name in langs else 0),
                "color": "#ccc" if color is None else color,
            }
    langs = sorted(langs.values(), key=lambda l: l["count"], reverse=True)[:7]
    if len(langs) > TEMPLATE_ROWS:
        other = {
            "name": "Other",
            "count": sum(lang["count"] for lang in langs[TEMPLATE_ROWS-1:]),
            "color": "#ccc",
        }
        langs = [*langs[:TEMPLATE_ROWS-1], other]

    contribs = get_contribs(client)

    return {
        "stars":        sum(repo["stargazerCount"] for repo in repos),
        "forks":        sum(repo["forkCount"] for repo in repos),
        "contribs":     contribs["contributionCalendar"]["totalContributions"],
        "issues":       contribs["totalIssueContributions"],
        "pull_reqs":    contribs["totalPullRequestContributions"],
        "contrib_to":   contribs["totalRepositoriesWithContributedCommits"],
        "langs":        langs,
    }


def main(token):

    stats = get_stats(token)

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR)
    )
    for name in env.list_templates():
        template = env.get_template(name)
        result = template.render(stats)

        OUTPUT_DIR.mkdir(exist_ok=True)
        with open(OUTPUT_DIR / name, "w") as f:
            f.write(result)


if __name__ == "__main__":

    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        raise ValueError("Environment variable GITHUB_TOKEN not set")

    main(token)
