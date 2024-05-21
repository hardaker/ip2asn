def test_save_and_load_big_numbers32():
    import ip2asn

    i2a = ip2asn.IP2ASN("/dev/null")

    test_numbers = [
        0, 1, 2**31, 2**32-1, 2**32, 2**32+1, 2**64-1, 2**64+1, 2**128-1
    ]

    converted_numbers = i2a.save_large_numbers32(test_numbers)

    assert test_numbers != converted_numbers

    back_to_ints = i2a.load_large_numbers32(converted_numbers)

    assert test_numbers == back_to_ints


def test_save_and_load_big_numbers64():
    import ip2asn

    i2a = ip2asn.IP2ASN("/dev/null")

    test_numbers = [
        0, 1, 2**31, 2**32-1, 2**32, 2**32+1, 2**64-1, 2**64+1, 2**128-1
    ]

    converted_numbers = i2a.save_large_numbers64(test_numbers)

    assert test_numbers != converted_numbers

    back_to_ints = i2a.load_large_numbers64(converted_numbers)

    assert test_numbers == back_to_ints


def test_data_save_and_load_big_numbers64():
    import ip2asn

    i2a = ip2asn.IP2ASN("/dev/null")

    test_numbers = [
        [0, 1, '1111', 'US', 'BOGUS1'],
        [2**31, 2**32-1, '2222', 'US', 'BOGUS2'],
        [2**32, 2**32+1, '3333', 'US', 'BOGUS3'],
        [2**64+1, 2**128-1, '4444', 'US', 'BOGUS4'],
    ]

    converted_numbers = i2a.save_data_numbers64(test_numbers)

    assert test_numbers != converted_numbers

    back_to_ints = i2a.load_data_numbers64(converted_numbers)

    assert test_numbers == back_to_ints



