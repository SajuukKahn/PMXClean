#DisplayName = Set Parameters
#Description = Sets the Dynamic Mixer dispense parameters
#Icon = WaterPumpMaterialIcon
#SubIcon = CogOutlineMaterialIcon

def __inputs__():
    #Description = The dispense rate
    Inputs.Rate = new.double(500, 0, 2000, 1, 10, "RPM")

def __run__():
    SetRate(Inputs.Rate)
    Outputs.Rate.Value = Inputs.Rate.Value

def __virtual__():
    pass

def __outputs__():
    #Description = The dispense rate
    #Property = True
    Outputs.Rate = new.double(500, 0, 2000, 1, 10, "RPM")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass