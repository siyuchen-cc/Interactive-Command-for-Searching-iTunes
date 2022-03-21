#########################################
##### Name:                         #####
##### Uniqname:                     #####
#########################################

import json
from pickle import TRUE
import webbrowser  

class Media:

    def __init__(self, title="No Title", author="No Author", release_year='No Release Year', url='No URL',json=None):
        if json is None:
            self.title = title
            self.author = author
            self.release_year=release_year
            self.url=url
        else:
            if 'trackName' in json.keys():
                self.title=json['trackName']
            elif 'trackCensoredName' in json.keys():
                self.title=json['trackCensoredName']
            elif 'collectionName' in json.keys():
                self.title=json['collectionName']

            self.author=json['artistName']
            self.release_year=json['releaseDate'].split('-')[0]
            try:
                self.url=json['trackViewUrl']
            except:
                self.url=json['collectionViewUrl']
            

    def info(self):
        return self.title + ' by ' + self.author + ' (' + str(self.release_year) + ')'
    
    def length(self):
        return 0

class Song(Media):
    def __init__(self, title="No Title", author="No Author", release_year='No Release Year', url='No URL', album='No Album', genre='No Genre', track_length=0, json=None):
        if json is None:
            super().__init__(title, author, release_year, url)
            self.album=album
            self.genre=genre
            self.track_length=track_length
    
        else:
            super().__init__(json=json)
            self.album=json['collectionName']
            self.genre=json['primaryGenreName']
            self.track_length=json['trackTimeMillis']
            self.author=json['artistName']
            self.release_year=json['releaseDate'].split('-')[0]

    def info(self):
        return super().info()+ ' [' + self.genre +']'
    def length(self):
        return round(self.track_length/1000,0)  #convert ms to s

class Movie(Media):
    def __init__(self, title="No Title", author="No Author", release_year='No Release Year', url='No URL', rating='No Rating', movie_length=0,json=None):
        if json is None:
            super().__init__(title, author, release_year, url)
            self.rating=rating
            self.movie_length=movie_length
        else:
            super().__init__(json=json)
            self.rating=json['contentAdvisoryRating']
            self.movie_length=json['trackTimeMillis']
            self.author=json['artistName']
            self.release_year=json['releaseDate'].split('-')[0]


    def info(self):
        return super().info() + ' [' +self.rating + ']'
    
    def length(self):
        return round(self.movie_length/60000,0) # ms to minutes 

# Other classes, functions, etc. should go here

import requests
import json

base_url = "https://itunes.apple.com/search?" 

response = requests.get(base_url)
results_object = response.json() 

def get_url(input):
    params={}
    params['term']=input
    response=requests.get(base_url,params)

    if response.status_code == 200:
        results_object=response.json()
        return results_object['results']  
    else:
        print('Invalid. Can not search for the result.')
        return None
    
def create_Media_list(list_dict1):  
    other_media_list=[]
    song_list=[]
    movie_list=[]
    #print(dict1)
    for dict1 in list_dict1:
        #print(dict1,'this is dict1!!!!!')
        try:
            if 'kind' not in dict1.keys():
                if Media(json=dict1) not in other_media_list:
                    other_media_list.append(Media(json=dict1))
            if dict1['kind']=='song':
                if Song(json=dict1) not in song_list:
                    song_list.append(Song(json=dict1))
            if dict1['kind']=="feature-movie":
                if Movie(json=dict1) not in movie_list:
                    movie_list.append(Movie(json=dict1))
        except:
            if Media(json=dict1) not in other_media_list:
                other_media_list.append(Media(json=dict1))
            
    return song_list,movie_list,other_media_list


if __name__ == "__main__":
    
    search_input=input('Please enter a search term, or enter "exit" to quit: ')
    if search_input.isnumeric() is True:
            print('invalid input')
           

    while True:
        if search_input.lower()=='exit':
            print('Bye!')
            break
        

        #while search_input.lower() !='exit' and (search_input.isnumeric() is not True): 
             

        if search_input.isnumeric() is False:
            Song_list,Movie_list,Other_list=create_Media_list(get_url(search_input))  

            if len(Song_list)!=0:
                    print('\nSong\n')
                    for i in range(len(Song_list)):
                        print(str(i+1) + ' ' + Song_list[i].info())
                    #search_input=input("Enter a number for to lauch preview or enter a search query to search or enter 'exit' to quit: ")

            if len(Movie_list)!=0:
                    print('\nMovie\n')
                    for i in range(len(Movie_list)):
                        print(str(len(Song_list)+i+1) + ' ' + Movie_list[i].info())
                    #search_input=input("Enter a number for to lauch preview or enter a search query to search or enter 'exit' to quit: ")

            if len(Other_list)!=0:
                    print('\nOther_media\n')
                    for i in range(len(Other_list)):
                        print(str(len(Song_list)+len(Movie_list)+i+1) + ' ' + Other_list[i].info())
            
            
                    
            #launch preview.     
        if search_input.isnumeric():
            overall_media_list = Song_list + Movie_list + Other_list
            search_index=int(search_input)
            if int(search_index)>len(overall_media_list):
                print('invalid! please enter a number between 1 and ',str(len(overall_media_list)))
            elif int(search_index)<= len(overall_media_list):
                open_url=overall_media_list[int(search_index)-1].url
                print('Lauching  ' + open_url)
                webbrowser.open(open_url)
        
        search_input=input("Enter a number for to lauch preview or enter a search query to search or enter 'exit' to quit: ")
                 
                   
        

        
        
         