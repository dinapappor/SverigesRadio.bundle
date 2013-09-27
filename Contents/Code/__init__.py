TEXT_TITLE = 'Sveriges Radio'
ART = 'SR.jpg'
PLUGIN_PREFIX = '/music/SverigesRadio'
PLSReg = Regex('File1=(https?://.+)')
def Start():
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ART)



@handler(PLUGIN_PREFIX, TEXT_TITLE, thumb=ART, art=ART)
def MainMenu():

    menu = ObjectContainer()
    
    #Add listen live menu.
    menu.add(
            DirectoryObject(
                key = Callback(GetLiveChannels),
                title = 'Lyssna live!')
            )
    menu.add (
            DirectoryObject(
                key = Callback(GetAllCategories),
                title = 'Program efter kategori')
            )
    menu.add(
	    PrefsObject(
		title=u"Inställningar..."
		)
	    )
    return menu


def GetLiveChannels():

    ChannelMenu = ObjectContainer(title1='Sveriges Radio', title2='Kanaler')
    AudioQuality = Prefs['AudioQuality']

    Log(Client.Protocols)

    if AudioQuality == 'High':
	AudioQualityString = '&audioquality=hi'
    elif AudioQuality == 'Low':
	AudioQualityString = '&audioquality=lo'
    else:
	AudioQualityString = ''

    SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/channels?liveaudiotemplateid=3&pagination=false&format=json'+AudioQualityString)
    for channel in SRData['channels']:
	Log(channel['liveaudio']['url'])
        ChannelMenu.add(
                CreateTrackObject(
                    MediaUrl = channel['liveaudio']['url'],
                    MediaTitle = channel['name'],
                    MediaDescription = channel['tagline'],
                    MediaArt = channel['image'],
		    MediaDuration = 0
                    )
                )

    return ChannelMenu

@route('/music/sverigesradio/track')
def CreateTrackObject(MediaUrl, MediaTitle, MediaDescription, MediaArt, MediaDuration):

    if MediaUrl.endswith('.m4a'):
	MediaContainer = Container.MP4
	MediaCodec = AudioCodec.AAC
	MediaFormat = 'aac'
    elif MediaUrl.endswith('mp3'):
	MediaCodec = AudioCodec.MP3
	MediaFormat = 'mp3'
	MediaContainer = 'mp3'
    elif ".pls" in MediaUrl:
	MediaContainer = Container.MP4
	MediaCodec = AudioCodec.AAC
	MediaFormat = 'aac'

    Track = TrackObject(
	    key = Callback(CreateTrackObject, MediaUrl = MediaUrl, MediaTitle = MediaTitle, MediaDescription = MediaDescription, MediaArt = MediaArt),
	    rating_key = MediaUrl,
	    title = MediaTitle,
	    summary = MediaDescription,
	    thumb = MediaArt,
	    items = [
		MediaObject(
		    parts = [
			PartObject(key=Callback(PlayAudio, MediaUrl=MediaUrl, ext=MediaFormat))
			],
		    container = MediaContainer,
		    audio_codec = MediaCodec,
		    audio_channels = 2,
		    duration = MediaDuration
		    )
		]
	    )
    return Track

def PlayAudio(MediaUrl):

    if MediaUrl.endswith(".pls"):
	MediaContent = content = HTTP.Request(MediaUrl, cacheTime=0).content
	RealUrl = PLSReg.search(MediaContent)

	if RealUrl:
	    Log("Found real url: "+RealUrl.group(1))
	    return Redirect(RealUrl.group(1))
	else:
	    raise Ex.MediaNotAvailable
    else:
	return Redirect(MediaUrl)


def GetAllCategories():

    CategoryMenu = ObjectContainer(title1='Sveriges Radio', title2='Alla program')

    SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/programcategories?format=json&pagination=false')

    for Category in SRData['programcategories']:
	CategoryMenu.add(
		DirectoryObject(
		    key = Callback(
			ShowCategory, ChannelId = Category['id'], CategoryName = Category['name']),
		    title = Category['name']
		    )
		)


    return CategoryMenu


def ShowCategory(ChannelId, CategoryName):

    ProgramMenu = ObjectContainer(title1='Sveriges Radio', title2=CategoryName)

    SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/programs/index?pagination=false&format=json&programcategoryid='+str(ChannelId))

    for Program in SRData['programs']:
	ProgramMenu.add(
		DirectoryObject(
		    key= Callback(
			ListEpisodes, ProgramId = Program['id'], ProgramName = Program['name']
			),
		    title = Program['name']
		    )
		)


    return ProgramMenu

def ListEpisodes(ProgramName, ProgramId, Page = 1, TotalPages = 1):
    Log("ProgramId: "+str(ProgramId))
    EpisodeMenu = ObjectContainer(title1='Sveriges Radio', title2=ProgramName)
    if Page < TotalPages:
	SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/episodes/index?format=json&programid='+str(ProgramId)+'&page='+str(Page))
    else:
	SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/episodes/index?format=json&programid='+str(ProgramId))

    for Episode in SRData['episodes']:
	if 'broadcast' in Episode:
	    EpisodeMenu.add(
		    CreateTrackObject(
			MediaUrl = Episode['broadcast']['broadcastfiles'][0]['url'],
			MediaTitle = Episode['title'],
			MediaDescription = Episode['description'],
			MediaArt = Episode['imageurl'],
			MediaDuration = Episode['broadcast']['broadcastfiles'][0]['duration'] * 1000
			)
		)
	elif 'listenpodfile':
	    EpisodeMenu.add(
		    CreateTrackObject(
			MediaUrl = Episode['listenpodfile']['url'],
			MediaTitle = Episode['title'],
			MediaDescription = Episode['description'],
			MediaArt = '',
			MediaDuration = Episode['listenpodfile']['duration'] * 1000
			)
		    )
	else:
	    pass

    if SRData['pagination']['page'] < SRData['pagination']['totalpages']:
	EpisodeMenu.add(
		NextPageObject(
		    key = Callback(ListEpisodes, ProgramName = ProgramName, ProgramId=ProgramId, Page = Page + 1, TotalPages = SRData['pagination']['totalpages'] ),
		    title = u'Nästa sida'
		    )
		)

    return EpisodeMenu
