from datetime import timedelta
import httpx

from prefect import flow, task
from prefect.cache_policies import INPUTS
from prefect.concurrency.sync import rate_limit


@flow(log_prints=True)
def show_stars(github_repos: list[str]):
    """Show the number of stars that GitHub repos have"""

    stats_futures = fetch_stats.map(github_repos)

    stars = get_stars.map(stats_futures).result()

    for repo, star_count in zip(github_repos, stars):
        print(f"{repo} has {star_count} stars!")


@task(retries=3, cache_policy=INPUTS, cache_expiration=timedelta(days=1))
def fetch_stats(github_repo: str):
    """Fetch the statistics for a GitHub repo"""
    rate_limit("github-api")
    return httpx.get(f"https://api.github.com/repos/{github_repo}").json()


@task
def get_stars(repo_stats: dict):
    """Get the number of stars from GitHub repo statistics"""
    return repo_stats["stargazers_count"]


if __name__ == "__main__":
    show_stars(["PrefectHQ/prefect", "pydantic/pydantic", "huggingface/transformers"])
