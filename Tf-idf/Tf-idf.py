import re
import math
from nltk.stem.porter import *
import time
from tkinter import *

class Song:                              #Song class is the base class of the entire program. All the information needed in a song
                                         #(term frequencies , total number of terms , track ids , tf-idf vectors etc.) are contained in an instance of this class.
    def __init__(self,raw_song):
        """
        Parameter (self, raw_song)
        self -> 
        raw_song ->
        __init__ method is used for preprocessing the data containing songs with their corresponding frequency with the help of regex Python library
        We store them as a dictionary.
        """
        self.song=re.split(",",raw_song)    
        self.track_id=self.song[0]
        self.mxm_track_id=self.song[1]
        self.tf={}
        for i in range(2,len(self.song)):   #running a for loop on the entire dataset to separate arrays containing the song against it's term frequency
            temp=re.split(":",self.song[i])
            self.tf[int(temp[0])]=int(temp[1])
        self.total_terms=sum_terms(self.tf) 
        self.normalized_tf=normalize_tf(self.tf,self.total_terms)
        self.tf_idf_vector={}               #initially idf_vector and tf_idf vector is set to empty dictionary.
        self.normalized_tf_idf_vector={}

    def vector_normalize(self):
        """
        vector_normalize takes self as parameter and normalizes self from alphabet to number
        """
        self.normalized_tf_idf_vector=normalize_vector(self.tf_idf_vector)
        
    def tf_idf_update(self):

        self.tf_idf_vector=tf_idf_weight(self.normalized_tf)

class Query:
    def __init__(self,term_frequency):
        self.tf=term_frequency
        self.total_terms=sum_terms(self.tf)
        self.normalized_tf=normalize_tf(self.tf,self.total_terms)
        self.tf_idf_vector={}
        self.normalized_tf_idf_vector={}

    def vector_normalize(self):
        """
        The query given ny the user is normalized in order to compare
        """
        self.normalized_tf_idf_vector=normalize_vector(self.tf_idf_vector)

    def tf_idf_update(self):
        self.tf_idf_vector=tf_idf_weight(self.normalized_tf)

def normalize_vector(tf_idf_vector):
    """
    Parameter (tf_idf_vector)
    tf_idf_vector -> tf-idf vector
    Takes vector and normalizes it
    """
    length=0.00;
    normalized_tf_idf_vector={}
    for i in tf_idf_vector:
        length=length+(tf_idf_vector[i]*tf_idf_vector[i])
    length=float(math.sqrt(length))
    for i in tf_idf_vector:
        normalized_tf_idf_vector[i]=float(tf_idf_vector[i]/length)
    return normalized_tf_idf_vector

def tf_idf_weight(tf):
    """
    Parameter (tf)
    tf -> term frequency
    Assigns td-idf vector in a song
    """
    tf_idf={}
    for i in tf:
        tf_idf[i]=tf[i]*idf[i-1]
    return tf_idf
    
def normalize_tf(tf,total_terms):
    """
    Parameter (tf,total_terms)
    tf -> term frequency
    total terms -> number of words in a song
    It divides the term frequency with total number of terms in a song
    """
    normalized_tf={}
    for i in tf:
        normalized_tf[i]=float(float(tf[i])/float(total_terms))
    return normalized_tf

def sum_terms(tf):
    """
    Parameter (tf)
    tf -> term frequency
    It takes the term frequency list and returns the sum of all the term frequencies
    """
    count=0
    for i in tf:
        count=count+tf[i]
    return count

def clean_list():    
    for i in raw_song_list:
        if len(i)<10 :
            raw_song_list.remove(i)

def make_objects():
    """
    Creates a list of all the songs in form of an object
    """
    songs=[]
    for i in raw_song_list:
        songs.append(Song(i))
    return songs

def inverse_document_frequency():
    """
    Assigns the value to idf global variable
    """
    document_freq=[]
    inverse_df=[]
    for i in range(5000):
        document_freq.append(0)
    for i in song_list:
        for j in i.tf:
            document_freq[j-1]=document_freq[j-1]+1
    for i in document_freq:
        inverse_df.append(float(math.log(float(total_songs)/float(i))))
    return inverse_df

def list_update(l):
    """
    Parameter (l)
    l -> list of query/song objects
    Assigns value to tf idf vectors
    """
    for i in l:
        i.tf_idf_update()

def list_normalize_vectors(l):
    """
    Parameter (l)
    l -> list of query/song objects
    Converts the given vector into unit vector
    """
    for i in l:
        i.vector_normalize()

def take_input() :
    """
    Takes input from the user and coverts the query in processed form.
    """
    k=int(e2.get())
    query_string=e1.get()
    query_string=re.split(" ",query_string)
    stemmer=PorterStemmer()
    stemmed=[stemmer.stem(i) for i in query_string]
    q={}
    for i in range(len(stemmed)):
        if stemmed[i] in terms:
            if (terms.index(stemmed[i])+1) in q:
                q[terms.index(stemmed[i])+1]+=1
            else:
                q[terms.index(stemmed[i])+1]=1
    query=Query(q)
    query.tf_idf_update()
    query.vector_normalize()
    ans=calc_cosine(query)
    ans.sort()
    print(ans[-k:])

def calc_cosine(q):
    """
    Parameter (q)
    q -> Processed query
    It calculates cosine similarity between tf-idf vectors of the documents and the query
    """
    ans=[]
    for i in song_list:
        temp=0.00
        for j in q.normalized_tf_idf_vector:
            if j in i.normalized_tf_idf_vector:
                  temp+=q.normalized_tf_idf_vector[j]*i.normalized_tf_idf_vector[j]
        ans.append((temp,i.track_id))
    return ans

f=open("mxm_dataset_test.txt" ,"r")
content=f.read()
terms=re.split(",",content[3:29372])#terms is the list of 5000 most popular words
raw_song_list=re.split("TR",content[29374:])#contains the list of songs in given format
total_songs=len(raw_song_list)#number of songs
clean_list()
##song_list=make_objects()
##idf=inverse_document_frequency()
##list_update(song_list) #assigns tf-idf vectors to each of the songs
##list_normalize_vectors(song_list) # normalizes the tf-idf vectors
##master=Tk()
##Label(master,text="Please Enter Query").grid(row=0)
##Label(master,text="Please Enter K").grid(row=1)
##e1=Entry(master)
##e1.grid(row=0,column=1)
##e2=Entry(master)
##e2.grid(row=1,column=1)
##Button(master,text="Submit",command=take_input).grid(row=2,column=0)
##mainloop()

