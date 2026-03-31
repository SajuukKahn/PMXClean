#DisplayName = Check Error Status
#Description = Checks the error status from the Unitronics controller
#Icon = MonitorEyeMaterialIcon

def __inputs__():
    pass

def __run__():
    if (Settings.CartError.Value is False):
        errorCode = ReadErrorIndex()
        errorMessage = new.string(GetErrorMessage(errorCode.ErrorIndex.Value))
        __throwexception__(Exceptions.CartError, errorMessage)

def __outputs__():
    pass

def __exceptions__():
    Exceptions.CartError = new.exception("#FluidDelivery.Exceptions.EnduranceTitle", "#FluidDelivery.Exceptions.EnduranceGenericError", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, errorMessage):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName()])
    exception.ExceptionData.Message = errorMessage
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    StopMonitoring()

def __exceptionrecovery__():
    pass