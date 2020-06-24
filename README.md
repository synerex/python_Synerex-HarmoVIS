# python_Synerex-HarmoVIS
Python library for using Synerex-HarmoVIS_Client with Proxy

  pip install synerex_harmovis


 You might use this library with "HarmoVIS_client" at https://github.com/synerex/HarmoVIS_client/releases
 

## sample Python code.
You should use await and Ax functions in jupyter notebook (v6.x).
Also you need Python 3.7 or later.

```
import synerex_harmovis as sx

# you can set your map position.
await sx.sendViewStateAx(lat=35.181433,lon=136.906421,zoom=12, pitch=50)

# set flyToFlag true
await sx.sendHarmoVISAx("{\"flyToFlag:\":true}")

# now fly to tokyo!
await sx.sendViewStateAx(lat=35.689444,lon=139.69167,zoom=12, pitch=50)


```
