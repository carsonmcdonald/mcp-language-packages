from fastmcp import FastMCP, Context
from typing import Annotated
from pydantic import Field
from package_search.search_providers import get_package_search, get_known_package_languages

import logging

logging.basicConfig(filename='/tmp/app.log', level=logging.DEBUG)

mcp = FastMCP(name="Language Packages")

@mcp.tool()
def package_languages() -> list:
    """Provides a list of known programming languages that packages can be fetched for."""
    return get_known_package_languages()

@mcp.tool()
async def find_packages(
    language: Annotated[str, Field(description="A known programming language.")],
    search: Annotated[str, Field(description="The search value used to find potential packages.")],
    ctx: Context
) -> list:
    """Find packages for a language by searching."""

    try:
        await ctx.debug(f"{language}, {search}")
        package_search = get_package_search(language)
        if package_search is None:
            return []
        else:
            return package_search.search(search)
    except Exception as e:
        logging.error(f"Error fetching packages: {e}")

    return []

if __name__ == "__main__":
    mcp.run()
