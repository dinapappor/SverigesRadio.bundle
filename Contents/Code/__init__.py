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

def ListEpisodes(ProgramName, ProgramId):
    Log("ProgramId: "+str(ProgramId))
    EpisodeMenu = ObjectContainer(title1='Sveriges Radio', title2=ProgramName)
    
    SRData = JSON.ObjectFromURL('http://api.sr.se/api/v2/episodes/index?format=json&programid='+str(ProgramId))

    for Episode in SRData['episodes']:
	if 'broadcast' in Episode:
	    Log("Found broadcast")
	    EpisodeMenu.add(
		    TrackObject(
			url = Episode['broadcast']['broadcastfiles'][0]['url'],
			title = Episode['title'],
			summary = Episode['description'],
			thumb = Episode['imageurl']
			)
		)
	else:
	    Log("There was no broadcast")

    return EpisodeMenu
