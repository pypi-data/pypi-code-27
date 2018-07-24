#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys

import _pyhash

fnv1_32 = _pyhash.fnv1_32
fnv1a_32 = _pyhash.fnv1a_32
fnv1_64 = _pyhash.fnv1_64
fnv1a_64 = _pyhash.fnv1a_64

murmur1_32 = _pyhash.murmur1_32
murmur1_aligned_32 = _pyhash.murmur1_aligned_32
murmur2_32 = _pyhash.murmur2_32
murmur2a_32 = _pyhash.murmur2a_32
murmur2_aligned_32 = _pyhash.murmur2_aligned_32
murmur2_neutral_32 = _pyhash.murmur2_neutral_32
murmur2_x64_64a = _pyhash.murmur2_x64_64a
murmur2_x86_64b = _pyhash.murmur2_x86_64b
murmur3_32 = _pyhash.murmur3_32
murmur3_x86_128 = _pyhash.__dict__.get('murmur3_x86_128')
murmur3_x64_128 = _pyhash.__dict__.get('murmur3_x64_128')

lookup3 = _pyhash.lookup3_little if sys.byteorder == 'little' else _pyhash.lookup3_big
lookup3_little = _pyhash.lookup3_little
lookup3_big = _pyhash.lookup3_big

super_fast_hash = _pyhash.super_fast_hash

city_32 = _pyhash.city_32
city_64 = _pyhash.city_64
city_128 = _pyhash.__dict__.get('city_128')
city_crc_128 = _pyhash.__dict__.get('city_crc_128')

spooky_32 = _pyhash.spooky_32
spooky_64 = _pyhash.spooky_64
spooky_128 = _pyhash.__dict__.get('spooky_128')

farm_32 = _pyhash.__dict__.get('farm_32')
farm_64 = _pyhash.__dict__.get('farm_64')
farm_128 = _pyhash.__dict__.get('farm_128')

metro_64 = metro_64_1 = _pyhash.metro_64_1
metro_64_2 = _pyhash.metro_64_2
metro_128 = metro_128_1 = _pyhash.__dict__.get('metro_128_1')
metro_128_2 = _pyhash.__dict__.get('metro_128_2')
metro_crc_64 = metro_crc_64_1 = _pyhash.metro_64_crc_1
metro_crc_64_2 = _pyhash.metro_64_crc_2
metro_crc_128 = metro_crc_128_1 = _pyhash.__dict__.get('metro_128_crc_1')
metro_crc_128_2 = _pyhash.__dict__.get('metro_128_crc_2')

mum_64 = _pyhash.mum_64

t1_32 = _pyhash.t1_32
t1_32_be = _pyhash.t1_32_be
t1_64 = _pyhash.t1_64
t1_64_be = _pyhash.t1_64_be

xx_32 = _pyhash.xx_32
xx_64 = _pyhash.xx_64

import unittest
import logging


class TestHasher(unittest.TestCase):
    def setUp(self):
        self.data = b'test'
        self.udata = 'test'

    def doTest(self, hasher_type, bytes_hash, seed_hash, unicode_hash):
        if hasher_type:
            hasher = hasher_type()

            self.assertEqual(bytes_hash, hasher(self.data))

            self.assertEqual(seed_hash, hasher(self.data, seed=bytes_hash))

            self.assertEqual(seed_hash, hasher(self.data, self.data))

            self.assertEqual(unicode_hash, hasher(self.udata))


class TestFNV1(TestHasher):
    def testFNV1_32(self):
        self.doTest(hasher_type=fnv1_32,
                    bytes_hash=3698262380,
                    seed_hash=660137056,
                    unicode_hash=3910690890)

    def testFNV1a_32(self):
        self.doTest(hasher_type=fnv1a_32,
                    bytes_hash=1858026756,
                    seed_hash=1357873952,
                    unicode_hash=996945022)

    def testFNV1_64(self):
        self.doTest(hasher_type=fnv1_64,
                    bytes_hash=17151984479173897804,
                    seed_hash=6349570372626520864,
                    unicode_hash=14017453969697934794)

    def testFNV1a_64(self):
        self.doTest(hasher_type=fnv1a_64,
                    bytes_hash=11830222609977404196,
                    seed_hash=8858165303110309728,
                    unicode_hash=14494269412771327550)


