import json
from pathlib import Path
from jira import JIRA
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context

CONFIG_FILE = Path("jira_config.json")


def load_config() -> dict:
    """Load JIRA credentials from a config file or prompt the user."""
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open() as f:
            return json.load(f)

    base_url = input("JIRA URL (e.g. https://your-domain.atlassian.net): ").strip()
    username = input("JIRA username/email: ").strip()
    api_token = input("JIRA API token: ").strip()

    data = {"base_url": base_url, "username": username, "api_token": api_token}
    with CONFIG_FILE.open("w") as f:
        json.dump(data, f)
    print(f"Saved credentials to {CONFIG_FILE}")
    return data


def start_server() -> None:
    creds = load_config()
    jira = JIRA(server=creds["base_url"], basic_auth=(creds["username"], creds["api_token"]))

    server = FastMCP(name="JiraBot")

    @server.tool()
    def search_issues(jql: str, ctx: Context) -> str:
        """Return summaries for the first few issues matching JQL."""
        issues = jira.search_issues(jql, maxResults=5)
        if not issues:
            return "No issues found."
        return "\n".join(f"{i.key}: {i.fields.summary}" for i in issues)

    server.run()


def main() -> None:
    try:
        start_server()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
