import unittest
import io

class test_ip2asn(unittest.TestCase):
    def get_first_20_rows(self):
        """Hard coded first 20 rows of one copy of the database"""
        return io.StringIO("""16777216	16777471	13335	US	CLOUDFLARENET - Cloudflare, Inc.
16777472	16778239	0	None	Not routed
16778240	16779263	56203	AU	GTELECOM-AUSTRALIA Gtelecom-AUSTRALIA
16779264	16781311	0	None	Not routed
16781312	16781567	2519	JP	VECTANT ARTERIA Networks Corporation
16781568	16793599	0	None	Not routed
16793600	16809983	18144	JP	AS-ENECOM Energia Communications,Inc.
16809984	16810495	23969	TH	TOT-NET TOT Public Company Limited
16810496	16813055	23969	TH	TOT-NET TOT Public Company Limited
16813056	16832511	23969	TH	TOT-NET TOT Public Company Limited
16832512	16842751	23969	TH	TOT-NET TOT Public Company Limited
16842752	16843007	0	None	Not routed
16843008	16843263	13335	US	CLOUDFLARENET - Cloudflare, Inc.
16843264	16844287	0	None	Not routed
16844288	16844543	138449	HK	SYUNET-AS-AP SIANG YU SCIENCE AND TECHNOLOGY LIMITED
16844544	16844799	0	None	Not routed
16844800	16845055	4134	CN	CHINANET-BACKBONE No.31,Jin-rong Street
16845056	16847871	0	None	Not routed
16847872	16848127	133948	HK	DIL-AS-AP DONGFONG INC LIMITED
16848128	16859135	0	None	Not routed
""")

    def test_load(self):
        import ip2asn
        self.assertTrue(ip2asn, "Successfully loaded ip2asn")

        # create a class
        i2a = ip2asn.IP2ASN(self.get_first_20_rows())
        self.assertTrue(i2a, "Successfully created a class")

    def test_lookup_address_row(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows())

        result = i2a.lookup_address_row("1.1.1.1")
        print(result)
        self.assertTrue(isinstance(result, list), "properly returned a list")

    def test_lookup_address(self):
        import ip2asn
        i2a = ip2asn.IP2ASN(self.get_first_20_rows())

        result = i2a.lookup_address("1.1.1.1")
        self.assertTrue(isinstance(result, dict), "properly returned a list")
        self.assertEqual(result,
                         {'ip_text': '1.1.1.1',
                          'ip_numeric': 16843009,
                          'ip_range': [16843008, 16843263],
                          'ASN': '13335',
                          'country': 'US',
                          'owner': 'CLOUDFLARENET - Cloudflare, Inc.'},
                         "Data returned matched expected")
        
