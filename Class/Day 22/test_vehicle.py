import pytest
import vehicle

def test_vehicle_price():
    assert vehicle.VehicleRental(1200,'Regular',12.2,True).rent_per_day == 1200