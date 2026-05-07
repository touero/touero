#!/usr/bin/python3

import asyncio
import fnmatch
import json
import os
import sys
import time
from typing import Dict, List, Optional, Set, Tuple

import aiohttp
import requests


###############################################################################
# Main Classes
###############################################################################

class Queries(object):
    """
    Class with functions to query the GitHub GraphQL (v4) API and the REST (v3)
    API. Also includes functions to dynamically generate GraphQL queries.
    """

    def __init__(self, username: str, access_token: str,
                 session: aiohttp.ClientSession, max_connections: int = 10):
        self.username = username
        self.access_token = access_token
        self.session = session
        self.semaphore = asyncio.Semaphore(max_connections)

    async def query(self, generated_query: str) -> Dict:
        """
        Make a request to the GraphQL API using the authentication token from
        the environment
        :param generated_query: string query to be sent to the API
        :return: decoded GraphQL JSON output
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        url = "https://api.github.com/graphql"
        try:
            async with self.semaphore:
                r = await self.session.post(url, headers=headers, json={"query": generated_query})
            return await r.json()
        except Exception as e:
            print(f"Async query {url} error: {str(e)}")
            async with self.semaphore:
                r = requests.post(url, headers=headers, json={"query": generated_query})
                return r.json()

    async def query_rest(self, path: str, params: Optional[Dict] = None) -> Dict:
        """
        Make a request to the REST API
        :param path: API path to query
        :param params: Query parameters to be passed to the API
        :return: deserialized REST JSON output
        """

        headers = {
            "Authorization": f"token {self.access_token}",
        }
        local_params = dict() if params is None else dict(params)
        normalized_path = path[1:] if path.startswith("/") else path
        url = f"https://api.github.com/{normalized_path}"

        for attempt in range(30):
            retry_after = min(60, 10 + attempt * 2)
            try:
                async with self.semaphore:
                    r = await self.session.get(url, headers=headers, params=tuple(local_params.items()))
                if r.status == 200:
                    result = await r.json()
                    if result is not None:
                        return result
                if r.status in (401, 404):
                    body = await r.text()
                    print(f"Async get {url} returned non-retryable status {r.status}. Skipping.\n"
                          f"Body: {body[:500]}")
                    return dict()
                if r.status == 403:
                    body = await r.text()
                    # For traffic APIs, GitHub requires push/admin access; this is not retryable.
                    if ("Must have push access to repository" in body
                            or "Resource not accessible by integration" in body):
                        print(f"Async get {url} returned non-retryable status 403 (permission). Skipping.\n"
                              f"Body: {body[:500]}")
                        return dict()
                    # Rate-limit 403 may be temporary; retry those.
                    if "rate limit" in body.lower():
                        reset_epoch = r.headers.get("X-RateLimit-Reset")
                        wait_reason = "backoff"
                        if reset_epoch and reset_epoch.isdigit():
                            reset_wait = max(1, int(reset_epoch) - int(time.time()) + 1)
                            retry_after = max(retry_after, min(reset_wait, 3600))
                            wait_reason = "until rate-limit reset"
                        print(f"Async get {url} returned status 403 (rate limit). "
                              f"Retrying in {retry_after}s ({wait_reason})...\n"
                              f"Body: {body[:500]}")
                        await asyncio.sleep(retry_after)
                        continue
                    print(f"Async get {url} returned non-retryable status 403. Skipping.\n"
                          f"Body: {body[:500]}")
                    return dict()
                if r.status == 202:
                    header_delay = r.headers.get("Retry-After")
                    if header_delay and header_delay.isdigit():
                        retry_after = max(retry_after, int(header_delay))
                    print(f"Async get {url} returned status 202 (GitHub is computing stats). "
                          f"Retrying in {retry_after}s...")
                elif r.status == 429 or 500 <= r.status <= 599:
                    body = await r.text()
                    print(f"Async get {url} returned retryable status {r.status}. Retrying in {retry_after}s...\n"
                          f"Body: {body[:500]}")
                else:
                    body = await r.text()
                    print(f"Async get {url} returned non-retryable status {r.status}. Skipping.\n"
                          f"Body: {body[:500]}")
                    return dict()
                await asyncio.sleep(retry_after)
                continue
            except Exception as e:
                print(f"Async rest_query {url}: {str(e)}")
                async with self.semaphore:
                    r = requests.get(url, headers=headers, params=tuple(local_params.items()))
                    if r.status_code == 200:
                        return r.json()
                    if r.status_code == 403 and "rate limit" in (r.text or "").lower():
                        reset_epoch = r.headers.get("X-RateLimit-Reset")
                        wait_reason = "backoff"
                        if reset_epoch and reset_epoch.isdigit():
                            reset_wait = max(1, int(reset_epoch) - int(time.time()) + 1)
                            retry_after = max(retry_after, min(reset_wait, 3600))
                            wait_reason = "until rate-limit reset"
                        print(f"Sync get {url} returned status 403 (rate limit). "
                              f"Retrying in {retry_after}s ({wait_reason})...\n"
                              f"Body: {r.text[:500]}")
                        await asyncio.sleep(retry_after)
                        continue
                    if r.status_code in (401, 403, 404):
                        print(f"Sync get {url} returned non-retryable status {r.status_code}. Skipping.\n"
                              f"Body: {r.text[:500]}")
                        return dict()
                    print(f"Sync get {url} returned status {r.status_code}. Retrying in {retry_after}s...\n"
                          f"Body: {r.text[:500]}")
                    await asyncio.sleep(retry_after)
                    continue
        print("There are too many access failures. Data for this repository will be incomplete.")
        return dict()

    @staticmethod
    def repos_overview(contrib_cursor: Optional[str] = None,
                       owned_cursor: Optional[str] = None) -> str:
        """
        :return: GraphQL query with overview of user repositories
        """
        return f"""{{
  viewer {{
    login,
    name,
    repositories(
        first: 100,
        orderBy: {{
            field: UPDATED_AT,
            direction: DESC
        }},
        after: {"null" if owned_cursor is None else '"'+ owned_cursor +'"'}
    ) {{
      pageInfo {{
        hasNextPage
        endCursor
      }}
      nodes {{
        nameWithOwner
        isFork
        viewerPermission
        stargazers {{
          totalCount
        }}
        forkCount
        languages(first: 10, orderBy: {{field: SIZE, direction: DESC}}) {{
          edges {{
            size
            node {{
              name
              color
            }}
          }}
        }}
      }}
    }}
    repositoriesContributedTo(
        first: 100,
        includeUserRepositories: false,
        orderBy: {{
            field: UPDATED_AT,
            direction: DESC
        }},
        contributionTypes: [
            COMMIT,
            PULL_REQUEST,
            REPOSITORY,
            PULL_REQUEST_REVIEW
        ]
        after: {"null" if contrib_cursor is None else '"'+ contrib_cursor +'"'}
    ) {{
      pageInfo {{
        hasNextPage
        endCursor
      }}
      nodes {{
        nameWithOwner
        viewerPermission
        stargazers {{
          totalCount
        }}
        forkCount
        languages(first: 10, orderBy: {{field: SIZE, direction: DESC}}) {{
          edges {{
            size
            node {{
              name
              color
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""

    @staticmethod
    def contrib_years() -> str:
        """
        :return: GraphQL query to get all years the user has been a contributor
        """
        return """
query {
  viewer {
    contributionsCollection {
      contributionYears
    }
  }
}
"""

    @staticmethod
    def contribs_by_year(year: str) -> str:
        """
        :param year: year to query for
        :return: portion of a GraphQL query with desired info for a given year
        """
        return f"""
    year{year}: contributionsCollection(
        from: "{year}-01-01T00:00:00Z",
        to: "{int(year) + 1}-01-01T00:00:00Z"
    ) {{
      contributionCalendar {{
        totalContributions
      }}
    }}
"""

    @classmethod
    def all_contribs(cls, years: List[str]) -> str:
        """
        :param years: list of years to get contributions for
        :return: query to retrieve contribution information for all user years
        """
        by_years = "\n".join(map(cls.contribs_by_year, years))
        return f"""
query {{
  viewer {{
    {by_years}
  }}
}}
"""


class Stats(object):
    """
    Retrieve and store statistics about GitHub usage.
    """
    def __init__(self, username: str, access_token: str,
                 session: aiohttp.ClientSession,
                 exclude_repos: Optional[Set] = None,
                 exclude_langs: Optional[Set] = None,
                 consider_forked_repos: bool = False):
        self.username = username
        self._exclude_repos = set() if exclude_repos is None else exclude_repos
        self._exclude_langs = set() if exclude_langs is None else exclude_langs
        self._consider_forked_repos = consider_forked_repos
        self.queries = Queries(username, access_token, session)

        self._name = None
        self._stargazers = None
        self._forks = None
        self._total_contributions = None
        self._languages = None
        self._repos = None
        self._repos_with_push = None
        self._lines_changed = None
        self._views = None        

    def _is_repo_excluded(self, repo_name: str) -> bool:
        """
        Return True when repo name matches any exclude pattern.
        Supports exact names and glob patterns like `owner/*`.
        """
        if repo_name in self._exclude_repos:
            return True
        return any(fnmatch.fnmatch(repo_name, pattern) for pattern in self._exclude_repos)

    async def to_str(self) -> str:
        """
        :return: summary of all available statistics
        """
        languages = await self.languages_proportional
        formatted_languages = "\n  - ".join(
            [f"{k}: {v:0.4f}%" for k, v in languages.items()]
        )
        lines_changed = await self.lines_changed
        return f"""Name: {await self.name}
Stargazers: {await self.stargazers:,}
Forks: {await self.forks:,}
All-time contributions: {await self.total_contributions:,}
Repositories with contributions: {len(await self.all_repos)}
Lines of code added: {lines_changed[0]:,}
Lines of code deleted: {lines_changed[1]:,}
Lines of code changed: {lines_changed[0] + lines_changed[1]:,}
Project page views: {await self.views:,}
Languages:
  - {formatted_languages}"""

    async def get_stats(self) -> None:
        """
        Get lots of summary statistics using one big query. Sets many attributes
        """
        self._stargazers = 0
        self._forks = 0
        self._languages = dict()
        self._repos = set()
        self._repos_with_push = set()
        self._ignored_repos = set()
        
        next_owned = None
        next_contrib = None
        while True:
            raw_results = await self.queries.query(
                Queries.repos_overview(owned_cursor=next_owned,
                                       contrib_cursor=next_contrib)
            )
            raw_results = raw_results if raw_results is not None else {}

            self._name = (raw_results
                          .get("data", {})
                          .get("viewer", {})
                          .get("name", None))
            if self._name is None:
                self._name = (raw_results
                              .get("data", {})
                              .get("viewer", {})
                              .get("login", "No Name"))

            contrib_repos = (raw_results
                             .get("data", {})
                             .get("viewer", {})
                             .get("repositoriesContributedTo", {}))
            owned_repos = (raw_results
                           .get("data", {})
                           .get("viewer", {})
                           .get("repositories", {}))
            
            repos = []
            for repo in owned_repos.get("nodes", []):
                repo_name = repo.get("nameWithOwner")
                if repo.get("isFork", False) and not self._consider_forked_repos:
                    # Keep forked repos out of aggregate stats unless explicitly enabled.
                    if repo_name and not self._is_repo_excluded(repo_name):
                        self._ignored_repos.add(repo_name)
                    continue
                repos.append(repo)

            # Contributed repos are for contribution-based metrics (e.g. lines changed),
            # not star/fork aggregates.
            for repo in contrib_repos.get("nodes", []):
                repo_name = repo.get("nameWithOwner")
                if repo_name in self._ignored_repos or self._is_repo_excluded(repo_name):
                    continue
                self._ignored_repos.add(repo_name)

            for repo in repos:
                name = repo.get("nameWithOwner")
                if name in self._repos or self._is_repo_excluded(name):
                    continue
                self._repos.add(name)
                permission = repo.get("viewerPermission", "")
                if permission in {"ADMIN", "MAINTAIN", "WRITE"}:
                    self._repos_with_push.add(name)
                self._stargazers += repo.get("stargazers").get("totalCount", 0)
                self._forks += repo.get("forkCount", 0)

                for lang in repo.get("languages", {}).get("edges", []):
                    name = lang.get("node", {}).get("name", "Other")
                    languages = await self.languages
                    if name in self._exclude_langs: continue
                    if name in languages:
                        languages[name]["size"] += lang.get("size", 0)
                        languages[name]["occurrences"] += 1
                    else:
                        languages[name] = {
                            "size": lang.get("size", 0),
                            "occurrences": 1,
                            "color": lang.get("node", {}).get("color")
                        }

            if owned_repos.get("pageInfo", {}).get("hasNextPage", False) or \
                    contrib_repos.get("pageInfo", {}).get("hasNextPage", False):
                next_owned = (owned_repos
                              .get("pageInfo", {})
                              .get("endCursor", next_owned))
                next_contrib = (contrib_repos
                                .get("pageInfo", {})
                                .get("endCursor", next_contrib))
            else:
                break

        # TODO: Improve languages to scale by number of contributions to
        #       specific filetypes
        print("---- Languages:")
        print(json.dumps(self._languages, indent=2, ensure_ascii=False))

        if self._languages.get("Python") is not None and self._languages.get("Jupyter Notebook") is not None:
            jupyter_statistics: int = self._languages["Jupyter Notebook"].get("size", 0)
            python_statistics: int = self._languages["Python"].get("size", 0)
            self._languages["Python"]["size"] = jupyter_statistics + python_statistics
            self._languages.pop("Jupyter Notebook", None)

        langs_total = sum([v.get("size", 0) for v in self._languages.values()])
        for k, v in self._languages.items():
            v["prop"] = 100 * (v.get("size", 0) / langs_total)

    @property
    async def name(self) -> str:
        """
        :return: GitHub user's name (e.g., Jacob Strieb)
        """
        if self._name is not None:
            return self._name
        await self.get_stats()
        assert(self._name is not None)
        return self._name

    @property
    async def stargazers(self) -> int:
        """
        :return: total number of stargazers on user's repos
        """
        if self._stargazers is not None:
            return self._stargazers
        await self.get_stats()
        assert(self._stargazers is not None)
        return self._stargazers

    @property
    async def forks(self) -> int:
        """
        :return: total number of forks on user's repos
        """
        if self._forks is not None:
            return self._forks
        await self.get_stats()
        assert(self._forks is not None)
        return self._forks

    @property
    async def languages(self) -> Dict:
        """
        :return: summary of languages used by the user
        """
        if self._languages is not None:
            return self._languages
        await self.get_stats()
        assert(self._languages is not None)
        return self._languages

    @property
    async def languages_proportional(self) -> Dict:
        """
        :return: summary of languages used by the user, with proportional usage
        """
        if self._languages is None:
            await self.get_stats()
            assert(self._languages is not None)

        return {k: v.get("prop", 0) for (k, v) in self._languages.items()}

    @property
    async def repos(self) -> List[str]:
        """
        :return: list of names of user's repos
        """
        if self._repos is not None:
            return self._repos
        await self.get_stats()
        assert(self._repos is not None)
        return self._repos
    
    @property
    async def all_repos(self) -> List[str]:
        """
        :return: list of names of user's repos with contributed repos included
                irrespective of whether the ignore flag is set or not
        """
        if self._repos is not None and self._ignored_repos is not None:
            return self._repos | self._ignored_repos
        await self.get_stats()
        assert(self._repos is not None)
        assert(self._ignored_repos is not None)
        return self._repos | self._ignored_repos

    @property
    async def total_contributions(self) -> int:
        """
        :return: count of user's total contributions as defined by GitHub
        """
        if self._total_contributions is not None:
            return self._total_contributions

        self._total_contributions = 0
        years = (await self.queries.query(Queries.contrib_years())) \
            .get("data", {}) \
            .get("viewer", {}) \
            .get("contributionsCollection", {}) \
            .get("contributionYears", [])
        by_year = (await self.queries.query(Queries.all_contribs(years))) \
            .get("data", {}) \
            .get("viewer", {}).values()
        for year in by_year:
            self._total_contributions += year \
                .get("contributionCalendar", {}) \
                .get("totalContributions", 0)
        return self._total_contributions

    @property
    async def lines_changed(self) -> Tuple[int, int]:
        """
        :return: count of total lines added, removed, or modified by the user
        """
        if self._lines_changed is not None:
            return self._lines_changed

        def progress_line(done: int, total: int, width: int = 30) -> str:
            ratio = 1.0 if total == 0 else done / total
            filled = int(width * ratio)
            bar = "█" * filled + "-" * (width - filled)
            return f"[lines_changed] [{bar}] {ratio * 100:6.2f}% ({done}/{total})"

        def render_status(done: int, total: int, repo_msg: str) -> None:
            # Keep a 2-line live view: line1=progress bar, line2=current repo
            sys.stdout.write("\033[2F")
            sys.stdout.write("\033[2K" + progress_line(done, total) + "\n")
            sys.stdout.write("\033[2K" + f"[lines_changed] repo: {repo_msg}\n")
            sys.stdout.flush()

        additions = 0
        deletions = 0
        repos = sorted(await self.all_repos)
        total_repos = len(repos)
        print(progress_line(0, total_repos))
        print("[lines_changed] repo: waiting...")

        for idx, repo in enumerate(repos, start=1):
            render_status(idx - 1, total_repos, f"scanning {repo}")
            repo_additions_before = additions
            repo_deletions_before = deletions
            repo_commit_count = 0
            page = 1
            had_any_commit = False
            while True:
                commits = await self.queries.query_rest(
                    f"/repos/{repo}/commits",
                    params={
                        "author": self.username,
                        "per_page": 100,
                        "page": page
                    }
                )
                if not isinstance(commits, list) or len(commits) == 0:
                    break

                had_any_commit = True
                for commit in commits:
                    sha = commit.get("sha", "") if isinstance(commit, dict) else ""
                    if not sha:
                        continue
                    repo_commit_count += 1
                    commit_detail = await self.queries.query_rest(
                        f"/repos/{repo}/commits/{sha}"
                    )
                    if not isinstance(commit_detail, dict):
                        continue
                    stats = commit_detail.get("stats", {})
                    additions += stats.get("additions", 0)
                    deletions += stats.get("deletions", 0)

                if len(commits) < 100:
                    break
                page += 1
            if had_any_commit:
                render_status(
                    idx,
                    total_repos,
                    f"done {repo} | commits={repo_commit_count}, "
                    f"+{additions - repo_additions_before}/-{deletions - repo_deletions_before}",
                )
            else:
                render_status(idx, total_repos, f"done {repo} | no commits by {self.username}")

        print(f"[lines_changed] Finished. total additions=+{additions}, deletions=-{deletions}")

        self._lines_changed = (additions, deletions)
        return self._lines_changed

    @property
    async def views(self) -> int:
        """
        Note: only returns views for the last 14 days (as-per GitHub API)
        :return: total number of page views the user's projects have received
        """
        if self._views is not None:
            return self._views

        total = 0
        repos_for_views = self._repos_with_push
        if repos_for_views is None:
            await self.get_stats()
            repos_for_views = self._repos_with_push
        for repo in sorted(repos_for_views or set()):
            r = await self.queries.query_rest(f"/repos/{repo}/traffic/views")
            for view in r.get("views", []):
                total += view.get("count", 0)

        self._views = total
        return total


###############################################################################
# Main Function
###############################################################################

async def main() -> None:
    """
    Used mostly for testing; this module is not usually run standalone
    """
    access_token = os.getenv("ACCESS_TOKEN")
    user = os.getenv("GITHUB_ACTOR")
    async with aiohttp.ClientSession() as session:
        s = Stats(user, access_token, session)
        print(await s.to_str())


if __name__ == "__main__":
    asyncio.run(main())
