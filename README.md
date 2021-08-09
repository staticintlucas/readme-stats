# `readme-stats`

Generates stats for [my profile README].

![stats]

## How it works

The script `main.py` contains all the code to fetch my statistics using GitHub's [GraphQL API].
This requires and API token with permissions to access my information, which is saved in this repository's secrets.

With these stats, and the [Jinja] templating engine, it populates the SVG template in [templates/stats.svg](templates/stats.svg).
The finished SVG is saved to [output/stats.svg](output/stats.svg).

[GitHub Actions] is used to automate running the script.
The workflow is visible in [.github/workflows/main.yml](.github/workflows/main.yml).
This is programmed to run `main.py` every 6 hours and, if there are changes, commit the newly generated SVG.

Note: it can take some time for the image to update after the workflow has run.
GitHub seems to cache some images despite having been modified in the repo.

[my profile readme]: https://github.com/staticintlucas/staticintlucas
[stats]: output/stats.svg
[graphql api]: https://docs.github.com/en/graphql
[jinja]: https://palletsprojects.com/p/jinja/
[github actions]: https://github.com/features/actions
