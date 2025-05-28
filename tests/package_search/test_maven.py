import unittest
import json
import pytest

from package_search.maven_package_search import MavenPackageSearch # type: ignore

@pytest.fixture(scope="class")
def sample_search_response(request):
    with open('tests/package_search/maven-search-response.json', 'r') as file:
        request.cls.data = json.loads(file.read())

@pytest.mark.usefixtures("sample_search_response")
class TestMavenPackageSearc(unittest.TestCase):
    data = dict()

    def test_upper(self):
        maven = MavenPackageSearch()
        urls = maven._extract_pom_urls(self.data)

        self.assertEqual(urls, [
            'https://repo1.maven.org/maven2/org/openidentityplatform/commons/guice/2.2.4/guice-2.2.4.pom',
            'https://repo1.maven.org/maven2/io/github/replay-framework/guice/2.6.3/guice-2.6.3.pom',
            'https://repo1.maven.org/maven2/com/codeborne/replay/guice/2.3.1/guice-2.3.1.pom',
            'https://repo1.maven.org/maven2/io/github/qsy7/java/modules/ssh/providers/guice/0.3.4/guice-0.3.4.pom',
            'https://repo1.maven.org/maven2/io/github/qsy7/java/infrastructure/inject/providers/guice/0.3.3/guice-0.3.3.pom'
        ])