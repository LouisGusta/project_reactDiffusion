from helper import getRandomValue, getColors
from googleapiclient.http import MediaFileUpload

class Infos:
    width=1920
    height=1080
    fps=60
    k= f= dA= dB=0
    mode= rA= gA= bA= rB= gB= bB=0
    totalFrames=18000
    deltaT=1.0
    pathVideo='../upload_yt/src/video.mp4'
    pathThumb='../upload_yt/src/thumbnail.png'

    def __init__(self):
        self.k, self.f, self.dA, self.dB= getRandomValue()
        self.mode, self.rA, self.gA, self.bA, self.rB, self.gB, self.bB= getColors()

class Video:
    file='../upload_yt/src/video.mp4' 
    title= """Reaction Diffusion Simulation | k{k} / f{f}""".format(k=Infos.k, f=Infos.f)
    if Infos.mode == 0:
        description="""
        This is a interactive video created by Project Reaction Diffusion
        dA: {dA} 
        dB: {dB} 
        k: {k} 
        f: {f} 
        Color: ({rA},{gA},{bA}) 
        Background Color: ({rB},{gB},{bB}) 
        -----------------------------------------------------------------------
        This study is based on 
        """.format(dA=Infos.dA, dB=Infos.dB,k=Infos.k, f=Infos.f, rA=Infos.rA, gA=Infos.gA, bA=Infos.bA, rB=Infos.rB, gB=Infos.gB, bB=Infos.bB)
    else:
        description="""
        This is a interactive video created by Project Reaction Diffusion
        dA: {dA} 
        dB: {dB} 
        k: {k} 
        f: {f} 
        -----------------------------------------------------------------------
        This study is based on http://karlsims.com/rd.html
        """.format(dA=Infos.dA, dB=Infos.dB,k=Infos.k, f=Infos.f)
        
    keywords=""
    category="28"
    privacyStatus="public"
    logging_level="DEBUG"
    noauth_local_webserver=""
    auth_host_port=""

    # def defineThumbnail(youtube, videoId):
    #     thumbnail="../upload_yt/src/thumbnail.png"

    #     request = youtube.thumbnails().set(
    #         videoId = videoId,
    #         media_body=MediaFileUpload(thumbnail)
    #     )
    #     request.execute()



