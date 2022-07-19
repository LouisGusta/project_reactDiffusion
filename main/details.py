from helper import getRandomValue, getColors
from googleapiclient.http import MediaFileUpload

class Infos:
    width=1920
    height=1080
    fps=60
    k= f= dA= dB=0
    mode= rA= gA= bA= rB= gB= bB=0
    totalFrames=1800
    apf=30
    deltaT=0.5
    pathVideo='../upload_yt/src/video.mp4'
    pathThumb='../upload_yt/src/thumbnail.png'

    def __init__(self):
        self.k, self.f, self.dA, self.dB= getRandomValue()
        self.mode, self.rA, self.gA, self.bA, self.rB, self.gB, self.bB= getColors()

class Video:
    file='../upload_yt/src/video.mp4'    
    keywords=""
    category="28"
    privacyStatus="private"
    logging_level="DEBUG"
    noauth_local_webserver=""
    auth_host_port=""

    def __init__(self, params):
        self.title= """Reaction Diffusion Simulation | k{k} / f{f}""".format(k=params.k, f=params.f)
        if params.mode == 0:
            self.description="""
This is an automatically generated video created by Project Reaction Diffusion

dA: {dA} 
dB: {dB} 
k: {k} 
f: {f} 
Color: ({rA},{gA},{bA}) 
Background Color: ({rB},{gB},{bB}) 

This study is based on http://karlsims.com/rd.html
            """.format(dA=params.dA, dB=params.dB,k=params.k, f=params.f, rA=params.rA, gA=params.gA, bA=params.bA, rB=params.rB, gB=params.gB, bB=params.bB)
        else:
            self.description="""
This is an automatically generated video created by Project Reaction Diffusion

dA: {dA} 
dB: {dB} 
k: {k} 
f: {f} 

This study is based on http://karlsims.com/rd.html
            """.format(dA=params.dA, dB=params.dB,k=params.k, f=params.f)
        

    # def defineThumbnail(youtube, videoId):
    #     thumbnail="../upload_yt/src/thumbnail.png"

    #     request = youtube.thumbnails().set(
    #         videoId = videoId,
    #         media_body=MediaFileUpload(thumbnail)
    #     )
    #     request.execute()



