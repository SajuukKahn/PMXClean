# DisplayName = Set Width From Product
# Description = Set the width of the servo adjust based on the currently selected product
# Icon = ArrowLeftRightMaterialIcon
# Flags = IsProcessStep

def __inputs__():
    pass

def __run__():
    if not PVA.Product.IsProductSelected():
        __throwexception__(Exceptions.MissingProduct, "Width")
        return

    productWidth = PVA.Product.GetCurrentProductExternalProperty(GetDeviceParameter(), GetProductPropertyName())

    if productWidth == None:
        __throwexception__(Exceptions.ProductMissingProperty, "Width")
        return

    SetWidth(productWidth)

def __virtual__():
    pass

def __outputs__():
    pass

def __exceptions__():
    Exceptions.MissingProduct = new.exception("#Product.Exceptions.NoProductSelectedTitle", "#Product.Exceptions.NoProductSelected", new.enum("Severity", "Error").Value, None)
    Exceptions.ProductMissingProperty = new.exception("#Product.Exceptions.MissingPropertyTitle", "#Product.Exceptions.MissingPropertyTitle", new.enum("Severity", "Error").Value, None)

def __throwexception__(exception, name = ""):
    __exceptionhandling__()
    exception.ExceptionData.MessageParams = tuple([GetDisplayName(), name])
    PVA.Exceptions.ThrowException(exception)

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass