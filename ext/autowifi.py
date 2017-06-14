from wifi import Scheme, Cell
import sys

def autoconnect_command(interface):
    ssids = [cell.ssid for cell in Cell.all(interface)]
    connected = False
    for scheme in [Scheme.find('wlan0', s) for s in ['scheme-'+str(x) for x in range(1,6)]]:

        ssid = scheme.options.get('wpa-ssid', scheme.options.get('wireless-essid'))
        if ssid in ssids:
            sys.stderr.write('Connecting to "%s".\n' % ssid)
            try:
                scheme.activate()
            except ConnectionError:
                assert False, "Failed to connect to %s." % scheme.name
            connected = True
            break
    else:
        print "Couldn't find any schemes that are currently available."

    if not connected:
        s = Scheme.find('wlan0', 'hotspot')
        s.activate()

if __name__=='__main__':
    autoconnect_command('wlan0')
