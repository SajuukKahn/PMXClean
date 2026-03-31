#DisplayName = Set Parameters
#Description = Sets the PCP dispense parameters
#Icon = WaterPumpMaterialIcon
#SubIcon = CogOutlineMaterialIcon

def __inputs__():
    #Description = The dispense rate
    Inputs.Rate = new.double(1, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Suckback Duration
    #Description = The duration of motor reverse time after dispense
    Inputs.SuckbackDuration = new.double(0, 0, 5, 0.1, 1, "s")

    #DisplayName = Actual Displacement
    #Description = Actual material displacement recorded. Set the initial value to the Nominal Displacment for this pump. Max and min values are +/- 20% of Nominal Displacement.
    Inputs.ActualDisplacementA = new.double(.0170, 0.0001, 2, 0.0001, 0.01, "mL/rev", None, -1, True)

def __run__():
    axisA = Settings.PumpAAxis
    if axisA is None:
        __throwexception__(Exceptions.AxisMissing)
        return

    controller = axisA.GetController()
    if controller is None:
        __throwexception__(Exceptions.NoControllerConfigured)
        return

    SetRate(Inputs.Rate)
    SetActualDisplacement(Inputs.ActualDisplacementA)
    SetSuckbackDuration(Inputs.SuckbackDuration)
    SetContinuousDispense()

    Outputs.Rate = Inputs.Rate
    Outputs.SuckbackDuration = Inputs.SuckbackDuration

    updateOutputs()

    controller.ExecuteCommand(new.string("sbk_dur=" + str(Inputs.SuckbackDuration.Value)))

def __virtual__():
    pass

def updateOutputs():
    Outputs.Rate.MinimumValue = Inputs.Rate.MinimumValue
    Outputs.Rate.MaximumValue = Inputs.Rate.MaximumValue
    Outputs.Rate.Value = Inputs.Rate.Value

    Outputs.SuckbackDuration.MinimumValue = Inputs.SuckbackDuration.MinimumValue
    Outputs.SuckbackDuration.MaximumValue = Inputs.SuckbackDuration.MaximumValue
    Outputs.SuckbackDuration.Value = Inputs.SuckbackDuration.Value

def __outputs__():
    #Description = The dispense rate
    #Property = True
    Outputs.Rate = new.double(1, 0, 1000, 0.001, 1, "mL/min")

    #DisplayName = Suckback Duration
    #Description = The duration of motor reverse time after dispense
    #Property = True
    Outputs.SuckbackDuration = new.double(0, 0, 5, 0.1, 1, "s")

def __exceptions__():
    Exceptions.AxisMissing = new.exception("#FluidDelivery.Exceptions.AxisMissingTitle", "#FluidDelivery.Exceptions.AxisMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.NoControllerConfigured = new.exception("#Controller.Exceptions.MissingDeviceTitle", "#Controller.Exceptions.MissingDevice", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass