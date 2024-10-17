import heating_system_api
import pytest

class TestHeatingSystem:

    # Before each
    def setup_method(self):
        self.system = heating_system_api.System()
        self.system.connect()
        self.system.turn_on()

    # After each
    def teardown_method(self):
        if self.system.is_on:
            self.system.turn_off()
        self.system.disconnect()

    # TC01: Validate if the user can turn the system on, with success
    @pytest.mark.critical
    def test_MMI_turn_on_system(self):
        assert self.system.is_on

    # TC02: Validate if the user can turn the system off, with success
    @pytest.mark.critical
    def test_MMI_turn_off_system(self):
        self.system.turn_off()
        assert not self.system.is_on

    # TC03: Validate if the user can turn on the boost mode, by the MMI
    @pytest.mark.high
    def test_MMI_turn_on_boost_mode(self):
        self.system.turn_on_boost_mode()
        assert self.system.is_boost_mode_on() == True

    # TC04: Validate if the user can turn off the boost mode, by the MMI
    @pytest.mark.high
    def test_MMI_turn_off_boost_mode(self):
        self.system.turn_on_boost_mode()
        self.system.turn_off_boost_mode()
        assert self.system.is_boost_mode_on() == False

    # TC05: Validate if the user receives any indication about “high power consumption” when the boost mode is activated, by the MMI
    @pytest.mark.medium
    def test_MMI_high_power_consumption_indication_when_boost_on(self):
        self.system.turn_on_boost_mode()
        assert self.system.get_power_consumption_warning() == "high power consumption"

    # TC06: Validate if the user does not receive any indication about “high power consumption” when the boost mode is deactivated, by the MMI
    @pytest.mark.medium
    def test_MMI_no_power_consumption_indication_when_boost_off(self):
        self.system.turn_off_boost_mode()
        assert self.system.get_power_consumption_warning() is None

    # TC07: Validate if the user can define a temperature of 14 or more, but less than 31, by the MMI
    @pytest.mark.critical
    def test_MMI_set_valid_temperature(self):
        self.system.set_temperature(22)
        assert self.system.get_temperature() == 22

    # TC08: Validate if the user can not define a temperature of 13 or less, by the MMI
    @pytest.mark.medium
    def test_MMI_set_temperature_below_minimum(self):
        with pytest.raises(ValueError):
            self.system.set_temperature(13)

    # TC09: Validate if the user can not define a temperature of 31 or more, by the MMI
    @pytest.mark.medium
    def test_MMI_set_temperature_above_maximum(self):
        with pytest.raises(ValueError):
            self.system.set_temperature(31)

    # TC10: Validate if the display is showing the right values of the system
    @pytest.mark.critical
    def test_MMI_display_shows_correct_values(self):
        self.system.set_temperature(22)
        assert self.system.display_value() == "Temperature: 22"

    # TC11: Validate if after changing the system values, the display shows the right data
    @pytest.mark.medium
    def test_MMI_display_updates_after_change(self):
        self.system.set_temperature(22)
        self.system.set_temperature(25)
        assert self.system.display_value() == "Temperature: 25"

    # TC12: Validate if the user can configure the holiday mode with success
    @pytest.mark.high
    def test_MMI_set_holiday_mode(self):
        self.system.set_holiday_mode(20, "01/08/2024", "31/08/2024")
        assert self.system.is_holiday_mode_on() == True

    # TC13: Validate if the temperature on the holiday mode backs to the default when the period is finished.
    # TC14: Validate if the user can turn off the holiday mode with success
    @pytest.mark.high
    def test_MMI_holiday_mode_default_temperature(self):
        self.system.set_holiday_mode(22, "01/08/2024", "31/08/2024")
        self.system.turn_off_holiday_mode()
        assert self.system.get_temperature() == self.system.default_temperature()
        assert self.system.is_holiday_mode_on() == False


    # TC15: Validate if the user can configure the Schedule Usage, in interval times mode
    @pytest.mark.high
    def test_MMI_schedule_usage_configuration(self):
        self.system.configure_schedule_usage("14:00", "17:00", 22)
        assert self.system.get_scheduled_temperature("16:00") == 22

    # TC16: Validate if the Schedule Usage receives the default values when it is not defined
    @pytest.mark.high
    def test_MMI_default_schedule_usage(self):
        self.system.configure_schedule_usage("14:00", "17:00", 22)
        self.system.turn_off_schedule_usage()
        assert self.system.get_scheduled_temperature("15:00") == self.system.default_temperature()

    # TC31: Validate if the RT shows the current room temperature
    @pytest.mark.critical
    def test_RT_shows_current_temperature(self):
        self.system.set_temperature(22)
        assert self.system.read_room_temperature() == 22

    # TC32: Validate if the user can define a temperature of 14 or more, but less than 31, by the RT
    @pytest.mark.critical
    def test_RT_set_valid_temperature(self):
        self.system.set_temperature(20)
        assert self.system.read_room_temperature() == 20

    # TC33: Validate if the user can not define a temperature of 13 or less, by the RT
    @pytest.mark.medium
    def test_RT_set_temperature_below_minimum(self):
        with pytest.raises(ValueError):
            self.system.set_temperature(13)

    # TC34: Validate if the user can not define a temperature of 31 or more, by the RT
    @pytest.mark.medium
    def test_RT_set_temperature_above_maximum(self):
        with pytest.raises(ValueError):
            self.system.set_temperature(31)

    # TC35: Validate if the RT shows the user the system operation mode (holiday mode/system state)
    @pytest.mark.high
    def test_RT_shows_system_operation_mode(self):
        self.system.set_holiday_mode(22, "01/08/2024", "31/08/2024")
        assert self.system.get_system_mode() == "Holiday Mode"

    # TC36: Validate if the RT allows the user to configure the system state
    @pytest.mark.medium
    def test_RT_configure_system_state(self):
        self.system.configure_system_state_welcome_message("Hi Manoel")
        assert self.system.get_welcome_message() == "Hi Manoel"

    # TC37: Validate, when the RT is disconnected from the MMI, it loses communication with the RT, and an Error appears.
    @pytest.mark.high
    def test_ERRORS_disconnected_error(self):
        self.system.disconnect_RT()
        assert self.system.get_error_message() == "RT disconnected"

    # TC38: Validate, when the temperature sensor does not work as expected, an Error appears.
    @pytest.mark.critical
    def test_ERRORS_temperature_sensor_error(self):
        self.system.simulate_sensor_failure()
        assert self.system.get_error_message() == "Temperature sensor malfunction"

    # TC39: Validate, when the LAN/WLAN is disconnected from the system configuration, the MMI loses communication with the APP, and an Error appears.
    @pytest.mark.high
    def test_LAN_WLAN_disconnection_error(self):
        self.system.disconnect_lan()
        assert self.system.get_error_message() == "Communication lost with APP"

