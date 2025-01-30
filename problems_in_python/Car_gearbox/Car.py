class Car:
    carModel = ""
    currentGear = 0

    def __init__(self, model, gear):
        self.carModel = model
        self.currentGear = gear

    def changeGearUpAndDown(self, newGear):
        if newGear == 0 :
            print("Neutral")
        elif newGear == -1:
            print("Reverse")
        elif newGear >= 1 and newGear <= 7:
            if newGear > self.currentGear:
                print(f"Shifting gear up from {self.currentGear} to {newGear}.")
            elif newGear < self.currentGear:
                print(f"Shifting gear down from {self.currentGear} to {newGear}.")
            else:
                print(f"Already in gear {newGear}.")
        else:
            print("gear not available")

        self.currentGear = newGear

