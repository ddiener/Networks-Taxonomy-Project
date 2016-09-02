class Taxonomy:
    
    '''
    Taxonomy represents a Linnean category (order, family, or genus)
    If a Taxonomy object's level is 'genus', then its item list contains
    strings of the form <species-name> [(<common-name>)]
    If the Taxonomy object's level is 'Order' or 'Family', then its item
    list contains Taxonomy objects of the next level down.
    '''
    def __init__(self, category, level='Order'):
        import pickle
        import os.path
        
        '''
        Create a new Taxonomy based on 'category'
        if 'level' is 'Order' and a serialization file
        for this order exists, then populate this object from
        that file; otherwise, create an empty Taxonomy

        category: the name of an order, a family, or a genus
        level: one of 'Order', 'Family', or 'Genus'
        '''
        self.errorMessageStatement = 'Insertion OK'
        if level == 'Order':
            # does the file already exist?
            if (os.path.isfile(category + ".p")):
                self.itemList = pickle.load(open(category + ".p", "rb"))
            self.level = 'Order'
            self.itemList = []
            self.categoryName = category;
        else:
            # just make an empty taxonomy object
            self.categoryName = category
            self.level = level
            self.itemList = []

    def addSpecies(self, species):
        '''
        Add a species to this taxonomy and return True. The level of this
        taxonomy must be 'genus'. If not, set an error message and return False.
        '''
        if self.level != 'Genus':
            self.errorMessageStatement = 'Taxonomy is not of level Genus.'
            return False
        else:
            self.itemList.append(species)
            self.serialize()
            return True    

    def addTaxonomy(self, subTaxonomy):
        '''
        Add a sub-taxonomy to this taxonomy and return True. The sub-taxonomy must
        be at one level below this taxonomy. If not, set an error message and return False.
        '''
        # checks to see one level below
        if self.level == 'Order' and subTaxonomy.level != 'Family':
            self.errorMessageStatement = 'Subtaxonomy was not one level below.'
            return False
        if self.level == 'Family' and subTaxonomy.level != 'Genus':
            self.errorMessageStatement = 'Subtaxonomy was not one level below.'
            return False
        self.itemList.append(subTaxonomy)
        self.serialize()
        return True
            

    def errorMessage(self):
        '''
        Return the error message generated by the last insertion, or
        'Insertion OK' if the last insertion did not create an error
        '''
        return self.errorMessageStatement

    def insert(self, path):
        
        '''
        Insert the species that is the last element of 'path' into
        this object,creating order, family, or genus Taxonomy objects
        as needed. If the length of path does not match the level of this
        Taxonomy object, set an error message ,abort the insertion,  and
        return False; otherwise return True after successful insertion.

        This Taxonomy Level  Expected path length
        Order                3
        Family               2
        Genus                1

        path: front-slash-separated list of categories.
        '''
        # to see if there is an existing species, otherwise add it
        temp = path.split('/')
        if self.level == 'Genus': 
            if len(temp) != 1:
                self.errorMessageStatement = 'Error inserting ' + path + ' into ' + self.categoryName + ': wrong length'
                return False
            else:
                self.itemList.append( temp[0] )
                self.serialize()
                return True
    
    
        if self.level == 'Family':
            if len(temp) != 2:
                self.errorMessageStatement = 'Error inserting ' + path + ' into ' + self.categoryName + ': wrong length'
                return False
            
            for item in self.itemList:
                if item.categoryName == temp[0]:
                    # in the event genus already exists
                    for _item in item.itemList:
                        if _item == temp[1]:
                            # species already exists in heirarchy
                            return True
                
                    # species does not exist, but the genus does
                    item.itemList.append( temp[0] )
                    return True
                
            # in the event no genus exists in the family
            newGenus = Taxonomy(temp[0], 'Genus')
            newGenus.itemList.append( temp[1] )
            self.itemList.append( newGenus )
            self.serialize()
            return True
        
        # error check on order
        if self.level == 'Order': 
            if len(temp) != 3:
                self.errorMessageStatement = 'Error inserting ' + path + ' into ' + self.categoryName + ': wrong length'
                return False
            print '\n'
            # iterate through family objects in order to see match
            for item in self.itemList:
                # check if there is a family that already exists
                if item.categoryName == temp[0]:
                    # there is already a family object with the same category name
                    for _item in item.itemList:
                        # for every genus in this family object
                        if _item.categoryName == temp[1]:
                            # genus already exists in this family object
                            for _item_ in _item.itemList:
                                # for every species string in this genus
                                if _item_ == temp[2]:
                                    # this species already exists in the genus
                                    return True
                            # genus exists but the species does not
                            _item.itemList.append(temp[2])
                            return True
                    # there is a family object, but no genus or therefore species
                    newGenus = Taxonomy(temp[1], 'Genus')
                    newGenus.itemList.append(temp[2])
                    _item.itemList.append(newGenus)
                    return True
            # adds a family with a new genus and new species in that genus
            newFamily = Taxonomy( temp[0], 'Family')
            _newGenus = Taxonomy( temp[1], 'Genus')
            _newGenus.itemList.append( temp[2] )
            self.itemList.append(newFamily)
            newFamily.itemList.append( _newGenus )
            self.serialize()
            return True

    def list(self):
        
        '''
        Return a string representing the contents of this Taxonomy
        and its sub-Taxonomies, in the format
        top-category-name (subitem1, subitem2,...),
        where subitem1, subitem2... are either strings representing species,
        in the  form <latin-name> [(common-name)], or sublists representing
        Taxonomies.
        '''
        # iterates through objects in an order's item list
        if self.level == 'Order':
            listSpecies = ""
            listSpecies += self.categoryName
            for family in self.itemList:
                listSpecies += " (" + family.categoryName
                for genus in family.itemList:
                    listSpecies += " (" + genus.categoryName
                    for species in genus.itemList:
                        listSpecies += " (" + species
                    listSpecies += ")"
                listSpecies += ")"
            listSpecies += ")"
            return listSpecies
        # iteratees through the items of a family
        if self.level == 'Family':
            listSpecies = ""
            listSpecies += self.categoryName
            for genus in self.itemList:
                listSpecies += " (" + genus.categoryName
                for species in genus.itemList:
                        listSpecies += " (" + species
                listSpecies += ")"
            listSpecies += ")"
            return listSpecies
        # iterates through items in a genus    
        if self.level == 'Genus':
            listSpecies = ""
            listSpecies += self.categoryName
            for species in self.itemList:
                listSpecies += " (" + species
            listSpecies += ")"
            return listSpecies
    

    def serialize(self):
        import pickle
    
        '''
        Save contents of this object using pickle
        '''
        pickle.dump(self.itemList, open(self.categoryName + ".p", "wb"))
        

    if __name__ == "__main__":
        import taxonomy
        import unittest
        import sys
        '''Test adding a species to a genus with no errors'''
        genus1 = taxonomy.Taxonomy('')
        while(1):
            userInput = raw_input('> ')
            commandList = []
            commandList = userInput.split(' ')
            for str in commandList:
                print( str + ' ' )
                if userInput.strip() == 'quit' or userInput.strip() == 'exit':
                    print 'Closing application'
                    sys.exit(0)
                if commandList[0] == 'insert':
                    genus1.insert(commandList[1])
                if commandList[0] == 'list':
                    print( genus1.list() )
                else:
                    print('The command ' + userInput + ' does not exist.')