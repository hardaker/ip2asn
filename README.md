# Objective

A python class to search [ip2asn] information for matches.

[ip2asn]: https://iptoasn.com/

# Installation

Using pip:

```
pip3 install ip2asn
```

Or manually:

```
git clone git@github.com:hardaker/ip2asn.git
cd ip2asn
python3 setup.py build
python3 setup.py install
```

# Example Usage

## setup

``` sh
curl -o ip2asn-v4-u32.tsv.gz https://iptoasn.com/data/ip2asn-v4-u32.tsv.gz
gunzip ip2asn-v4-u32.tsv.gz

```

## Coding

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

# Author

Wes Hardaker, USC/ISI

