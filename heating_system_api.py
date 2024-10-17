class System:
    def __init__(self):
        self.is_on = False
        self.boost_mode = False
        self.temperature = 20
        self.holiday_mode = False
        self.default_temp = 20
        self.power_consumption_warning = None
        self.scheduled_temperatures = {}
        self.current_mode = "Normal"
        self.error_message = None
        self.welcomeMessage = "Hi Admin"

    def connect(self):
        print("System connected")

    def disconnect(self):
        print("System disconnected")

    def turn_on(self):
        self.is_on = True
        print("System turned on")

    def turn_off(self):
        self.is_on = False
        print("System turned off")

    def turn_on_boost_mode(self):
        self.boost_mode = True
        self.power_consumption_warning = "high power consumption"
        print("Boost mode turned on")

    def turn_off_boost_mode(self):
        self.boost_mode = False
        self.power_consumption_warning = None
        print("Boost mode turned off")

    def is_boost_mode_on(self):
        return self.boost_mode

    def get_power_consumption_warning(self):
        return self.power_consumption_warning

    def set_temperature(self, temperature):
        if temperature < 14 or temperature >= 31:
            raise ValueError("Temperature must be between 14 and 30 degrees.")
        self.temperature = temperature
        print(f"Temperature set to {self.temperature}")

    def get_temperature(self):
        return self.temperature

    def display_value(self):
        return f"Temperature: {self.temperature}"

    def set_holiday_mode(self, temperature, start_date, end_date):
        self.holiday_mode = True
        self.holiday_mode_start_date = start_date
        self.holiday_mode_end_date = end_date
        self.set_temperature(temperature)
        self.current_mode = "Holiday Mode"
        print(f"Holiday mode set with temperature: {temperature}, in the period: {self.holiday_mode_start_date} to {self.holiday_mode_end_date}")

    def turn_off_holiday_mode(self):
        self.holiday_mode = False
        self.current_mode = "Normal"
        self.temperature = 20
        print("Holiday mode turned off")

    def is_holiday_mode_on(self):
        return self.holiday_mode

    def default_temperature(self):
        return self.default_temp

    def configure_schedule_usage(self, start_time, end_time, temperature):
        self.scheduled_temperatures[(start_time, end_time)] = temperature
        print(f"Scheduled temperature from {start_time} to {end_time}: {temperature}")

    def turn_off_schedule_usage(self):
        self.scheduled_temperatures = {}

    def get_scheduled_temperature(self, time):
        for (start, end), temp in self.scheduled_temperatures.items():
            if start <= time <= end:
                return temp
        return self.default_temp

    def read_room_temperature(self):
        return self.temperature

    def get_system_mode(self):
        return self.current_mode

    def configure_system_state_welcome_message(self, message):
        self.welcomeMessage = message
        print(f"Welcome message set to: {message}")

    def get_welcome_message(self):
        return self.welcomeMessage

    def disconnect_RT(self):
        print("RT disconnected")
        self.error_message = "RT disconnected"

    def simulate_sensor_failure(self):
        print("Simulating sensor failure")
        self.error_message = "Temperature sensor malfunction"

    def get_error_message(self):
        return self.error_message

    def disconnect_lan(self):
        print("LAN disconnected")
        self.error_message = "Communication lost with APP"

