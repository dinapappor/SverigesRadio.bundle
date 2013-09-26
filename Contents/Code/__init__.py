TEXT_TITLE = 'Sveriges Radio'
ART = 'SR.jpg'
PLUGIN_PREFIX = '/music/SverigesRadio'

def Start():
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ART)



@handler(PLUGIN_PREFIX, TEXT_TITLE, thumb=ART, art=ART)
def MainMenu():

    menu = ObjectContainer()

    menu.add(
            DirectoryObject(
                key = Callback(GetChannels),
                title='Kanaler')
                )
    return menu


def GetChannels():

    ChannelMenu = ObjectContainer(title1='Sveriges Radio', title2='Kanaler')

    SRData = XML.ElementFromURL('http://api.sr.se/api/v2/channels?pagination=false')

    Channels = SRData.find('channels')

    for Channel in Channels:
        ChannelName = Channel.get('name')
	for data in Channel:
	    if data.tag == 'image':
		ChannelImage= data.text
	    elif data.tag == 'tagline':
		ChannelSummary = data.text
	    elif data.tag == 'liveaudio':
		for subdata in data.getchildren():
		    if subdata.tag == 'url':
			MediaUrl = subdata.text
		    else:
			pass
	    else:
		pass
        ChannelMenu.add(
                TrackObject(
                    #url = MediaObject(bitrate='128', audio_codec = AudioCodec.MP3, container = 'mp3', parts = [PartObject(key=Redirect(MediaUrl))]),
                    url = MediaUrl,
		    title = ChannelName,
		    summary = ChannelSummary,
		    thumb = ChannelImage,
                    )

                )


    return ChannelMenu
