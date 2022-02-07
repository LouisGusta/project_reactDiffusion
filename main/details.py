from cmath import inf
from helper import getRandomValue, getColors
from googleapiclient.http import MediaFileUpload


class Infos:
    width=1920
    height=1080
    fps=60
    totalFrames=18000
    k, f, dA, dB= getRandomValue()
    mode, rA, gA, bA, rB, gB, bB= getColors()
    deltaT=1.0
    pathVideo='../upload_yt/src/video.mp4'
    pathThumb='../upload_yt/src/thumbnail.png'


class Video:
    file='../upload_yt/src/video.mp4' 
    title= 'usei um codigo maluco e olha só no que deu'#"""k{k} / f{f}""".format(k=Infos.k, f=Infos.f)
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
        This study is based on 
        """.format(dA=Infos.dA, dB=Infos.dB,k=Infos.k, f=Infos.f)
        # http://karlsims.com/rd.html
    keywords=""
    category="28"
    privacyStatus="public"

    def defineThumbnail(youtube, videoId):
        thumbnail="../upload_yt/src/thumbnail.png"

        request = youtube.thumbnails().set(
            videoId = videoId,
            media_body=MediaFileUpload(thumbnail)
        )
        request.execute()



