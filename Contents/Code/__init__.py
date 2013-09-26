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
                key = Callback(GetLiveChannels),
                title='Lyssna live!')
                )
    return menu


def GetLiveChannels():

    ChannelMenu = ObjectContainer(title1='Sveriges Radio', title2='Kanaler')

    SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/channels?pagination=false&format=json')
    for channel in SRData['channels']:
	ChannelMenu.add(
		TrackObject(
		    url = channel['liveaudio']['url'],
		    title = channel['name'],
		    summary = channel['tagline'],
		    thumb = channel['image']
		    )
		)

    return ChannelMenu
