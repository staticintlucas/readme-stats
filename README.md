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

Note: It can take some time for the image to update after the workflow has run.
GitHub seems to cache some images despite having been modified in the repo.

Note #2: The percentages of the languages used may not exactly add up to 100% depending on rounding errors.
It may sometimes appear to be 99.9% or 100.1% total.

## Use this for yourself

1. Fork/clone this repo
1. In your GitHub user settings, go to *Developer settings*, then *Personal access tokens* and create a new token with the *repo* and *read:user* permissions.
Set it to never expire, otherwise your stats will eventually stop updating.
1. In your repo setting go to *Secrets*, create a new *Repository secret* called `ACCESS_TOKEN`, and paste in your newly generated key.
1. Edit the template in [templates/stats.svg](templates/stats.svg) to remove my name and add yours.
   Note: I could fetch the user's name from the API, but programmatically adding the possessive apostrophe correctly is not always possible (e.g. Louis' or Louis's depends on how it's pronounced :smile:).
   Besides, lots of people will want to translate to their native languages anyway.

### Warning

Since this script has access to your private repos, it is (in theory) possible for people to learn more then they otherwise could about your private repos.
If an error happens in GitHub actions, the publicly visible log could potentially contain some info about your private repo names, stars, forks, issue count, languages, etc.
For me this is OK since I only have a bunch of half-finished projects there, but if you have anything super top secret you should be careful.

[my profile readme]: https://github.com/staticintlucas
[stats]: output/stats.svg
[graphql api]: https://docs.github.com/en/graphql
[jinja]: https://palletsprojects.com/p/jinja/
[github actions]: https://github.com/features/actions
