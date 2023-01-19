#SETTINGS CLASS
class Settings:
    def __init__(self):

        #hours and max attempts
        self.hours_between_reschedule = 6
        self.max_allowed_reschedule_attempts = 5

        #Define the step size of the simulation
        self.step_size_hour = 6
        self.amount_of_icu_beds = 28

        #sim settings
        self.simulator_days = 365 * 2

        self.debug_sleep = 0
        self.display_debug_msgs = False