class TestMurMurHash(TestHasher):
    def testMurMurHash1_32(self):
        self.doTest(hasher_type=murmur1_32,
                    bytes_hash=1706635965,
                    seed_hash=1637637239,
                    unicode_hash=2296970802)

    def testMurMurHash1Aligned_32(self):
        self.doTest(hasher_type=murmur1_aligned_32,
                    bytes_hash=1706635965,
                    seed_hash=1637637239,
                    unicode_hash=2296970802)

    def testMurMurHash2_32(self):
        self.doTest(hasher_type=murmur2_32,
                    bytes_hash=403862830,
                    seed_hash=1257009171,
                    unicode_hash=2308212514)

    def testMurMurHash2a_32(self):
        self.doTest(hasher_type=murmur2a_32,
                    bytes_hash=1026673864,
                    seed_hash=3640713775,
                    unicode_hash=3710634486)

    def testMurMurHash2Aligned32(self):
        self.doTest(hasher_type=murmur2_aligned_32,
                    bytes_hash=403862830,
                    seed_hash=1257009171,
                    unicode_hash=2308212514)

    def testMurMurHash2Neutral32(self):
        self.doTest(hasher_type=murmur2_neutral_32,
                    bytes_hash=403862830,
                    seed_hash=1257009171,
                    unicode_hash=2308212514)

    def testMurMurHash2_x64_64a(self):
        self.doTest(hasher_type=murmur2_x64_64a,
                    bytes_hash=3407684658384555107,
                    seed_hash=14278059344916754999,
                    unicode_hash=9820020607534352415)

    def testMurMurHash2_x86_64b(self):
        self.doTest(hasher_type=murmur2_x86_64b,
                    bytes_hash=1560774255606158893,
                    seed_hash=11567531768634065834,
                    unicode_hash=7104676830630207180)

    def testMurMurHash3_32(self):
        self.doTest(hasher_type=murmur3_32,
                    bytes_hash=3127628307,
                    seed_hash=1973649836,
                    unicode_hash=1351191292)

    def testMurMurHash3_x86_128(self):
        self.doTest(hasher_type=murmur3_x86_128,
                    bytes_hash=113049230771270950235709929058346397488,
                    seed_hash=201730919445129814667855021331871906456,
                    unicode_hash=34467989874860051826961972957664456325)

    def testMurMurHash3_x64_128(self):
        self.doTest(hasher_type=murmur3_x64_128,
                    bytes_hash=204797213367049729698754624420042367389,
                    seed_hash=25000065729391260169145522623652811022,
                    unicode_hash=301054382688326301269845371608405900524)


class TestLookup3(TestHasher):
    def testLookup3(self):
        self.doTest(hasher_type=lookup3,
                    bytes_hash=3188463954,
                    seed_hash=478901866,
                    unicode_hash=1380664715)


class TestSuperFastHash(TestHasher):
    def testSuperFastHash(self):
        self.doTest(hasher_type=super_fast_hash,
                    bytes_hash=942683319,
                    seed_hash=777359542,
                    unicode_hash=1430748046)


class TestCityHash(TestHasher):
    def testCityHash32(self):
        self.doTest(hasher_type=city_32,
                    bytes_hash=1633095781,
                    seed_hash=3687200064,
                    unicode_hash=3574089775)

    def testCityHash64(self):
        self.doTest(hasher_type=city_64,
                    bytes_hash=17703940110308125106,
                    seed_hash=8806864191580960558,
                    unicode_hash=7557950076747784205)

        self.assertFalse(hasattr(city_64, 'has_sse4_2'))

    def testCityHash128(self):
        self.doTest(hasher_type=city_128,
                    bytes_hash=195179989828428219998331619914059544201,
                    seed_hash=206755929755292977387372217469167977636,
                    unicode_hash=211596129097514838244042408160146499227)

        if hasattr(city_128, 'has_sse4_2'):
            self.assertTrue(city_128.has_sse4_2, "support SSE 4.2")

    def testCityHashCrc128(self):
        self.doTest(hasher_type=city_crc_128,
                    bytes_hash=195179989828428219998331619914059544201,
                    seed_hash=206755929755292977387372217469167977636,
                    unicode_hash=211596129097514838244042408160146499227)


