
def MetadataObjectForURL(url):
    ChannelId = url.split("/")[-1].split(".")[0]
    SRData = XML.ElementFromURL('http://api.sr.se/api/v2/channels/'+ChannelId)

    ChannelData = SRData.find('channel')

    for Data in ChannelData:
	ChannelName = Channeldata.get('name')
	if Data.tag == 'image':
	    ChannelThumb = Data.text
	else:
	    pass
    
    return TrackObject(
	    title = ChannelName,
	    thumb = ChannelThumb,
	    )






def MediaObjectsForURL(url):
    return [
        MediaObject(
	bitrate = '128',
	audio_codec = AudioCodec.MP3,
	container = 'mp3',
	parts = [PartObject(key = Callback(PlayTrack, url = url, ext = '.mp3'))]
)
	]

def PlayTrack(url):
    return Redirect(url)
