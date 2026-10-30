"""Check source identity and prevent off-site or mismatched source URLs."""
import unittest
from official_sources import valid_official_source


class OfficialSourceTests(unittest.TestCase):
    def notice(self, url):
        return {'id': '2026-21824', 'publicationDate': '2026-10-27', 'officialUrl': url}

    def test_official_gpo_publication(self):
        self.assertTrue(valid_official_source(self.notice('https://www.govinfo.gov/content/pkg/FR-2026-10-27/html/2026-21824.htm')))

    def test_federal_register_rendition(self):
        self.assertTrue(valid_official_source(self.notice('https://www.federalregister.gov/documents/2026/10/27/2026-21824/mattresses-determinations')))

    def test_wrong_notice_or_publication_date(self):
        for url in ('https://www.govinfo.gov/content/pkg/FR-2026-10-27/html/2026-21853.htm',
                    'https://www.govinfo.gov/content/pkg/FR-2026-10-26/html/2026-21824.htm',
                    'https://www.federalregister.gov/documents/2026/10/26/2026-21824/mattresses'):
            with self.subTest(url=url):
                self.assertFalse(valid_official_source(self.notice(url)))

    def test_unsafe_or_unexpected_destination(self):
        for url in ('http://www.govinfo.gov/content/pkg/FR-2026-10-27/html/2026-21824.htm',
                    'https://www.govinfo.gov.example.com/content/pkg/FR-2026-10-27/html/2026-21824.htm',
                    'https://name@www.govinfo.gov/content/pkg/FR-2026-10-27/html/2026-21824.htm',
                    'https://www.govinfo.gov/content/pkg/FR-2026-10-27/html/2026-21824.htm?redirect=elsewhere'):
            with self.subTest(url=url):
                self.assertFalse(valid_official_source(self.notice(url)))


if __name__ == '__main__':
    unittest.main()
