import unittest
import io

class test_ip2asn(unittest.TestCase):
    def get_first_20_rows_v4_ints(self):
        """Hard coded first 20 rows of one copy of the database"""
        return io.StringIO("""16777216	16777471	13335	US	CLOUDFLARENET - Cloudflare, Inc.
16777472	16778239	0	None	Not routed
16778240	16779263	56203	AU	GTELECOM-AUSTRALIA Gtelecom-AUSTRALIA
16779264	16781311	0	None	Not routed
16781312	16781567	2519	JP	VECTANT ARTERIA Networks Corporation
16781568	16793599	0	None	Not routed
16793600	16809983	18144	JP	AS-ENECOM Energia Communications,Inc.
16809984	16834047	23969	TH	TOT-NET TOT Public Company Limited
16834048	16842751	23969	TH	TOT-NET TOT Public Company Limited
16842752	16843007	0	None	Not routed
16843008	16843008	13335	US	CLOUDFLARENET - Cloudflare, Inc.
16843009	16843009	7497	CN	CSTNET-AS-AP Computer Network Information Center
16843010	16843263	13335	US	CLOUDFLARENET - Cloudflare, Inc.
16843264	16844287	0	None	Not routed
16844288	16844543	138449	HK	SYUNET-AS-AP SIANG YU SCIENCE AND TECHNOLOGY LIMITED
16844544	16844799	0	None	Not routed
16844800	16845055	4134	CN	CHINANET-BACKBONE No.31,Jin-rong Street
16845056	16847871	0	None	Not routed
16847872	16848127	133948	HK	DIL-AS-AP DONGFONG INC LIMITED
16848128	16859135	0	None	Not routed
""")

    def get_first_20_rows_v4_ascii(self):
        """Get the hard coded list of first 20 rows of the non-int version."""

        return io.StringIO("""1.0.0.0	1.0.0.255	13335	US	CLOUDFLARENET - Cloudflare, Inc.
1.0.1.0	1.0.3.255	0	None	Not routed
1.0.4.0	1.0.7.255	56203	AU	GTELECOM-AUSTRALIA Gtelecom-AUSTRALIA
1.0.8.0	1.0.15.255	0	None	Not routed
1.0.16.0	1.0.16.255	2519	JP	VECTANT ARTERIA Networks Corporation
1.0.17.0	1.0.63.255	0	None	Not routed
1.0.64.0	1.0.127.255	18144	JP	AS-ENECOM Energia Communications,Inc.
1.0.128.0	1.0.221.255	23969	TH	TOT-NET TOT Public Company Limited
1.0.222.0	1.0.255.255	23969	TH	TOT-NET TOT Public Company Limited
1.1.0.0	1.1.0.255	0	None	Not routed
1.1.1.0	1.1.1.0	13335	US	CLOUDFLARENET - Cloudflare, Inc.
1.1.1.1	1.1.1.1	7497	CN	CSTNET-AS-AP Computer Network Information Center
1.1.1.2	1.1.1.255	13335	US	CLOUDFLARENET - Cloudflare, Inc.
1.1.2.0	1.1.5.255	0	None	Not routed
1.1.6.0	1.1.6.255	138449	HK	SYUNET-AS-AP SIANG YU SCIENCE AND TECHNOLOGY LIMITED
1.1.7.0	1.1.7.255	0	None	Not routed
1.1.8.0	1.1.8.255	4134	CN	CHINANET-BACKBONE No.31,Jin-rong Street
1.1.9.0	1.1.19.255	0	None	Not routed
1.1.20.0	1.1.20.255	133948	HK	DIL-AS-AP DONGFONG INC LIMITED
1.1.21.0	1.1.63.255	0	None	Not routed
""")

    def get_first_20_rows_v6(self):
        """return the first 20 rows of a v6 database sample"""
        return io.StringIO("""::	::1	0	None	Not routed
64:ff9b::1:0:0	100::ffff:ffff:ffff:ffff	0	None	Not routed
100:0:0:1::	2001:0:ffff:ffff:ffff:ffff:ffff:ffff	0	None	Not routed
2001:1::	2001:4:111:ffff:ffff:ffff:ffff:ffff	0	None	Not routed
2001:4:112::	2001:4:112:ffff:ffff:ffff:ffff:ffff	112	US	ROOTSERV - DNS-OARC
2001:4:113::	2001:c0:2:ffff:ffff:ffff:ffff:ffff	0	None	Not routed
2001:c0:3::	2001:c0:3:ffff:ffff:ffff:ffff:ffff	22884	MX	TOTAL PLAY TELECOMUNICACIONES SA DE CV
2001:c0:4::	2001:1ff:ffff:ffff:ffff:ffff:ffff:ffff	0	None	Not routed
2001:200::	2001:200:5ff:ffff:ffff:ffff:ffff:ffff	2500	JP	WIDE-BB WIDE Project
2001:200:600::	2001:200:6ff:ffff:ffff:ffff:ffff:ffff	7667	JP	KDDLAB KDDI R&D Laboratories, INC.
2001:200:700::	2001:200:8ff:ffff:ffff:ffff:ffff:ffff	2500	JP	WIDE-BB WIDE Project
2001:200:900::	2001:200:9ff:ffff:ffff:ffff:ffff:ffff	7660	JP	APAN-JP Asia Pacific Advanced Network - Japan
2001:200:a00::	2001:200:bfff:ffff:ffff:ffff:ffff:ffff	2500	JP	WIDE-BB WIDE Project
2001:200:c000::	2001:200:dfff:ffff:ffff:ffff:ffff:ffff	23634	JP	E-DNS-JP WIDE Project
2001:200:e000::	2001:200:ffff:ffff:ffff:ffff:ffff:ffff	7660	JP	APAN-JP Asia Pacific Advanced Network - Japan
2001:201::	2001:217:ffff:ffff:ffff:ffff:ffff:ffff	0	None	Not routed
2001:218::	2001:218:21ff:ffff:ffff:ffff:ffff:ffff	2914	US	NTT-COMMUNICATIONS-2914 - NTT America, Inc.
2001:218:2200::	2001:218:22ff:ffff:ffff:ffff:ffff:ffff	18259	JP	HIGE NTT Communications Corporation
2001:218:2300::	2001:218:3003:ffff:ffff:ffff:ffff:ffff	2914	US	NTT-COMMUNICATIONS-2914 - NTT America, Inc.
2001:218:3004::	2001:218:3004:ffff:ffff:ffff:ffff:ffff	20940	EU	AKAMAI-ASN1""")

    def test_load(self):
        import ip2asn
        self.assertTrue(ip2asn, "Successfully loaded ip2asn")

        # create a class
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v4_ints())
        self.assertTrue(i2a, "Successfully created a class")

    def test_lookup_address_row(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v4_ints())

        result = i2a.lookup_address_row("1.1.1.2")
        print(result)
        self.assertTrue(isinstance(result, list), "properly returned a list")

    def test_lookup_address(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v4_ints())

        result = i2a.lookup_address("1.1.1.2")
        self.assertTrue(isinstance(result, dict), "properly returned a dict")
        self.assertEqual(result,
                         {'ip_text': '1.1.1.2',
                          'ip_numeric': 16843010,
                          'ip_range': [16843010, 16843263],
                          'ASN': '13335',
                          'country': 'US',
                          'owner': 'CLOUDFLARENET - Cloudflare, Inc.'},
                         "Data returned matched expected")
    
    def test_lookup_with_non_numeric(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v4_ascii())

        result = i2a.lookup_address("1.1.1.2")
        self.assertTrue(isinstance(result, dict), "properly returned a dict")
        self.assertEqual(result,
                         {'ip_text': '1.1.1.2',
                          'ip_numeric': 16843010,
                          'ip_range': [16843010, 16843263],
                          'ASN': '13335',
                          'country': 'US',
                          'owner': 'CLOUDFLARENET - Cloudflare, Inc.'},
                         "Data returned matched expected")
        
    def test_lookup_with_ipv6(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v6(), ipversion=6)

        result = i2a.lookup_address("2001:200::42")
        self.assertTrue(isinstance(result, dict), "properly returned a dict")
        self.assertEqual(result,
                         {'ip_text': '2001:200::42',
                          'ip_numeric': 42540528726795050063891204319802818626,
                          'ip_range': [42540528726795050063891204319802818560,
                                       42540528728651960122819274732151504895],
                          'ASN': '2500',
                          'country': 'JP',
                          'owner': 'WIDE-BB WIDE Project'},
                         "v6 Data returned matched expected")
        
    def test_lookup_with_ipvunknown(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v6(), ipversion=None)

        result = i2a.lookup_address("2001:200::42")
        self.assertTrue(isinstance(result, dict), "properly returned a dict")
        self.assertEqual(result,
                         {'ip_text': '2001:200::42',
                          'ip_numeric': 42540528726795050063891204319802818626,
                          'ip_range': [42540528726795050063891204319802818560,
                                       42540528728651960122819274732151504895],
                          'ASN': '2500',
                          'country': 'JP',
                          'owner': 'WIDE-BB WIDE Project'},
                         "v6 Data returned matched expected")
        

    def test_lookup_asn(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows_v6(), ipversion=None)
        
        result = i2a.lookup_asn("2914")
        self.assertTrue(isinstance(result, list), "properly returned an list")

        self.assertEqual(len(result), 2, "properly returned 2 elements")

        result = i2a.lookup_asn(2914, limit=1)
        self.assertEqual(len(result), 1,
                         "properly returned 1 element when limited")

        self.assertEqual(result,
                         [{'ip_range': [42540530628270950406235306564857626624,
                                       42540530638793440740161038901500182527], 
                           'ASN': '2914', 
                           'country': 'US', 
                           'owner': 'NTT-COMMUNICATIONS-2914 - NTT America, Inc.'}], 
                         "returned expected results")
