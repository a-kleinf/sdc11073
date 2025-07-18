"""Unit tests for the SdcLocation class."""

import unittest
import uuid

from sdc11073.location import SdcLocation
from sdc11073.wsdiscovery.service import Service
from sdc11073.xml_types.wsd_types import ScopesType


class TestSdcLocation(unittest.TestCase):
    scheme = SdcLocation.scheme  # 'sdc.ctxt.loc'
    default_root = 'sdc.ctxt.loc.detail'
    scope_prefix = scheme + ':/' + default_root  # sdc.ctxt.loc:/sdc.ctxt.loc.detail'

    def test_scope_string(self):
        loc = SdcLocation(fac='HO/SP1', poc='CU1', bed='BedA500')
        self.assertEqual(loc.root, self.default_root)
        self.assertEqual(loc.fac, 'HO/SP1')
        self.assertEqual(loc.poc, 'CU1')
        self.assertEqual(loc.bed, 'BedA500')
        self.assertEqual(loc.rm, None)
        self.assertEqual(loc.bldng, None)
        self.assertEqual(loc.flr, None)
        self.assertEqual(
            loc.scope_string,
            f'{self.scope_prefix}/HO%2FSP1%2F%2F%2FCU1%2F%2FBedA500?fac=HO%2FSP1&poc=CU1&bed=BedA500',
        )

        # this is an unusual scope with bed only plus root
        loc = SdcLocation(bed='BedA500', root='myroot')
        self.assertEqual(loc.root, 'myroot')
        self.assertEqual(loc.fac, None)
        self.assertEqual(loc.poc, None)
        self.assertEqual(loc.bed, 'BedA500')
        self.assertEqual(loc.rm, None)
        self.assertEqual(loc.bldng, None)
        self.assertEqual(loc.flr, None)
        self.assertEqual(loc.scope_string, f'{self.scheme}:/myroot/%2F%2F%2F%2F%2FBedA500?bed=BedA500')

        # this is an unusual scope with all parameters and spaces in them
        loc = SdcLocation(
            fac='HOSP 1',
            poc='CU 1',
            bed='Bed A500',
            flr='flr 1',
            rm='rM 1',
            bldng='abc 1',
            root='some where',
        )
        self.assertEqual(loc.root, 'some where')
        self.assertEqual(loc.fac, 'HOSP 1')
        self.assertEqual(loc.poc, 'CU 1')
        self.assertEqual(loc.bed, 'Bed A500')
        self.assertEqual(loc.rm, 'rM 1')
        self.assertEqual(loc.bldng, 'abc 1')
        self.assertEqual(loc.flr, 'flr 1')

        self.assertEqual(loc, SdcLocation.from_scope_string(loc.scope_string))

    def test_from_scope_string(self):
        scope_string_sdc = self.scope_prefix + '/HOSP1%2F%2F%2FCU1%2F%2FBedA500?fac=HOSP1&poc=CU1&bed=BedA500'
        loc = SdcLocation.from_scope_string(scope_string_sdc)
        self.assertEqual(loc.root, self.default_root)
        self.assertEqual(loc.fac, 'HOSP1')
        self.assertEqual(loc.poc, 'CU1')
        self.assertEqual(loc.bed, 'BedA500')
        self.assertEqual(loc.rm, None)
        self.assertEqual(loc.bldng, None)
        self.assertEqual(loc.flr, None)
        self.assertEqual(loc.scope_string, scope_string_sdc)

        # correct handling of scope with %20 spaces and + char in query
        scope_string = (
            self.scheme + ':/some%20where/HOSP%201%2Fabc%201%2FCU%201%2Fflr%201%2FrM%201%2FBed%20A500?rm=rM+1&flr=flr+1'
            '&bed=Bed+A500&bldng=abc+1&fac=HOSP+1&poc=CU+1'
        )
        loc = SdcLocation.from_scope_string(scope_string)
        self.assertEqual(loc.root, 'some where')
        self.assertEqual(loc.fac, 'HOSP 1')
        self.assertEqual(loc.poc, 'CU 1')
        self.assertEqual(loc.bed, 'Bed A500')
        self.assertEqual(loc.rm, 'rM 1')
        self.assertEqual(loc.bldng, 'abc 1')
        self.assertEqual(loc.flr, 'flr 1')

        # if we can create another identical  DraegerLocation from loc, then scopeString also seems okay.
        self.assertEqual(loc, SdcLocation.from_scope_string(loc.scope_string))

        # correct handling of scope with %20 spaces also in query
        for scope_string in (
            self.scheme
            + ':/some%20where/HOSP%201%2Fabc%201%2FCU%201%2Fflr%201%2FrM%201%2FBed%20A500?rm=rM%201&flr=flr%201'
            '&bed=Bed+A500&bldng=abc+1&fac=HOSP+1&poc=CU+1',
            self.scheme
            + ':/some%20where/this_part_of string_does_not_matter?rm=rM%201&flr=flr%201&bed=Bed+A500&bldng=abc+1'
            '&fac=HOSP+1&poc=CU+1',
        ):
            loc = SdcLocation.from_scope_string(scope_string)
            self.assertEqual(loc.root, 'some where')
            self.assertEqual(loc.fac, 'HOSP 1')
            self.assertEqual(loc.poc, 'CU 1')
            self.assertEqual(loc.bed, 'Bed A500')
            self.assertEqual(loc.rm, 'rM 1')
            self.assertEqual(loc.bldng, 'abc 1')
            self.assertEqual(loc.flr, 'flr 1')

    def test_equal(self):
        loc1 = SdcLocation(bed='BedA500', root='myroot')
        loc2 = SdcLocation(bed='BedA500', root='myroot')
        self.assertEqual(loc1, loc2)
        for attr_name in ('root', 'fac', 'bldng', 'poc', 'flr', 'rm', 'bed'):
            print(f'different {attr_name} expected')
            setattr(loc1, attr_name, 'x')
            setattr(loc2, attr_name, 'y')
            self.assertNotEqual(loc1, loc2)
            print(f'equal {attr_name} expected')
            setattr(loc2, attr_name, 'x')
            self.assertEqual(loc1, loc2)

    def test_contains(self):
        whole_world = SdcLocation()
        my_bed = SdcLocation(fac='fac1', poc='poc1', bed='bed1', bldng='bld1', flr='flr1', rm='rm1')
        my_bld = SdcLocation(fac='fac1', poc='poc1', bldng='bld1')
        other_bld = SdcLocation(fac='fac1', poc='poc1', bldng='bld2')
        any_flr1 = SdcLocation(flr='flr1')  # any location that has flr1 will match
        self.assertTrue(my_bed in whole_world)
        self.assertFalse(whole_world in my_bed)
        self.assertTrue(my_bed in SdcLocation(fac='fac1'))
        self.assertTrue(my_bed in SdcLocation(fac='fac1', poc='poc1'))
        self.assertTrue(my_bed in SdcLocation(fac='fac1', bed='bed1'))
        self.assertTrue(my_bed in SdcLocation(bed='bed1'))
        self.assertTrue(my_bed in my_bld)
        self.assertFalse(my_bld in my_bed)
        self.assertTrue(my_bed in any_flr1)
        self.assertFalse(my_bld in any_flr1)
        self.assertFalse(my_bed in other_bld)

        # non-default root
        my_bed = SdcLocation(fac='fac1', poc='poc1', bed='bed1', bldng='bld1', flr='flr1', rm='rm1', root='myroot')
        self.assertTrue(
            my_bed
            in SdcLocation(
                fac='fac1',
                poc='poc1',
                bed='bed1',
                bldng='bld1',
                flr='flr1',
                rm='rm1',
                root='myroot',
            ),
        )
        self.assertTrue(my_bed in SdcLocation(fac='fac1', root='myroot'))
        self.assertFalse(my_bed in SdcLocation(fac='fac2', root='myroot'))
        self.assertFalse(my_bed in SdcLocation(fac='fac1'))

    def test_filter_services_inside(self):
        my_loc = SdcLocation(fac='fac1', poc='poc1', bed='bed1', bldng='bld1', flr='flr1', rm='rm1', root='myroot')
        other_loc = SdcLocation(fac='fac2', poc='poc1', bed='bed1', bldng='bld1', flr='flr1', rm='rm1', root='myroot')
        service1 = Service(types=None, scopes=ScopesType(my_loc.scope_string), epr='a', x_addrs=None, instance_id='42')
        service2 = Service(
            types=None,
            scopes=ScopesType(other_loc.scope_string),
            epr='b',
            x_addrs=None,
            instance_id='42',
        )
        service3 = Service(types=None, scopes=None, epr='b', x_addrs=None, instance_id='42')
        matches = my_loc.filter_services_inside((service1, service2, service3))
        self.assertEqual(len(matches), 1)

    def test_scope_string_matches_returns_false_on_error(self):
        loc = SdcLocation(
            fac=uuid.uuid4().hex,
            poc=uuid.uuid4().hex,
            bed=uuid.uuid4().hex,
            bldng=uuid.uuid4().hex,
            flr=uuid.uuid4().hex,
            rm=uuid.uuid4().hex,
        )
        loc2 = SdcLocation(
            fac=uuid.uuid4().hex,
            poc=uuid.uuid4().hex,
            bed=uuid.uuid4().hex,
            bldng=uuid.uuid4().hex,
            flr=uuid.uuid4().hex,
            rm=uuid.uuid4().hex,
        )
        loc2.scheme = uuid.uuid4().hex
        self.assertFalse(loc._scope_string_matches(loc2.scope_string))

    def test_hash(self):
        fac = uuid.uuid4().hex
        poc = uuid.uuid4().hex
        bed = uuid.uuid4().hex
        bldng = uuid.uuid4().hex
        flr = uuid.uuid4().hex
        rm = uuid.uuid4().hex
        root = uuid.uuid4().hex
        loc = SdcLocation(
            fac=fac,
            poc=poc,
            bed=bed,
            bldng=bldng,
            flr=flr,
            rm=rm,
            root=root,
        )
        self.assertEqual(hash((fac, bldng, flr, poc, rm, bed, root)), hash(loc))
