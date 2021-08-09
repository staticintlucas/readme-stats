# `readme-stats`

Generates stats for [my profile README].

![stats]

## How it works

The script `main.py` contains all the code to fetch my statistics using GitHub's [GraphQL API].
This requires and API token generated to access my information, saved in this repository's secrets.

It uses these stats, along with the [Jinja] templating engine populates the SVG template in [templates/stats.svg](templates/stats.svg).
The generated SVG is saved to [output/stat.svg](output/stat.svg).

[GitHub Actions] is used to automate running the script.
The workflow is visible in [.github/workflows/main.yml](.github/workflows/main.yml).
This is programmed to run `main.py` every 6 hours and, if there are changes, check in a newly generated SVG.

[my profile readme]: https://github.com/staticintlucas/staticintlucas
[stats]: output/stats.svg
[graphql api]: https://docs.github.com/en/graphql
[jinja]: https://palletsprojects.com/p/jinja/
[github actions]: https://github.com/features/actions
