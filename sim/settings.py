# SETTINGS CLASS
class Settings:
    def __init__(self, bed_amount=28, covid_amount=1, department_distribution=None):
        # hours and max attempts
        self.hours_between_reschedule = 24  # default 6
        self.max_allowed_reschedule_attempts = 20  # default 5

        # Define the step size of the simulation
        self.step_size_hour = 6
        self.amount_of_icu_beds = bed_amount  # default 28
        self.max_beds = 50

        # normal amount of patients without covid
        self.normal_patient_amount = 5890

        # Define properties for reservations. The first on is the maximum amount of reservations, the second is the
        # max time. E.g if in the next 8 hours 4 people will undergo surgery, 4 beds will be kept free
        self.max_amount_of_beds_reserved = 6
        self.max_time_before_schedule = 8

        # set departments
        if department_distribution is None: department_distribution = {'CARD/INT/OTHER': 7, 'NEU/NEC': 7, 'CAPU': 7,
                                                                       'CHIR': 7}
        self.department_distribution = department_distribution
        self.department_distribution['COVID'] = bed_amount - sum(department_distribution.values())
        if self.department_distribution['COVID'] < 0:
            raise Exception(f"department distribution has to many beds: {self.department_distribution['COVID'] * -1}")

        # sim settings
        self.simulator_days = 365 * 2

        self.debug_sleep = 0
        self.display_debug_msgs = False

        # COVID patient settings
        if covid_amount == 0: covid_amount = 0.00000001
        self.COVID_amount = covid_amount
        self.EXPO_VARIABLE_COVID = self.simulator_days * 24 / self.COVID_amount

        # == Animation Settings == 
        # Set the amount of steps that have to pass before a new point is plotted
        self.plot_graph_interval = 15  # default 15
        self.animator_enabled = False