class TestSpookyHash(TestHasher):
    def testSpookyHash32(self):
        self.doTest(hasher_type=spooky_32,
                    bytes_hash=1882037601,
                    seed_hash=1324274298,
                    unicode_hash=2977967976)

    def testSpookyHash64(self):
        self.doTest(hasher_type=spooky_64,
                    bytes_hash=10130480990056717665,
                    seed_hash=1598355329892273278,
                    unicode_hash=4093159241144086376)

    def testSpookyHash128(self):
        self.doTest(hasher_type=spooky_128,
                    bytes_hash=241061513486538422840128476001680072033,
                    seed_hash=315901747311404831226315334184550174199,
                    unicode_hash=207554373952009549684886824908954283880)


class TestFarmHash(TestHasher):
    def testFarmHash32(self):
        hasher = farm_32()

        h1 = hasher(self.data)
        h2 = hasher(self.data, seed=123)
        h3 = hasher(self.udata)

        self.assertTrue(h1 != 0)
        self.assertTrue(h2 != 0)
        self.assertTrue(h3 != 0)
        self.assertNotEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertNotEqual(h2, h3)

    def testFarmHash64(self):
        self.doTest(hasher_type=farm_64,
                    bytes_hash=8581389452482819506,
                    seed_hash=10025340881295800991,
                    unicode_hash=7274603073818924232)

    def testFarmHash128(self):
        self.doTest(hasher_type=farm_128,
                    bytes_hash=334882099032867325754781607143811124132,
                    seed_hash=49442029837562385903494085441886302499,
                    unicode_hash=251662992469041432568516527017706898625)


class TestMetroHash(TestHasher):
    def testMetroHash64_1(self):
        self.doTest(hasher_type=metro_64_1,
                    bytes_hash=7555593383206836236,
                    seed_hash=9613011798576657330,
                    unicode_hash=5634638029758084150)

    def testMetroHash128_1(self):
        self.doTest(hasher_type=metro_128_1,
                    bytes_hash=310240039238111093048322555259813357218,
                    seed_hash=330324289553816260191102680044286377986,
                    unicode_hash=160639312567243412360084738183177128736)

    def testMetroHash64_2(self):
        self.doTest(hasher_type=metro_64_2,
                    bytes_hash=13328239478646503906,
                    seed_hash=16521803336796657060,
                    unicode_hash=5992985172783395072)

    def testMetroHash128_2(self):
        self.doTest(hasher_type=metro_128_2,
                    bytes_hash=308979041176504703647272401075625691044,
                    seed_hash=156408679042779357342816971045969684594,
                    unicode_hash=169904568621124891123383613748925830588)

    def testMetroHashCrc64_1(self):
        self.doTest(hasher_type=metro_crc_64_1,
                    bytes_hash=6872506084457499713,
                    seed_hash=14064239385324957326,
                    unicode_hash=5634638029758084150)

    def testMetroHashCrc128_1(self):
        self.doTest(hasher_type=metro_crc_128_1,
                    bytes_hash=44856800307026421677415827141042094245,
                    seed_hash=199990471895323666720887863107514038076,
                    unicode_hash=53052528140813423722778028047086277728)

    def testMetroHashCrc64_2(self):
        self.doTest(hasher_type=metro_crc_64_2,
                    bytes_hash=9168163846307153532,
                    seed_hash=11235719994915751828,
                    unicode_hash=15697829093445668111)

    def testMetroHashCrc128_2(self):
        self.doTest(hasher_type=metro_crc_128_2,
                    bytes_hash=29039398407115405218669555123781288008,
                    seed_hash=26197404070933777589488526163359489061,
                    unicode_hash=136212167639765185451107230087801381416)


