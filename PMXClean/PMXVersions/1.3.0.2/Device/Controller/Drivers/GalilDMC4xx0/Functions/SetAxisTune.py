#DisplayName = Set Axis Tune
#Description = Sets the tune parameters for an axis
#Icon = PipeWrenchMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The axis to set tune parameters for
    Inputs.Axis = new.axis("Controller0")

    #DisplayName = Proportional Gain
    #Description = The new proportional gain value for the axis
    Inputs.ProportionalGain = new.double(75, 0, 4095.875, .1, 10, "")

    #DisplayName = Integral Gain
    #Description = The new integral gain value for the axis
    Inputs.IntergralGain = new.double(1, 0, 255.999, .1, 10, "")

    #DisplayName = Derivative Gain
    #Description = The new derivative gain value for the axis
    Inputs.DerivativeGain = new.double(75, 0, 4095.875, .1, 10, "")

    #DisplayName = Assign To Properties
    #Desctiption = Assigns the value to the properties on the controller
    Inputs.AssignToProperties = new.bool(False)

def __run__():
    if Inputs.Axis is None:
        __throwexception__(Exceptions.AxisRequired)
        return

    referenceName = Inputs.Axis.GetReferenceName()

    if Inputs.ProportionalGain is not None:
        InternalSetAxisProportionalGain(referenceName, Inputs.ProportionalGain.Value, Inputs.AssignToProperties.Value)

    if Inputs.IntergralGain is not None:
        InternalSetAxisIntegralGain(referenceName, Inputs.IntergralGain.Value, Inputs.AssignToProperties.Value)

    if Inputs.DerivativeGain is not None:
        InternalSetAxisDerivativeGain(referenceName, Inputs.DerivativeGain.Value, Inputs.AssignToProperties.Value)
        
def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.AxisRequired = new.exception("#Controller.Exceptions.AxisRequiredTitle", "#Controller.Exceptions.AxisRequired", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass