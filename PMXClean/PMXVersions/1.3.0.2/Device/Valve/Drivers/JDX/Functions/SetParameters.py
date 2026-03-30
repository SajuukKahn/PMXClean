#DisplayName = Set Parameters
#Description = Sets the JDX parameters
#Icon = DispenseValveCustomIcon
#SubIcon = CogMaterialIcon
#Flags = IsProgramStep, IsTriggerStep

def __inputs__():
    #Description = The Flow time required for the material to flow into the orifice after each drop has been ejected
    Inputs.Refill = new.double(10, 1.8, 200, 1, 10, "ms")

    #Description = The time required for the material to be ejected from the orifice
    Inputs.Dwell = new.double(10, 1.8, 200, 1, 10, "ms")

    #Description = The number of cycles
    Inputs.Cycles = new.int(10, 1, 998, 10, 100, "cycles")

    #DisplayName = Run Continuous
    #Description = A value indicating whether to run continously until off is called, ignoring cycles
    Inputs.RunContinuous = new.bool(False)

def __run__():
    refill = '{:05d}'.format(int(Inputs.Refill.Value * 10))
    dwell = '{:05d}'.format(int((Inputs.Dwell.Value * 10) + 6))
    cycles = '{:03d}'.format(int(Inputs.Cycles.Value))
    if Inputs.RunContinuous.Value:
        cycles = "000"

    SendPacket(Settings.Header.Value + refill + ',' + dwell + ',' + cycles + Settings.Footer.Value)
    PVA.System.Wait(20)

    updateOutputs();

def __virtual__():
    pass

def updateOutputs():
    Outputs.Refill.Value = Inputs.Refill.Value
    Outputs.Dwell.Value = Inputs.Dwell.Value
    Outputs.Cycles.Value = Inputs.Cycles.Value
    Outputs.RunContinuous.Value = Inputs.RunContinuous.Value

def __outputs__():
    #Description = The Flow time required for the material to flow into the orifice after each drop has been ejected
    Outputs.Refill = new.double(10, 1.8, 200, 1, 10, "ms")

    #Description = The time required for the material to be ejected from the orifice
    Outputs.Dwell = new.double(10, 1.8, 200, 1, 10, "ms")

    #Description = The number of cycles
    Outputs.Cycles = new.int(10, 1, 998, 10, 100, "cycles")

    #DisplayName = Run Continuous
    #Description = A value indicating whether to run continously until off is called, ignoring cycles
    Outputs.RunContinuous = new.bool(False, True)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass