from src.controller import UGVRemoteController
from src.utils import normalise_to_range

sample_config = {
    'ps4_controller_config': {
        'PS4_INTERFACE': 'test/test',
        'R2_MIN': 0,
        'R2_MAX': 255,
        'L2_MIN': 0,
        'L2_MAX': 255,
        'L3_RIGHT_MIN': -128,
        'L3_RIGHT_MAX': 127,
        'L3_LEFT_MIN': -128,
        'L3_LEFT_MAX': 127,
    },
    'ugv_config': {
        'SPEED_MIN': 0,
        'SPEED_MAX': 100,
        'TURN_VALUE_MIN': -1,
        'TURN_VALUE_MID': 0,
        'TURN_VALUE_MAX': 1,
    }
}

controller = UGVRemoteController(config=sample_config)

# 1. Test Initialization
def test_initialization():
    """Test that the controller initializes correctly."""
    assert controller.speed == 0
    assert controller.turn == 0

# 2. Test Property Getters and Setters
def test_speed_property():
    """Test getter and setter for speed property."""
    assert controller.speed == 0
    controller.speed = 50
    assert controller.speed == 50
    controller.speed = -25
    assert controller.speed == -25
    controller.speed = 0

def test_turn_property():
    """Test getter and setter for turn property."""
    assert controller.turn == 0
    controller.turn = 1
    assert controller.turn == 1
    controller.turn = -1
    assert controller.turn == -1
    controller.turn = 0

# 3. Test `on_R2_press`
def test_on_R2_press():
    """Test handling of R2 button press."""
    controller.on_R2_press(128)
    expected_speed = normalise_to_range(
        128,
        sample_config['ps4_controller_config']['R2_MIN'],
        sample_config['ps4_controller_config']['R2_MAX'],
        sample_config['ugv_config']['SPEED_MIN'],
        sample_config['ugv_config']['SPEED_MAX']
    )
    assert controller.speed == expected_speed

# 4. Test `on_R2_release`
def test_on_R2_release():
    """Test handling of R2 button release."""
    controller.speed = 50
    controller.on_R2_release()
    assert controller.speed == 0

# 5. Test `on_L2_press`
def test_on_L2_press():
    """Test handling of L2 button press."""
    controller.on_L2_press(200)
    expected_speed = -normalise_to_range(
        200,
        sample_config['ps4_controller_config']['L2_MIN'],
        sample_config['ps4_controller_config']['L2_MAX'],
        sample_config['ugv_config']['SPEED_MIN'],
        sample_config['ugv_config']['SPEED_MAX']
    )
    assert controller.speed == expected_speed

# 6. Test `on_L2_release`
def test_on_L2_release():
    """Test handling of L2 button release."""
    controller.speed = 70
    controller.on_L2_release()
    assert controller.speed == 0

# 7. Test `on_L3_right`
def test_on_L3_right():
    """Test handling of L3 joystick moved to the right."""
    controller.on_L3_right(100)
    expected_turn = normalise_to_range(
        100,
        sample_config['ps4_controller_config']['L3_RIGHT_MIN'],
        sample_config['ps4_controller_config']['L3_RIGHT_MAX'],
        sample_config['ugv_config']['TURN_VALUE_MID'],
        sample_config['ugv_config']['TURN_VALUE_MAX']
    )
    assert controller.turn == expected_turn

# 8. Test `on_L3_left`
def test_on_L3_left():
    """Test handling of L3 joystick moved to the left."""
    controller.on_L3_left(-100)
    expected_turn = normalise_to_range(
        -100,
        sample_config['ps4_controller_config']['L3_LEFT_MIN'],
        sample_config['ps4_controller_config']['L3_LEFT_MAX'],
        sample_config['ugv_config']['TURN_VALUE_MIN'],
        sample_config['ugv_config']['TURN_VALUE_MID']
    )
    assert controller.turn == expected_turn

# 9. Test Multiple Events
def test_multiple_events():
    """Test combination of button presses."""
    # Simulate forward speed
    controller.on_R2_press(200)
    expected_speed = normalise_to_range(
        200,
        sample_config['ps4_controller_config']['R2_MIN'],
        sample_config['ps4_controller_config']['R2_MAX'],
        sample_config['ugv_config']['SPEED_MIN'],
        sample_config['ugv_config']['SPEED_MAX']
    )
    assert controller.speed == expected_speed

    # Simulate turning
    controller.on_L3_right(50)
    expected_turn = normalise_to_range(
        50,
        sample_config['ps4_controller_config']['L3_RIGHT_MIN'],
        sample_config['ps4_controller_config']['L3_RIGHT_MAX'],
        sample_config['ugv_config']['TURN_VALUE_MID'],
        sample_config['ugv_config']['TURN_VALUE_MAX']
    )
    assert controller.turn == expected_turn

    # Simulate stop
    controller.on_R2_release()
    assert controller.speed == 0
