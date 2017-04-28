import re
def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string, flags=re.MULTILINE))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


def getMAC(interface):
    try:
        str = open('/sys/class/net/' + interface + '/address').read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

def getRobotInfos(app):
    return {
        'name': app.config["DOTBOT_NAME"],
        'master': '*',
        'ip': '*',
        'bridge': '*/bridge/',
        "macaddress":getMAC('wlan0'),
        "model": "%s v%s"%(app.config["MODEL_NAME"], app.config["MODEL_VERSION"])
        }