class TestMumHash(TestHasher):
    def testMumHash64(self):
        self.doTest(hasher_type=mum_64,
                    bytes_hash=8715813407503360407,
                    seed_hash=1160173209250992409,
                    unicode_hash=16548684777514844522)


class TestT1Hash(TestHasher):
    def testT1Hash32(self):
        if _pyhash.build_with_sse42:
            self.doTest(hasher_type=t1_32,
                        bytes_hash=1818352152,
                        seed_hash=2109716410,
                        unicode_hash=1338597275)
        else:
            self.doTest(hasher_type=t1_32,
                        bytes_hash=3522842737,
                        seed_hash=1183993215,
                        unicode_hash=4227842359)

    def testT1Hash32Be(self):
        self.doTest(hasher_type=t1_32_be,
                    bytes_hash=3775388856,
                    seed_hash=2897901480,
                    unicode_hash=1664992048)

    def testT1Hash64(self):
        self.doTest(hasher_type=t1_64,
                    bytes_hash=10616215634819799576,
                    seed_hash=6056749954736269874,
                    unicode_hash=18194209408316694427)

    def testT1Hash64Be(self):
        self.doTest(hasher_type=t1_64_be,
                    bytes_hash=10616215634819799576,
                    seed_hash=6056749954736269874,
                    unicode_hash=18194209408316694427)


class TestXXHash(TestHasher):
    def testXXHash32(self):
        self.doTest(hasher_type=xx_32,
                    bytes_hash=1042293711,
                    seed_hash=1018767936,
                    unicode_hash=2783988247)

    def testXXHash64(self):
        self.doTest(hasher_type=xx_64,
                    bytes_hash=5754696928334414137,
                    seed_hash=12934826212537126916,
                    unicode_hash=16125048496228390453)


class TestIssues(unittest.TestCase):
    # https://github.com/flier/pyfasthash/issues/3
    def testErrorReturnNone(self):
        h = fnv1_64()

        old_refcnt = sys.getrefcount(None)

        for i in range(10000):
            try:
                h(None)

                self.fail("fail to raise exception")
            except TypeError as ex:
                pass

        new_refcnt = sys.getrefcount(None)

        self.assertTrue(old_refcnt >= new_refcnt)

    # https://github.com/flier/pyfasthash/issues/24
    def testDefaultStringType(self):
        hasher = murmur3_32()

        self.assertEqual(hasher('foo'), hasher('foo'))
        self.assertNotEqual(hasher('foo'), hasher(b'foo'))


