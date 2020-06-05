from datetime import datetime 
import asyncio
from grpclib.client import Channel

from .proto import api
from .proto import geography as geo

class SxHarmoVIS:
    ''' SxHarmoVIS: base class for Synerex-HarmoVIS integration
    '''
    def __init__(self, srvaddr='localhost:18000', channel=14, node_id = 100):
        hs = srvaddr.split(':')
        self.grpcChannel = Channel(host=hs[0], port=int(hs[1]))
        self.service = api.SynerexStub(self.grpcChannel)
        self.chan = channel
        self.node_id = node_id

    def close(self):
        self.grpcChannel.close()

    async def notifySupply(self, name, data):
        ts = datetime.now()
        cdata = api.Content(entity = data.SerializeToString())
        return await self.service.notify_supply(
            sender_id = self.node_id,
            channel_type = self.chan,
            supply_name = name,
            ts = ts,
            cdata = cdata
        )


    async def sendViewStateAsync(self, lat, lon, zoom):
        data = geo.ViewState(lat = lat, lon = lon , zoom= zoom) 
        return await self.notifySupply('ViewState',data)

    async def sendPitchAsync(self, pitch):
        data = geo.Pitch(pitch = pitch) 
        return await self.notifySupply('Pitch',data)

    async def sendBearingAsync(self, bearing):
        data = geo.Bearing(bearing = bearing) 
        return await self.notifySupply('Bearing',data)

    async def sendBarGraphsAsync(self, bs):
        mybars =[]
        for b in bs.bars:
            bd = []
            for d in b["barData"]:
                if type(d) is list:
                    bd0=geo.BarData(value = d[0],color = d[1])
                else:
                    bd0=geo.BarData(value = d, color = 0x00f000)
                bd.append(bd0)
            mybars.append(geo.BarGraph(id=b["id"], ts=b["ts"],
                                       color_type= b["colorType"],
                                       shape_type=b["shapeType"],
                                       min = b["min"],
                                       max = b["max"],
                                       color = b["color"],
                                       width = b["width"],
                                       radius = b["radius"],
                                       area_color = b["areaColor"],
                                       text = b["text"],
                                       lat = b["lat"],
                                       lon = b["lon"],
                                       bar_data = bd ))
        data = geo.BarGraphs(bars = mybars)
        return await self.notifySupply('BarGraphs',data)

    async def drawLinesAsync(self, lines):
        mylines =[]
        colors = []
        for l in lines.lines:
            mylines.append(geo.Line(from_=[l[0][1],l[0][0]],to=[l[1][1],l[1][0]]))
            colors.append(l[2])
        data = geo.Lines(lines = mylines, width= lines.width, color = colors)
        return await self.notifySupply('Lines',data)

class LineStore:
    def __init__(self):
        self.lines = []
        self.width = 1
    
    def setWidth(self, wid):
        self.width = wid

    def addLine(self,lat0,lon0,lat1,lon1, color = 0x708080):
        self.lines.append([[lat0,lon0],[lat1,lon1], color])

class BGStore:
    def __init__(self):
        self.bars = []
        self.idbase = 0
        self.colorType = geo.BarColorType.VARCOLOR
        self.shapeType = geo.BarShapeType.HEX
        self.areaColor = 0x0f0f0f
        self.color = 0x000d60
        self.radius = 100
        self.width = 30
        

    def addBarData(self,ts, label, lat,lon,barData):
        self.bars.append({
            'id': self.idbase,
            'ts': ts,
            'colorType': self.colorType,
            'shapeType': self.shapeType,
            'min' : 0,
            'max' : 100,
            'color': self.color,
            'width': self.width,
            'radius': self.radius,
            'areaColor': self.areaColor,
            'text' : label,
            'lat':lat,
            'lon':lon,
            'barData':barData
        })
        self.idbase = self.idbase+1
        return self.idbase-1

    def addBarDataNow(self,label,lat,lon, barData):
        ts = datetime.now()
        return self.addBarData(ts, label, lat,lon, barData)

    def updateBarData(self, id, ts, lat, lon, barData):
        self.bars[id].update({
            'ts': ts,
            'lat':lat,
            'lon':lon,
            'barData':barData
        })

    def updateBarDataNow(self,id, lat,lon, barData):
        ts = datetime.now()
        self.updateBarData(id, ts, lat,lon, barData)

async def sendBearingAx(b):
    srv = SxHarmoVIS()
    res = await srv.sendBearingAsync(b)
    srv.close()
    return res

async def sendPitchAx(p):
    srv = SxHarmoVIS()
    res = await srv.sendPitchAsync(p)
    srv.close()
    return res

async def sendViewStateAx(lat,lon,zoom):
    srv = SxHarmoVIS()
    res = await srv.sendViewStateAsync(lat,lon,zoom)
    srv.close()
    return res

async def sendBarGraphsAx(bg):
    srv = SxHarmoVIS()
    res = await srv.sendBarGraphsAsync(bg)
    srv.close()
    return res

async def drawLinesAx(ln):
    srv = SxHarmoVIS()
    res = await srv.drawLinesAsync(ln)
    srv.close()
    return res


def sendBearing(b):
    return asyncio.run(sendBearingAx(b))

def sendPitch(p):
    return asyncio.run(sendPitchAx(p))

def sendViewState(lat,lon,zoom):
    return asyncio.run(sendViewStateAx(lat,lon,zoom))

def sendBarGraphs(bg):
    return asyncio.run(sendBarGraphsAx(bg))

def drawLines(ln):
    return asyncio.run(drawLinesAx(ln))

    
