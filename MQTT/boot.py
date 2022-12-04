import esp
esp.osdebug(None)

wifi_ssid = "kinabalucoders-roaming"
wifi_password = "iamawesome"

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
do_connect()