import cv2
import numpy as np
import os
#Add Thread Management
class Settings:
    """Settings class to handle shared data
    Attributes:
        * Images: dictionary link image name 'Wall' to image picture
        * Agents: Agent ID counter start from 1000
        * Food: Food ID counter start from 2000
        * Obstacles: Obstacles ID counter start from 3000
        * BlockSize: define how many pixles for block images sizes, images like (food,obstacles,blank,unob,agents , etc..), example (50,50)
        * WorldSize: define how many blocks in the world (10,10)-> 100 block
        * FigureSize: define the size of the images outputed.
        * ProbabilitiesTable: Dictionary (Key:name,Value:Probability distribution numpy array).
        * PossibleActions: numpy array contain all possible actions for agent.(Could be modified to represent customized set of actions)"""
    
    #Block Size
    BlockSize=(100,100)
    #Images so all elements, foods reference to those images without replication
    Images={}
    Images[0]=np.tile(1,(BlockSize[0],BlockSize[1],3)) #Empty
    Images[-1] =np.tile(0,(BlockSize[0],BlockSize[1],3)) # black or unobservable

    #Agent ID domain start from
    Agents=1000

    #Food ID domain (types)
    Food=2000

    #Barriers ID domain (types)
    Obstacles=3000

    #World Size
    WorldSize=(20,20)

    # Max Steps Per Episode
    MaxSteps = 1000

    #Figure Size
    FigureSize = (10,10)

    #Probability Distributions Table
    ProbabilitiesTable = {}
    
    #List of Possible Actions For Agent
    PossibleActions = np.array([['R','L'],['R','R'],['L','N'],['L','S'],['L','E'],['L','W'],\
    ['M','N'],['M','S'],['M','E'],['M','W']])

    @staticmethod
    def AddProbabilityDistribution(Name,IntProbabilityDst):
        """Convert Integerwise distribution array to indicies  
        Args:
            * Name: The name of the distribution
            * IntProbabilityDst: Integer array [0....+inf] of the world size, Used to generate Probability matrix using dirichlet distribution"""
        
        # Create A Probability with sum to 1.
        # more info : 
        # https://en.wikipedia.org/wiki/Dirichlet_distribution
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.dirichlet.html

        Settings.ProbabilitiesTable[Name] = np.random.dirichlet(IntProbabilityDst.ravel())

        #dx  = np.random.dirichlet(IntProbabilityDst.ravel())
        # desendent order of indicies with highest probability
        #rgsrt =  (-np.array(dx)).argsort()
        
        #Settings.ProbabilitiesTable[Name] = np.unravel_index(argsrt,IntProbabilityDst.shape)

    @staticmethod
    def SetWorldSize(x,y):
        """Update world Size
        Args:
            newsize: the new world size, example : SetWorldSize((20,20))"""
        #print 'Warning: This Value Should not be changed after creating the world'
        Settings.WorldSize=newsize

        Settings.apb = 360.0/(Settings.WorldSize[0]*2 + Settings.WorldSize[1]*2)

    # get unique Agent ID
    @staticmethod
    def GetAgentID():
        """staticmethod to get unique agent ID
        Return: integer for Agents"""
        Settings.Agents+=1
        return Settings.Agents

    #get unique obstacle ID (type)
    @staticmethod
    def GetObstaclesID():
        """staticmethod to get unique obstacle ID
        Return: integer for obstalces"""
        Settings.Obstacles+=1
        return Settings.Obstacles

    #get unique Food ID (type)
    @staticmethod
    def GetFoodID():
        """staticmethod to get unique Food ID
        Return: integer for Foods"""
        Settings.Food+=1
        return Settings.Food

    #convert from BGR colors to RGB colors
    @staticmethod
    def ImageViewer(image):
        """Convert image from BGR to RGB colors
        Return: RGB image"""
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)/255.0

    #Store Image with Key
    @staticmethod
    def AddImage(Key,Fname):
        """Add Image to Images dictionary
        Args:
            * Key: Dictionary name for the image
            * Fname: File Directory to the image Example: 'Pics/wall.jpg'
        Exception:
            * IOError: if file doesn't exist
        Example:
            * Settings.AddImage('Wall','Pics/wall.jpg')
        """
        if not os.path.isfile(Fname):
            raise IOError('file:\'{}\' not found'.format(Fname))
        Settings.Images[Key] = Settings.ImageViewer(cv2.resize(cv2.imread(Fname),Settings.BlockSize))
    @staticmethod
    def SetBlockSize(Newsize):
        """Set new block size in the Settings
        Args :
            * Newsize: integer for block new size. (block can only be square not rectangle).
        Exception:
            * AssertionError: if Newsize is not integer or less or equal 0"""
        assert type(Newsize) is int, "Newsize is not integer"
        assert Newsize>0, "Newsize can't be less or equal zero"
        Settings.BlockSize = (Newsize,Newsize)
        Settings.Images[0]=np.tile(1,(Settings.BlockSize[0],Settings.BlockSize[1],3)) #Empty
        Settings.Images[-1]=np.tile(0,(Settings.BlockSize[0],Settings.BlockSize[1],3)) # black or unobservable

        