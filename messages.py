from CTkMessagebox import CTkMessagebox

def Error_Message():
    CTkMessagebox(
        title="Error", 
        message="Du hast keinen Link eingegeben!"
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
