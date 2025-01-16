# Objective

A python class to search [ip2asn] information for matches.

[ip2asn]: https://iptoasn.com/

See the [pretty documentation] over on *readthedocs*.

[pretty documentation]: https://ip2asn.readthedocs.io/en/latest/

# Installation

Using pip or pipx:

```
pipx install ip2asn
```

# Example Usage

## setup

``` sh
ip2asn -f ip2asn.db --fetch
```

## command line

### Searching for an address

``` sh
# ip2asn 8.8.8.8

Address: 8.8.8.8
  Numeric ip: 134744072
         ASN: 15169
       Owner: GOOGLE - Google LLC
     Country: US
    ip_range: [134744064, 134744319]
```

### Searching for an ASN

``` sh
# ip2asn -a 15169

         ASN: 15169
       Owner: GOOGLE - Google LLC
     Country: US
    ip_range: [134743040, 134743295]

         ASN: 15169
       Owner: GOOGLE - Google LLC
     Country: US
    ip_range: [134744064, 134744319]

         ASN: 15169
       Owner: GOOGLE - Google LLC
...
(google has a lot of registrations)
```

### Displaying a tcpdump / libpcap filter given a address or ASN

``` sh
# ip2asn -T -a 15169
( net 8.8.4.0/24 or net 8.8.8.0/24 or net 8.35.200.0/21 or ....
```

## Coding

### Searching by IP address

```
import ip2asn
i2a = ip2asn.IP2ASN("ip2asn-v4-u32.tsv")
result = i2a.lookup_address("93.184.216.34")

import pprint
pprint.pprint(result)
```

**Produces:**

``` text
{'ASN': '15133',
 'country': 'US',
 'ip_numeric': 1572395042,
 'ip_range': [1572394752, 1572396543],
 'ip_text': '93.184.216.34',
 'owner': 'EDGECAST - MCI Communications Services, Inc. d/b/a Verizon Business'}
```

### Searching by ASN

``` python
import ip2asn
i2a = ip2asn.IP2ASN("ip2asn-combined.tsv")
results = i2a.lookup_asn(15169, limit=2)  # limit is optional

import pprint
pprint.pprint(results)
``**

**Produces:**

``` text
[{'ASN': '15169',
  'country': 'US',
  'ip_range': [134743040, 134743295],
  'owner': 'GOOGLE - Google LLC'},
 {'ASN': '15169',
  'country': 'US',
  'ip_range': [134744064, 134744319],
  'owner': 'GOOGLE - Google LLC'}]
```

# Author

Wes Hardaker, USC/ISI

