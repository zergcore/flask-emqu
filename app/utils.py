import os

async def verify_ping(hostname):
    #response = await os.system("ping " + hostname)
    response = os.system("ping " + hostname)
    # Verifying EXIT_STATUS
    if response == 0:
        pingstatus = "Servidor activo"
    else:
        pingstatus = "Servidor inactivo"
    
    context = {
        'response': response,
        'pingstatus': pingstatus
    }

    return context

