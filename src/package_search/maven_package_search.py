from typing import List
from package_search.base_package_search import PackageSearch
from requests_cache import CachedSession
import logging

class MavenPackageSearch(PackageSearch):
    """Search Maven packages."""

    def _convert_search_doc(self, doc) -> str:
        artifact_name = doc['a']
        artifact_package = str(doc['g']).replace(".", "/")
        artifact_version = doc['latestVersion']

        return f"https://repo1.maven.org/maven2/{artifact_package}/{artifact_name}/{artifact_version}/{artifact_name}-{artifact_version}.pom"

    def _extract_pom_urls(self, package_json) -> List[str]:
        return list(map(self._convert_search_doc, package_json['response']['docs']))

    def search(self, value) -> List[str]:
        """Use the Maven Central Repository REST API to search, see https://central.sonatype.org/search/rest-api-guide/"""

        logging.debug(f"Making Maven search request for '{value}'")

        with CachedSession() as session:
            package_search_response = session.get('https://search.maven.org/solrsearch/select', params={'q': value, 'rows': 5, 'wt': 'json'}, timeout=5)
            if package_search_response.status_code != 200:
                logging.error("Search returned non-200 response.")
                return []
            
            package_json = package_search_response.json()
            
            logging.debug(f"{package_json}")

            pom_urls = self._extract_pom_urls(package_json)

            poms = []
            for url in pom_urls:
                pom_data = session.get(url, timeout=5)
                if pom_data.status_code == 200 and "<description>" in pom_data.text.lower():
                    poms.append(pom_data.text)
                else:
                    logging.debug(f"Skipping {url} data, status code={pom_data.status_code}")

            return poms