try:
    import pytest

    def bench_hasher(benchmark, hasher, hash):
        h = hasher()
        data = b"".join([chr(i) for i in range(256)])

        @benchmark
        def result():
            return h(data)

        assert result == hash

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_fnv1_32(benchmark):
        bench_hasher(benchmark, fnv1_32, 4117514240)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_fnv1a_32(benchmark):
        bench_hasher(benchmark, fnv1a_32, 1500862464)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_fnv1_64(benchmark):
        bench_hasher(benchmark, fnv1_64, 487086381785722880)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_fnv1a_64(benchmark):
        bench_hasher(benchmark, fnv1a_64, 13917847256464560128)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash1_32(benchmark):
        bench_hasher(benchmark, murmur1_32, 3043957486)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash1_aligned_32(benchmark):
        bench_hasher(benchmark, murmur1_aligned_32, 3043957486)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash2_32(benchmark):
        bench_hasher(benchmark, murmur2_32, 2373126550)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash2a_32(benchmark):
        bench_hasher(benchmark, murmur2a_32, 178525084)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash2_aligned_32(benchmark):
        bench_hasher(benchmark, murmur2_aligned_32, 2373126550)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash2_neutral_32(benchmark):
        bench_hasher(benchmark, murmur2_neutral_32, 2373126550)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_murmur_hash2_x64_64a(benchmark):
        bench_hasher(benchmark, murmur2_x64_64a, 12604435678857905857)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_murmur_hash2_x86_64b(benchmark):
        bench_hasher(benchmark, murmur2_x86_64b, 3759496224018757553)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_murmur_hash3_32(benchmark):
        bench_hasher(benchmark, murmur3_32, 3825864278)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_murmur_hash3_x86_128(benchmark):
        bench_hasher(benchmark, murmur3_x86_128,
                     97431559281111809997269275467939498127)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_murmur_hash3_x64_128(benchmark):
        bench_hasher(benchmark, murmur3_x64_128,
                     149984839147466660491291446859193586361)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_lookup3(benchmark):
        bench_hasher(benchmark, lookup3, 3792570419)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_super_fast_hash(benchmark):
        bench_hasher(benchmark, super_fast_hash, 2804200527)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_city_hash32(benchmark):
        bench_hasher(benchmark, city_32, 2824210825)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_city_hash64(benchmark):
        bench_hasher(benchmark, city_64, 894299094737143437)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_city_hash128(benchmark):
        bench_hasher(benchmark, city_128,
                     254849646208103091500548480943427727100)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_city_hash_crc128(benchmark):
        bench_hasher(benchmark, city_crc_128,
                     254849646208103091500548480943427727100)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_spooky_hash32(benchmark):
        bench_hasher(benchmark, spooky_32, 2489700128)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_spooky_hash64(benchmark):
        bench_hasher(benchmark, spooky_64, 8714752859576848160)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_spooky_hash128(benchmark):
        bench_hasher(benchmark, spooky_128,
                     69975394272542483818884528997491134240)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_farm_hash32(benchmark):
        bench_hasher(benchmark, farm_32, 3977123615)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_farm_hash64(benchmark):
        bench_hasher(benchmark, farm_64, 5291657088564336415)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_farm_hash128(benchmark):
        bench_hasher(benchmark, farm_128,
                     2614362402971166945389138950146702896)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_metro_hash64_1(benchmark):
        bench_hasher(benchmark, metro_64_1, 6897098198286496634)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_metro_hash128_1(benchmark):
        bench_hasher(benchmark, metro_128_1,
                     284089860902754045805586152203438670446)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_metro_hash64_2(benchmark):
        bench_hasher(benchmark, metro_64_2, 9928248983045338067)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_metro_hash128_2(benchmark):
        bench_hasher(benchmark, metro_128_2,
                     298961466275459716490100873977629041349)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_metro_hash_crc64_1(benchmark):
        bench_hasher(benchmark, metro_crc_64_1, 15625740387403976237)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_metro_hash_crc128_1(benchmark):
        bench_hasher(benchmark, metro_crc_128_1,
                     221795002586229010982769362009963170208)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_metro_hash_crc64_2(benchmark):
        bench_hasher(benchmark, metro_crc_64_2, 9313388757605283934)

    @pytest.mark.benchmark(group='hash128', disable_gc=True)
    def test_metro_hash_crc128_2(benchmark):
        bench_hasher(benchmark, metro_crc_128_2,
                     319940271611864595969873671463832146628)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_mum_hash3(benchmark):
        bench_hasher(benchmark, mum_64, 5704960907050105809)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_t1hash32(benchmark):
        bench_hasher(benchmark, t1_32, 677439739)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_t1hash32be(benchmark):
        bench_hasher(benchmark, t1_32_be, 967014975)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_t1hash64(benchmark):
        bench_hasher(benchmark, t1_64, 6501324028002495964)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_t1hash64be(benchmark):
        bench_hasher(benchmark, t1_64_be, 6501324028002495964)

    @pytest.mark.benchmark(group='hash32', disable_gc=True)
    def test_xx_hash32(benchmark):
        bench_hasher(benchmark, xx_32, 1497633363)

    @pytest.mark.benchmark(group='hash64', disable_gc=True)
    def test_xx_hash64(benchmark):
        bench_hasher(benchmark, xx_64, 2282408585429094475)

except ImportError:
    pass

if __name__ == '__main__':
    if "-v" in sys.argv:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s %(message)s')

    unittest.main()
