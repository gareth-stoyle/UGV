import pytest
from src.controller import UGVRemoteController

sample_config = {
    'ps4_controller_config': {
        'ps4_interface': 'test/test',
        'R2_min_val': 0,
        'R2_max_val': 255,
        'L2_min_val': 0,
        'L2_max_val': 255
    },
    'ugv_config': {
        'speed_min_val': 0,
        'speed_max_val': 100
    }
}

controller = UGVRemoteController(config=sample_config)

# 1. Test Initialization
def test_initialization():
    assert controller.r_speed == 0
    assert controller.l_speed == 0
    assert controller.direction == 1

# 2. Test Property Getters and Setters
def test_r_speed_property():
    assert controller.r_speed == 0
    controller.r_speed = 50
    assert controller.r_speed == 50

def test_l_speed_property():
    assert controller.l_speed == 0
    controller.l_speed = 25
    assert controller.l_speed == 25

def test_direction_property():
    controller.direction = 0
    assert controller.direction == 0

# 3. Test `_control_normalise` Method
def test_control_normalise():
    normalized_value = controller._control_normalise(128, [0, 255], [0, 100])
    assert normalized_value == 50.196

# 4. Test `on_R2_press`
def test_on_R2_press():
    controller.on_R2_press(128)
    expected_speed = controller._control_normalise(
        128,
        [sample_config['ps4_controller_config']['R2_min_val'], sample_config['ps4_controller_config']['R2_max_val']],
        [sample_config['ugv_config']['speed_min_val'], sample_config['ugv_config']['speed_max_val']]
    )
    assert controller.l_speed == expected_speed

# 5. Test `on_R2_release`
def test_on_R2_release():
    controller.l_speed = 50
    controller.on_R2_release()
    assert controller.l_speed == 0

# 6. Test `on_L2_press`
def test_on_L2_press():
    controller.on_L2_press(200)
    expected_speed = controller._control_normalise(
        200,
        [sample_config['ps4_controller_config']['L2_min_val'], sample_config['ps4_controller_config']['L2_max_val']],
        [sample_config['ugv_config']['speed_min_val'], sample_config['ugv_config']['speed_max_val']]
    )
    assert controller.r_speed == expected_speed

# 7. Test `on_L2_release`
def test_on_L2_release():
    controller.r_speed = 70
    controller.on_L2_release()
    assert controller.r_speed == 0

# 8. Test `on_triangle_release`
def test_on_triangle_release():
    controller.direction = 1
    controller.on_triangle_release()
    assert controller.direction == 0

    controller.on_triangle_release()
    assert controller.direction == 1
