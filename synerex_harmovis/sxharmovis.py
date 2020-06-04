import grpc
import time
import random
import synerex_harmovis.sxutil

from synerex_harmovis.nodeapi import nodeapi_pb2
from synerex_harmovis.nodeapi import nodeapi_pb2_grpc
from synerex_harmovis.api import synerex_pb2
from synerex_harmovis.api import synerex_pb2_grpc
from synerex_harmovis.proto.geography import geography_pb2

from google.protobuf.timestamp_pb2 import Timestamp


class SxHarmoVIS:
    def __init__(self, srvaddr='localhost:18000', channel=14):
        self.channel = grpc.insecure_channel(srvaddr)
        self.client = synerex_pb2_grpc.SynerexStub(self.channel)
        self.sxClient = sxutil.SXServiceClient(client, 14, '')

    def sendViewState(self, lat, lon, zoom):
        ts = Timestamp()
        ts.GetCurrentTime()
        sm = synerex_pb2.Supply(id=99, sender_id=100, channel_type=14, supply_name='ViewState', ts=ts)
        data = geography_pb2.ViewState(lat = lat, lon = lon, zoom= zoom) 
        sm.cdata.entity = data.SerializeToString()
        self.client.NotifySupply(sm)

    def sendPitch(self, pitch):
        ts = Timestamp()
        ts.GetCurrentTime()
        sm = synerex_pb2.Supply(id=99, sender_id=100, channel_type=14, supply_name='Pitch', ts=ts)
        data = geography_pb2.Pitch(pitch= pitch)
        sm.cdata.entity = data.SerializeToString()
        self.client.NotifySupply(sm)

    def sendBearing(self, bearing):
        ts = Timestamp()
        ts.GetCurrentTime()
        sm = synerex_pb2.Supply(id=99, sender_id=100, channel_type=14, supply_name='Bearing', ts=ts)
        data = geography_pb2.Bearing(bearing = bearing)
        sm.cdata.entity = data.SerializeToString()
        self.client.NotifySupply(sm)

    def sendBarGraphs(self, bs):
        ts = Timestamp()
        ts.GetCurrentTime()
        sm = synerex_pb2.Supply(id=99, sender_id=100, channel_type=14, supply_name='BarGraphs', ts=ts)
        mybars =[]
        for b in bs.bars:
            bd = []
            for d in b.data:
                bd.append(geography_pb2.BarData(color=255,value = d))
            
            mybars.append(geography_pb2.BarGraph(id=b.id, ts=b.ts,
                                       colorType= b.colorType,
                                       shapeType=b.shapeType,
                                       min = b.min,
                                       max = b.max,
                                       color = b.color,
                                       width = b.width,
                                       radius = b.raduis,
                                       areaColor = b.areaColor,
                                       text = b.text,
                                       lat = b.lat,
                                       lon = b.lon,
                                       barData = bd ))

        data = geography_pb2.BarGraphs(bars = mybars)
        sm.cdata.entity = data.SerializeToString()
        client.NotifySupply(sm)

    def drawLines(self, lines):
        ts = Timestamp()
        ts.GetCurrentTime()
        sm = synerex_pb2.Supply(id=99, sender_id=100, channel_type=14, supply_name='Lines', ts=ts)
        mylines =[]
        for l in lines.lines:
            mylines.append()
            geography_pb2.Line(l[0],l[1])




class LineStore:
    def __init__(self):
        self.lines = []
        self.idbase = 0
        self.color = 0x0708080
        self.width = 1
    
    def setColor(self, col):
        self.color = col

    def addLine(self,lat0,lon0,lat1,lon1):
        self.lines.append([[lat0,lon0],[lat1,lon1]])



class BGstore:
    def __init__(self):
        self.bars = []
        self.idbase = 0

    def addBarData(self,lat,lon,label, bardata,ts):
        self.bars.append({
            'id': self.idbase,
            'ts': ts,
            'colorType': geography_pb2.FIXCOLOR,
            'shapeType': geography_pb2.BOX,
            'min' : 0,
            'max' : 100,
            'color' : 0xf0b0b0,
            'width': 30,
            'radius': 100,
            'areaColor': 0x0f0f0f,
            'text' : label,
            'lat':lat,
            'lon':lon,
            'barData':bardata
        })
        self.idbase = self.idbase+1
        return self.idbase-1

    def addBarDataNow(self,lat,lon,label, bardata):
        ts = Timestamp()
        ts.GetCurrentTime()
        return self.storeBarData(lat,lon,label, bardata,ts)

    def updateBarData(self, id, lat, lon, bardata,ts):
        self.bars[id].update({
            'ts': ts,
            'lat':lat,
            'lon':lon,
            'barData':bardata
        })

    def updateBarDataNow(self,lat,lon,label, bardata):
        ts = Timestamp()
        ts.GetCurrentTime()
        self.storeBarData(lat,lon,label, bardata,ts)

