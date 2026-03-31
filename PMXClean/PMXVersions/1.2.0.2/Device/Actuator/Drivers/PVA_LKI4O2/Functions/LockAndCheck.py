#DisplayName = Lock
#Description = Put the actuator in the "locked" state and check to ensure it succeeded
#Icon = LockMaterialIcon
#Flags = IsHidden

def __inputs__():
    #Description = The maximum amount of time to wait for the actuator to reach the desired state
    Inputs.Timeout = new.int(1000, 0, 1000000, 10, 100, "ms")

def __run__():
    Lock()
    Outputs.Passed.Value = LockCheck(Inputs.Timeout).IsLocked.Value

def __virtual__():
    pass

def __outputs__():
    Outputs.Passed = new.bool(False)

def __exceptions__():
    pass

def __throwexception__():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass