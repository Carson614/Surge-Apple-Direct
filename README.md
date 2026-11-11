# Surge Apple Core Direct

Conservative Apple core routing for Surge. Place your Siri / AI and Apple TV rules first, then this rule set with `DIRECT`, then a separately maintained Apple fallback with `Proxy`. Rule order is decisive.

```ini
RULE-SET,https://raw.githubusercontent.com/Carson614/Surge-Apple-Direct/main/Surge/Apple-Core-DIRECT.list,DIRECT
```

Coverage is intentionally limited to Apple Account, selected iCloud/CloudKit service families, known software download and certificate hosts. No blanket apple.com, icloud.com, mzstatic.com, itunes.apple.com, or Apple IP block is included. CloudKit and iCloud content families are shared platforms, so this is not proof that every future request under those families is unrelated to AI. Hosts and service behavior change; validate on actual devices. Apple's network documentation identifies reachability, not guaranteed direct routing in any specific country.

Potentially shared / unresolved: gateway.icloud.com, mask*.icloud.com, apple-relay.*, guzzoni, smoot, broad itunes.apple.com, mzstatic.com and cdn-apple.com, and APNs destination IPs. No blanket direct rule is added for these. Existing Siri/AI and Special rule sets may cover or intercept individual hosts; inspect the complete effective configuration and modules.

Sources: [Apple enterprise networks](https://support.apple.com/en-us/101555), [Sukka Apple services](https://github.com/SukkaW/Surge/blob/master/Source/non_ip/apple_services.conf), [blackmatrix7 Apple rules](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Surge/Apple). The rules are manually curated, not copied wholesale.

Run `python3 -m unittest discover -s tests -v`. The integration test downloads the current referenced rule sets and is subject to network availability; it models hostname matches only, not DNS, IP, process, user-agent, module, or actual device behavior.
