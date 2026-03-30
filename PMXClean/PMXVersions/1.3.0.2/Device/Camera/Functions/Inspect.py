#DisplayName = Inspect
#Description = Executes the selected Inspection utilizing the provided Input Image from a previous step
#Icon = CameraIrisMaterialIcon
#Flags = IsHidden, IsProgramStep

def __inputs__():
    #Description = The inspection to run
    Inputs.Inspection = new.inspection()

    #Optional = True
    #Private = True
    #CanReference = Linked
    #Description = The input image to apply the Inspection to
    Inputs.Image = new.image()

def __run__():
    if Inputs.Inspection is None:
        __throwexception__(Exceptions.MissingInspection)
        return

    if InspectionRequiresImageInput(Inputs.Inspection.ReferenceName):
        if Inputs.Image is None:
            __throwexception__(Exceptions.ImageInputNotValid)
            return

        if Inputs.Image.Identifier == 0:
            __throwexception__(Exceptions.ImageInputNotValid)
            return

    InternalRunInspection(Inputs.Inspection, Inputs.Image, Outputs.Image, Outputs.Translation, Outputs.Passed)

def __virtual__():
    pass

def __outputs__():
    Outputs.Image = new.image()
    Outputs.Passed = new.bool(False, True)
    Outputs.Translation = new.translation()

def __exceptions__():
    Exceptions.MissingInspection = new.exception("#Inspection.Exceptions.InputInspectionMissingTitle", "#Inspection.Exceptions.InputInspectionMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.ImageInputNotValid = new.exception("#Inspection.Exceptions.ImageInputMissingTitle", "#Inspection.Exceptions.ImageInputMissing", new.enum("Severity", "Error").Value, None)
    Exceptions.OperationFailed = new.exception("#Inspection.Exceptions.OperationFailedTitle", "#Inspection.Exceptions.OperationFailed", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetExecutingStepName()])
    if PVA.Inspection.IsDesignTime():
        PVA.Inspection.WarnException(exception)
    else:
        PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass