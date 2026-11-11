import re
import unittest
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / 'Surge/Apple-Core-DIRECT.list'
SIRI = 'https://raw.githubusercontent.com/RocM301/Apple-Rule/refs/heads/main/Apple-AI.list'
APPLE = 'https://fastly.jsdelivr.net/gh/dler-io/Rules@main/Surge/Surge%203/Provider/Apple.list'
SPECIAL = 'https://fastly.jsdelivr.net/gh/dler-io/Rules@main/Surge/Surge%203/Provider/Special.list'
TV = 'https://fastly.jsdelivr.net/gh/dler-io/Rules@main/Surge/Surge%203/Provider/Media/Apple%20TV.list'
AI = 'https://fastly.jsdelivr.net/gh/dler-io/Rules@main/Surge/Surge%203/Provider/AI%20Suite.list'

def parse(text):
    return [tuple(x.strip() for x in line.split(',')) for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith(('#', ';', '//'))]

def matches(rules, domain):
    d = domain.lower()
    for rule in rules:
        if len(rule) < 2: continue
        kind, value = rule[:2]; value = value.lower()
        if kind == 'DOMAIN' and d == value: return rule
        if kind == 'DOMAIN-SUFFIX' and (d == value or d.endswith('.' + value)): return rule
        if kind == 'DOMAIN-KEYWORD' and value in d: return rule
    return None

def fetch(url):
    with urllib.request.urlopen(url, timeout=20) as response:
        return parse(response.read().decode('utf-8-sig'))

class TestRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = parse(RULES.read_text())
        cls.siri, cls.ai, cls.special, cls.tv, cls.apple = map(fetch, [SIRI, AI, SPECIAL, TV, APPLE])
    def test_format_unique_and_no_broad_rules(self):
        self.assertEqual(len(self.core), len(set(self.core)))
        for rule in self.core:
            self.assertEqual(len(rule), 2)
            self.assertIn(rule[0], ('DOMAIN', 'DOMAIN-SUFFIX'))
            self.assertRegex(rule[1], r'^[a-z0-9.-]+$')
            self.assertNotIn(rule[1], ('apple.com', 'icloud.com', 'mzstatic.com', 'itunes.apple.com'))
    def test_critical_siri_first(self):
        for domain in ('guzzoni.apple.com', 'api.smoot.apple.com', 'apple-relay.apple.com',
                       'cp4.cloudflare.com', 'gateway.icloud.com', 'mask.icloud.com'):
            with self.subTest(domain=domain): self.assertIsNotNone(matches(self.siri, domain))
    def test_core_examples(self):
        for domain in ('account.apple.com', 'idmsa.apple.com', 'gsa.apple.com',
                       'foo.apple-cloudkit.com', 'foo.icloud-content.com', 'iosapps.itunes.apple.com'):
            with self.subTest(domain=domain): self.assertIsNotNone(matches(self.core, domain))
    def test_shared_hosts_not_in_core(self):
        for domain in ('gateway.icloud.com', 'mask.icloud.com', 'apple-relay.apple.com',
                       'guzzoni.apple.com', 'api.smoot.apple.com', 'apps.mzstatic.com'):
            with self.subTest(domain=domain): self.assertIsNone(matches(self.core, domain))
    def test_actual_order_siri_before_special_and_core(self):
        for domain in ('guzzoni.apple.com', 'guzzoni.smoot.apple.com', 'gateway.icloud.com', 'apps.mzstatic.com'):
            result = next((name for name, rules in [('Siri AI', self.siri), ('AI Suite', self.ai),
                ('Special', self.special), ('Apple TV', self.tv), ('Core', self.core), ('Apple', self.apple)]
                if matches(rules, domain)), None)
            with self.subTest(domain=domain): self.assertEqual(result, 'Siri AI')
    def test_tv_precedes_apple_fallback(self):
        self.assertTrue(matches(self.tv, 'tv.apple.com'))
        self.assertTrue(matches(self.apple, 'tv.apple.com'))

if __name__ == '__main__': unittest.main()
