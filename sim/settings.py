# SETTINGS CLASS
class Settings:
    def __init__(self):
        # hours and max attempts
        self.hours_between_reschedule = 24 # default 6
        self.max_allowed_reschedule_attempts = 20 # default 5

        # Define the step size of the simulation
        self.step_size_hour = 6
        self.amount_of_icu_beds = 25 # default 28

        # Define properties for reservations. The first on is the maximum amount of reservations, the second is the max time. E.g if in the next 8 hours 4 people will undergo surgery, 4 beds will be kept free
        self.max_amount_of_beds_reserved = 6
        self.max_time_before_schedule = 8 

        # sim settings
        self.simulator_days = 365 * 2

        self.debug_sleep = 0
        self.display_debug_msgs = False

        # == Animation Settings == 
        # Set the amount of steps that have to pass before a new point is plotted
        self.plot_graph_interval = 15 # default 15
        self.animator_enabled = True
