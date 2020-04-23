import unittest
import io

class test_ip2asn(unittest.TestCase):
    def get_first_ten_rows(self):
        """Hard coded first ten rows of one copy of the database"""
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
""")

    def test_load(self):
        import ip2asn
        self.assertTrue(ip2asn, "Successfully loaded ip2asn")

        # create a class
        i2a = ip2asn.IP2ASN(self.get_first_ten_rows())
        self.assertTrue(i2a, "Successfully created a class")

    
