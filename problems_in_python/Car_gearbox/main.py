import Car
mustang = Car.Car("Mustang", 1)


#Test cases
mustang.changeGearUpAndDown( 11) # Gear 11 is not available.
mustang.changeGearUpAndDown(0)  #The car is in Neutral.
mustang.changeGearUpAndDown( -1) #The car is in Reverse.
mustang.changeGearUpAndDown( 4)  #Shifting gear up from -1 to 4.
mustang.changeGearUpAndDown( 2)  #Shifting gear down from 4 to 2.
mustang.changeGearUpAndDown( 2)  #car already in gear