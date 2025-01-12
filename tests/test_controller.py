from src.controller import UGVRemoteController
from src.utils import normalise_to_range

sample_config = {
    'ps4_controller_config': {
        'PS4_INTERFACE': 'test/test',
        'R2_MIN': 0,
        'R2_MAX': 255,
        'L2_MIN': 0,
        'L2_MAX': 255
    },
    'ugv_config': {
        'SPEED_MIN': 0,
        'SPEED_MAX': 100
    }
}

controller = UGVRemoteController(config=sample_config)

# 1. Test Initialization
def test_initialization():
    assert controller.speed == 0

# 2. Test Property Getters and Setters
def test_r_speed_property():
    assert controller.speed == 0
    controller.speed = 50
    assert controller.speed == 50
    controller.speed = 0

def test_l_speed_property():
    assert controller.speed == 0
    controller.speed = 25
    assert controller.speed == 25
    controller.speed = 0

# def test_direction_property():
#     controller.direction = 0
#     assert controller.direction == 0

# 3. Test `normalise_to_range` Method
def test_normalise_to_range():
    normalized_value = round(normalise_to_range(128, 0, 255, 0, 100), 3)
    assert normalized_value == 50.196

# 4. Test `on_R2_press`
def test_on_R2_press():
    controller.on_R2_press(128)
    expected_speed = normalise_to_range(
        128,
        sample_config['ps4_controller_config']['R2_MIN'],
        sample_config['ps4_controller_config']['R2_MAX'],
        sample_config['ugv_config']['SPEED_MIN'],
        sample_config['ugv_config']['SPEED_MAX']
    )
    assert controller.speed == expected_speed

# 5. Test `on_R2_release`
def test_on_R2_release():
    controller.speed = 50
    controller.on_R2_release()
    assert controller.speed == 0

# 6. Test `on_L2_press`
def test_on_L2_press():
    controller.on_L2_press(200)
    expected_speed = -normalise_to_range(
        200,
        sample_config['ps4_controller_config']['L2_MIN'],
        sample_config['ps4_controller_config']['L2_MAX'],
        sample_config['ugv_config']['SPEED_MIN'],
        sample_config['ugv_config']['SPEED_MAX']
    )
    assert controller.speed == expected_speed

# 7. Test `on_L2_release`
def test_on_L2_release():
    controller.speed = 70
    controller.on_L2_release()
    assert controller.speed == 0

