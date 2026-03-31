# DisplayName = Height Check
# Description = Check the Height relative to the substrate at the current position
# Icon = EyeCheckMaterialIcon

def __inputs__():
    #DisplayName = Expected Reading
    #Description = The expected value relative to the substrate of the laser height check
    Inputs.ExpectedReading = new.double(100, 50.0, 150.0, 0.001, 1.0, "mm")

    #Description = The allowed tolerance from the expected value
    Inputs.Tolerance = new.double(1, 0.0, 100.0, 0.1, 1.0, u"\u00B1mm")
    
    #DisplayName = Error When Out of Range
    #Description = A value indicating whether the function should throw an exception if the height check is out of tolerance
    Inputs.ErrorOutOfRange = new.bool(False)

def __run__():
    expectedReading = Inputs.ExpectedReading.Value
    tolerance = Inputs.Tolerance.Value
    reading = Read().Reading.Value
    lowRange = expectedReading - tolerance
    highRange = expectedReading + tolerance

    Outputs.Reading.Value = reading
    Outputs.Pass.Value = reading >= lowRange and reading <= highRange

    if not Outputs.Pass and Inputs.ErrorOutOfRange:
        Exceptions.OutOfRange.ExceptionData.MessageParams = tuple([GetDisplayName(), Outputs.Reading.Value, lowRange, highRange])
        __throwexception__(Exceptions.OutOfRange)

def __virtual__():
    pass

def __outputs__():
    #Description = The height check reading relative to the substrate
    Outputs.Reading = new.double(0, 50.0, 150.0, 0.001, 1.0, "mm")

    #Description = A value indicating whether the height check was successfully within tolerance
    Outputs.Pass = new.bool(False)

def __throwexception__(exception):
    __exceptionhandling__()
    PVA.Exceptions.ThrowException(exception)

def __exceptions__():
    Exceptions.OutOfRange = new.exception("#HeightProfiling.Exceptions.OutOfRangeTitle", "#HeightProfiling.Exceptions.OutOfRange", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass