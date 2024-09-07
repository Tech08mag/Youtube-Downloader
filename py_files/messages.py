from CTkMessagebox import CTkMessagebox

def Error_Message():
    CTkMessagebox(
        title="Error", 
        message="Du hast keinen Link eingegeben!"
        )

def fail_to_load_formats():
    CTkMessagebox(
    title="Error", 
    message="Es konnten keine Resolutions für dieses Video gefunden werden!"
    )

def Success_Message():
    CTkMessagebox(
            title="Status",
            message="Die Eingabe wird verarbeitet!"
        )

def Finish_Message():
    CTkMessagebox(
        title="Status",
        message="Das Video wurde erfolgreich gedownloadet!"
    )
