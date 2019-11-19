#!/usr/bin/env python3
import gi.repository
from gi.repository import Gio, GLib

#object destination name
dest = "org.freedesktop.NetworkManager"
#path inside the object
path = "/org/freedesktop/NetworkManager/Settings"
#interface insde path
interface = "org.freedesktop.NetworkManager.Settings"
#method inside interface
method = "ListConnections"
#method arguments
arg = None
#method reply type
reply_type = GLib.VariantType("(ao)")
#flags of the bus call
flags = Gio.DBusCallFlags.NONE
#timeout of the bus call (-1 means default timeout)
timeout = -1
#cancellable object if the bus call can be cancelled
cancellable = None


#connection to dbus
dbus = Gio.bus_get_sync(Gio.BusType.SYSTEM, None)

#getting reply from destination object
reply =  dbus.call_sync(dest, path, interface, method, 
			None, reply_type, flags, timeout, cancellable)
print(reply)
for e in reply.unpack():
	for i in e:
		print(i,type(i))
