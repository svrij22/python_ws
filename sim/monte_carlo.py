from simulator import *
import itertools as it
import pandas as pd

# Get default settings
default_settings = Settings()
# Get all departments
departments = list(default_settings.department_distribution.keys())
# get min en max amount of beds
max_beds = default_settings.max_beds
min_beds = default_settings.amount_of_icu_beds
min_beds_for_department = 4
expanding_beds = [28]  # the amount af beds the Icu can expant to
normal_patient_amount = default_settings.normal_patient_amount


def monte_carlo():
    # stats
    dep_distribution = []
    bed_amount = []
    denied = []
    covid_denied = []
    waiting_time = []
    occupancy = []
    admissioned = []
    failed_reschedules = []
    succesful_reschedules = []

    # Get combinations
    combinations = all_combinations()

    for combi in combinations:
        # make distribution of departments
        distribution = {departments[0]: combi[0], departments[1]: combi[1], departments[2]: combi[2],
                        departments[3]: combi[3]}
        covid_multiplier = 0.1

        for i in expanding_beds:
            # calculate the amount of covid patients
            covid_patients = normal_patient_amount * covid_multiplier
            settings = Settings(bed_amount=i, covid_amount=covid_patients, department_distribution=distribution)
            icu_ending = run(settings)  # run icu with the specified distribution and covid amount
            covid_multiplier += 0.1  # for each time the amount of beds expent to covid mutipler go's up

            # save stats of icu
            covid_beds = i - sum(combi)  # calculate the amount of covid beds and add to combi
            combi.append(covid_beds)

            dep_distribution.append(combi)
            bed_amount.append(i)
            denied.append(icu_ending.stat_patients_DENIED)
            covid_denied.append(icu_ending.stat_covid_DENIED)
            waiting_time.append(icu_ending.stat_total_waiting_time)
            occupancy.append(icu_ending.stat_total_bed_occupation / (default_settings.simulator_days * 24 * i) * 100)
            admissioned.append(icu_ending.stat_patients_ADMISSIONED)
            failed_reschedules.append(icu_ending.stat_failed_RESCHEDULES)
            succesful_reschedules.append(icu_ending.stat_succesful_RESCHEDULES)

        # show progress
        print(f'at {(combinations.index(combi) + 1) / (len(combinations) + 1) * 100} %')

    # save data to a csv
    data = {
        'distribution': dep_distribution, 'bed_amount': bed_amount, 'denied': denied,
        'covid_denied': covid_denied, 'waiting_time': waiting_time, 'occupancy': occupancy,
        'admissioned': admissioned, 'failed_reschedules': failed_reschedules,
        'succesful_reschedules': succesful_reschedules
    }

    df = pd.DataFrame(data)
    df.to_csv('icu_data.csv')


def all_combinations():
    print(f'making combinations of beds distributions')
    combinations = []

    # make distributions
    distribution = it.product(range(min_beds_for_department, min_beds - 3 * min_beds_for_department),  # makes distributions where there are 4 values between 4 and 16
                              repeat=len(departments) - 1)

    # filter out not needed distributions
    for dis in distribution:
        dis = list(dis)
        if 20 < sum(dis) <= 28:  # only distributions where the sum is between 20 and 29
            combinations.append(dis)

    return combinations


monte_carlo()
