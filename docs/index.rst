.. ip2asn documentation master file, created by
   sphinx-quickstart on Thu Jan 16 15:01:57 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

ip2asn -- quickly look up information about IP addresses
========================================================

Installation
------------

::

    $ pip install -u ip2asn


Initialization and your first run
---------------------------------

First we need to download a copy of the ip2asn database, which we can
do using the `--fetch` argument:

::

   $ mkdir $HOME/lib
   $ ip2asn --fetch
   INFO      :     saved new data to /home/hardaker/lib/ip2asn-combined.tsv

Make sure it works and turn on caching to cache the results:

::

   $ ip2asn 170.247.170.2
   Address: 170.247.170.2
     Numeric ip: 2868357634
            ASN: 394353
          Owner: BROOT-AS
        Country: US
       ip_range: 170.247.170.0 - 170.247.171.255

Usage
=====

Searching for IP address details
--------------------------------

By default `ip2asn` will search for details about an IP address.
(Make sure to use the `-C` flag to turn on caching the first time in
order greatly speed future runs).

::

   $ ip2asn 8.8.8.8
   Address: 8.8.8.8
     Numeric ip: 134744072
            ASN: 15169
          Owner: GOOGLE
        Country: US
       ip_range: [134744064, 134744319]   

   

Searching by an ASN number
--------------------------

You can also find information directly about an ASN number using the
`-a` flag:

::

   $ ip2asn -a 394353
            ASN: 394353
          Owner: BROOT-AS
        Country: US
       ip_range: [2868357632, 2868358143]
   
            ASN: 394353
          Owner: BROOT-AS
        Country: US
       ip_range: [3236187904, 3236188159]
   ...

Creating machine readable output
--------------------------------

The `-F` (`--output-fsdb`) flag can generate FSDB formatted output
(basically glorified commented and tab-separated format), which can be
read in easily with the `pyfsdb` module.

::

   $ ip2asn -F 8.8.8.8
   #fsdb -F t address:a ip_numeric:l ASN:a owner:a country:a ip_range
   8.8.8.8 134744072       15169   GOOGLE  US      [134744064, 134744319]
   #  | ip2asn/main.py -F 8.8.8.8

Creating tcpdump filter expressions
-----------------------------------

In addition to generating helpful information, `ip2asn` can also
generate tcpdump filter expressions with the `-T`
(`--output-pcap-filter`) flag.  Although this works with an IP address, it
is far more helpful for generating filters for entire ASNs:

::

   $ ip2asn -T 394353
   ( net 170.247.170.0/23 or net 192.228.79.0/24 or net 199.9.14.0/23 or net 2001:500:84::/48 or net 2001:500:200::/47 or net 2001:500:203::/48 or net 2001:500:204::/46 or net 2001:500:208::/47 or net 2001:500:20a::/47 or net 2001:500:20c::/46 or net 2801:1b8:10::/47 or net 2801:1b8:12::/47 or net 2801:1b8:14::/46 or net 2801:1b8:18::/45 )

Using ip2asn in python code
===========================

Using `ip2asn` in code is fairly simple: create an object initialized
with the `ip2asn` database to load, and make queries against it.

Searching by IP address
-----------------------


.. code-block::

   import ip2asn
   i2a = ip2asn.IP2ASN("ip2asn-combined.tsv")

   # search by address
   results = i2a.lookup_address("8.8.8.8")
   print(results)

Searching by ASN number
-----------------------

.. code-block::

   import ip2asn
   i2a = ip2asn.IP2ASN("ip2asn-combined.tsv")

   # search by ASN
   results = i2a.lookup_asn(15169)
   print(results)


Related Projects
================

* The most excellent `iptoasn <https://iptoasn.com/>`_ project that generates the data resource that `ip2asn` is built around.
* `traffic-taffy <https://traffic-taffy.readthedocs.io/>`_: dissects and compares pcap files
* `pyfsdb <https://fsdb.readthedocs.io/>`_: reads tab-separated FSDB formatted files

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
