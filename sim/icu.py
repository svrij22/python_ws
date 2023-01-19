

#PATIENT CLASS
class IcuBed:
    def __init__(self):
        self.patient = {}
        self.occupied = False

    #check if is occupied
    def is_occupied(self):
        return self.occupied

    #get patient
    def get_patient(self):
        if not (self.occupied):
            raise Exception("Bed is empty")
        return self.patient

    #clear bed
    def clear(self):
        self.patient = {}
        self.occupied = False
        
    #set patient
    def set_patient(self, patient):
        if (self.occupied):
            raise Exception("Bed is occupied")

        self.patient = patient
        self.occupied = True

    #print self
    def print_self(self):
        print('icu bed is is occupied ' + str(self.occupied))

AMOUNT_OF_BEDS = 28

class IcuDepartment:

    #Init
    def __init__(self):
        #INIT BEDS
        self.ICUBeds = []
        for x in range(AMOUNT_OF_BEDS):
            self.ICUBeds.append(IcuBed())

    #Check if has space
    def has_space(self):
        for x in self.ICUBeds:
            if not (x.is_occupied()):
                return True
        return False

    # return percentage available
    def perc_avail(self):
        avail = [x for x in self.ICUBeds if not x.is_occupied()]
        return avail.count() / AMOUNT_OF_BEDS


    #add patient
    def add_patient(self, patient):

        #Sanity' has space
        if not self.has_space():
            raise Exception('No space available')

        #Add patient
        for bed in self.ICUBeds:
            if not (bed.is_occupied()):
                bed.set_patient(patient)
                return;

    #subtract hours from patients and remove from beds
    def hours_has_passed(self, hours):

        # for each bed -> is occup -> get patient -> subtract
        for bed in self.ICUBeds:
            if (bed.is_occupied()):

                #get patient and subtract
                patient = bed.get_patient()
                patient.hours_has_passed(hours)

                #disc if needed
                if (patient.should_be_discharged()):
                    bed.clear()


    #print the icu dept. state
    def describe_state(self):

        #for each bed print
        for index, bed  in enumerate(self.ICUBeds):
            print('bed ' + str(index + 1))
            if (bed.is_occupied()):
                bed.get_patient().print_self()
            else:
                print('empty')

    def describe_state_short(self):
        occup = [x for x in self.ICUBeds if x.is_occupied()]
        print("{} of {} beds occupied".format(str(len(occup)), str(AMOUNT_OF_BEDS)))

