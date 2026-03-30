def __settings__():
    pass

def onconnect():
    # Capture Attributes - Unremark and alter if the bounds need to change
    # e.g. Exposure Time has much higher top-range than this default
    #AddAcquisitionFeature("BlackLevel", "Black Level", 0, 25, "")
    #AddAcquisitionFeature("Gain", "Gain", 0, 47, "")
    #AddAcquisitionFeature("ExposureTime", "Exposure", 20, 100000, u"\u03BCs")

    # Image format controls
    SetFeature("PixelFormat", "YCbCr422_8")
    SetFeature("OffsetX", 0)
    SetFeature("OffsetY", 0)

    # Image Processing Control > White Balance Control
    SetFeature("BalanceWhiteAuto", "Off")
    SetFeature("BalanceRatioSelector", "Red")
    SetFeature("BalanceRatio", 0.7)
    SetFeature("BalanceRatioSelector", "Green")
    SetFeature("BalanceRatio", 0.7)
    SetFeature("BalanceRatioSelector", "Blue")
    SetFeature("BalanceRatio", 1.2)

    # Image Flip and Rotate Settings
    #  Rotation is rounded to nearest 90 Degrees
    FlipX(False)
    FlipY(False)
    Rotation(180)

    # Size of buffer collection
    Buffers(5)
    
    # The minimum packet size for normal operation with Jumbo Packets enabled 
    SetMinimumPacketSize(8000)

    # Calibration World Units error limits: (average, maximum)
    # this is relevant for Perspective Transformation mode
    CalibrationErrorLimits(0.015, 0.025)

    # Allowable skew tolerance in degrees
    SkewTolerance(15.0)

    # Whether or not to calibrate the live image
    DoLiveCalibration(True)

    # Optional changes to how the live calibration is performed
    SetLiveCalibrationMethods("M_NEAREST_NEIGHBOR", "M_OVERSCAN_DISABLE", True)

    # Set Digitizer parameters
    SetDigitizerParameter("M_GC_PACKET_RESEND", "M_ENABLE")
    SetDigitizerParameter("M_GC_FRAME_TIMEOUT", "M_DEFAULT")
    SetDigitizerParameter("M_GC_FRAME_MAX_RETRIES", "M_DEFAULT")
    SetDigitizerParameter("M_GC_MAX_NBR_PACKETS_OUT_OF_ORDER", "M_DEFAULT")
    SetDigitizerParameter("M_GC_PACKET_TIMEOUT", "M_DEFAULT")
    SetDigitizerParameter("M_GC_PACKET_MAX_RETRIES", "M_DEFAULT")
    SetDigitizerParameter("M_PROCESS_TIMEOUT", 500)
    SetDigitizerParameter("M_GC_INTER_PACKET_DELAY", 210)

    # Features to query on the Devices page
    AddFeatureQuery("BslResultingAcquisitionFrameRate")

    # Digitizer Features to query on the Devices page
    AddDigitizerQuery("M_PROCESS_TOTAL_BUFFER_NUM", "Process Buffers", "M_TYPE_INT64")
    AddDigitizerQuery("M_PROCESS_FRAME_RATE", "Actual Frame Rate", "M_TYPE_DOUBLE")
    #AddDigitizerQuery("M_DIGITIZER_INTERNAL_BUFFERS_NUM", "Internal Buffers", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_FRAME_STATUS_CODE", "Last Frame Status Code", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_FRAMES_GRABBED", "Total Frames", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_FRAME_CACHE_HITS", "Frame Cache Hits", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_FRAMES_CORRUPTED", "Corrupted Frames", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_FRAMES_MISSED", "Missed Frames", "M_TYPE_INT64")

    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_RECEIVED", "Total Packets", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKET_CACHE_HITS", "Packet Cache Hits", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_MISSED", "Missed Packets", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_RECEIVED_OUT_OF_ORDER", "Misordered Packets", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_RECOVERED", "Recovered Packets", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_RESENDS_NUM", "Resent Packets", "M_TYPE_INT64")
    #AddDigitizerQuery("M_GC_TOTAL_PACKETS_TIMEOUT", "Timed Out Packets", "M_TYPE_INT64")

    #AddDigitizerQuery("M_PROCESS_FRAME_COUNT", "Total Process Frames", "M_TYPE_INT64")
    #AddDigitizerQuery("M_PROCESS_FRAME_CORRUPTED", "Process Frames Corrupted", "M_TYPE_INT64")
    #AddDigitizerQuery("M_PROCESS_FRAME_MISSED", "Process Frames Missed", "M_TYPE_INT64")

    # Settings for Pattern Matching
    SetPatternFeature("M_ACCURACY", "M_MEDIUM")
    SetPatternFeature("M_CERTAINTY", 80)
    SetPatternFeature("M_NUMBER", 1)
    # default is the middle of the model, there is no way to specify default
    #SetPatternFeature("M_REFERENCE_X", INTEGERVALUE)
    # default is the middle of the model, there is no way to specify default
    #SetPatternFeature("M_REFERENCE_Y", INTEGERVALUE)
    SetPatternFeature("M_ROTATED_MODEL_MINIMUM_SCORE", 70)
    SetPatternFeature("M_SEARCH_ANGLE", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_ANGLE_ACCURACY", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_ANGLE_DELTA_NEG", 180)
    SetPatternFeature("M_SEARCH_ANGLE_DELTA_POS", 180)
    SetPatternFeature("M_SEARCH_ANGLE_INTERPOLATION_MODE", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_ANGLE_MODE", "M_DISABLE")
    SetPatternFeature("M_SEARCH_ANGLE_TOLERANCE", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_OFFSET_X", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_OFFSET_Y", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_SIZE_X", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_SIZE_Y", "M_DEFAULT")
    SetPatternFeature("M_SPEED", "M_MEDIUM")

    # Advanced Settings for Pattern Matching
    SetPatternFeature("M_COARSE_SEARCH_ACCEPTANCE", "M_DEFAULT")
    SetPatternFeature("M_EXTRA_CANDIDATES", "M_DEFAULT")
    SetPatternFeature("M_FAST_FIND", "M_DEFAULT")
    SetPatternFeature("M_FIRST_LEVEL", "M_DEFAULT")
    SetPatternFeature("M_LAST_LEVEL", "M_DEFAULT")
    SetPatternFeature("M_MAX_INITIAL_PEAKS", "M_DEFAULT")
    SetPatternFeature("M_MIN_SEPARATION_X", "M_DEFAULT")
    SetPatternFeature("M_MIN_SEPARATION_Y", "M_DEFAULT")
    SetPatternFeature("M_MODEL_STEP", "M_DEFAULT")
    SetPatternFeature("M_SEARCH_ANGLE_ACCURACY_MODE", "M_DEFAULT")

def ondisconnect():
    pass

def __exceptionhandling__():
    pass

def __exceptionrecovery__():
    pass