from package_search.base_package_search import PackageSearch 
from requests_cache import CachedSession
import logging

class NPMPackageSearch(PackageSearch):
    """Search NPM packages."""

    def search(self, value) -> list:
        """Search using the NPM registry API."""

        logging.debug(f"Making NPM search request for '{value}'")

        with CachedSession() as session:
            package_search_response = session.get('https://registry.npmjs.org/-/v1/search', params={'text': value, 'size': 5}, timeout=5)
            package_json = package_search_response.json()
            
            logging.debug(f"{package_json}")

            return package_json['objects']