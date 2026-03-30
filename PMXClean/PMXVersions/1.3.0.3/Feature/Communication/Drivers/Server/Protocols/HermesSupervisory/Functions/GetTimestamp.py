#DisplayName = Get Hermes Timestamp
#Description = Generates a Hermes-formatted timestamp
#Icon = ClockStartMaterialIcon
#Flags = IsHidden

from datetime import datetime

def __inputs__():
    pass

def __run__():
    #Hermes format: YYYY-MM-DDThh:mm:ss.sss
    now = datetime.now()
    Outputs.Timestamp.Value = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]

def __outputs__():
    Outputs.Timestamp = new.string("")

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass