from typing import Dict
from package_search.base_package_search import PackageSearch
from package_search.npm_package_search import NPMPackageSearch
from package_search.maven_package_search import MavenPackageSearch

available_search: Dict[str, PackageSearch]  = dict.fromkeys(['javascript', 'typescript'], NPMPackageSearch())
available_search.update(dict.fromkeys(['java', 'kotlin'], MavenPackageSearch()))

def get_known_package_languages() -> list:
    return list(available_search.keys())

def get_package_search(language: str) -> PackageSearch | None:
    return available_search[language.lower()]