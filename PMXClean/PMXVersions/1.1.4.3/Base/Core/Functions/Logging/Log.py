# DisplayName = Write To Log
# Description = Log a data collection to a file on disk
# Icon = BookEditMaterialIcon
# Flags = IsProgramStep, IsProcessStep

def __inputs__():
    #Description = The file to log to
    Inputs.File = new.file()

    #Description = The data to be logged
    Inputs.Data = new.collection(new.keyvaluepair("Time Stamp", None, new.enum("InputType", "Linked"), "Shared.System.CurrentTime"), True)

    #DisplayName = Archive Policy
    #Description = The frequency with which to generate a new file
    Inputs.ArchivePolicy = new.enum("ArchiveFrequency", "None")

def __run__():
    if not TestDirectoryExists(Inputs.File):
        __throwException__(Exceptions.BadDirectoryPath, Inputs.File.DirectoryPath)
        return

    loggingResponse = LogCollection(Inputs.File, Inputs.Data, Inputs.ArchivePolicy.Value)
    if loggingResponse is not None:
        __throwException__(Exceptions.LoggingFailed, loggingResponse)

def __virtual__():
    pass

def __outputs__():
    pass

def __throwException__(exception, message):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([message])
    PVA.Exceptions.ThrowException(exception)

def __exceptions__():
    Exceptions.BadDirectoryPath = new.exception("#Logging.Exceptions.BadDirectoryPathTitle", "#Logging.Exceptions.BadDirectoryPath", new.enum("Severity", "Error").Value, None)
    Exceptions.LoggingFailed = new.exception("#Logging.Exceptions.LoggingFailedTitle", "{#Logging.Exceptions.LoggingFailed}", new.enum("Severity", "Error").Value, None)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass