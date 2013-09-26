TEXT_TITLE = 'Sveriges Radio'
ART = 'SR.jpg'
PLUGIN_PREFIX = '/music/SverigesRadio'

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
	    Log(Episode['broadcast']['broadcastfiles'][0]['duration'])
	    EpisodeMenu.add(
		    TrackObject(
			url = Episode['broadcast']['broadcastfiles'][0]['url'],
			title = Episode['title'],
			summary = Episode['description'],
			thumb = Episode['imageurl'],
			duration = Episode['broadcast']['broadcastfiles'][0]['duration'] * 1000
			)
		)
	elif 'listenpodfile':
	    Log(Episode['listenpodfile']['duration'])
	    EpisodeMenu.add(
		    TrackObject(
			url = Episode['listenpodfile']['url'],
			title = Episode['title'],
			summary = Episode['description'],
			duration = Episode['listenpodfile']['duration'] * 1000
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
