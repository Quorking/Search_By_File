# -*- coding: utf-8 -*-
"""
Created on Sun 11/19 10:26:35 2017

Input -> file # to search for
Output -> Copied files in supplied path\Copied_Files

@author: Alec
"""
import datetime, os, zipfile, shutil

def search():
    
    def get_present_date():
        timeanddate = str(datetime.datetime.now())
        month = timeanddate[5:7]
        year = timeanddate[2:4]
        return month, year
        
    def get_user_input(month, year):
        while True:
            #Get File Number
            while True:
                try:
                    FileNumber = str(input('\nPlease enter file number : '))
                    if not str(FileNumber).isnumeric():
                        raise TypeError
                    if len(str(FileNumber)) > 8 or len(str(FileNumber)) < 8:
                        raise ValueError
                    break
                
                except TypeError:
                    print('\nThe input provided contained values besides numbers. Please try again.')
                
                except ValueError:
                    if len(str(FileNumber)) > 8:
                        print('\nThe input provided was greater than 8 digits. Please try again. ')
                    if len(str(FileNumber)) < 8:
                        print('\nThe input provided was less than 8 digits. Please try again. ')
                
            #Get Send Indicator
            while True:
                try:
                    SInd = input('\nDo you want to search send files? (Y/N) ' ).lower()
                    if not SInd == 'y' and not SInd == 'n':
                        raise TypeError
                    if SInd == 'n':
                        break
                    while True:
                        try:
                            filer = input('Please enter the 3 digit filer code for client: ')
                            if len(str(filer)) > 3 or len(str(filer)) < 3:
                                raise ValueError
                            SendInd = (str(SInd), str(filer))
                            break
    
                        except ValueError:
                            if len(str(filer)) > 3:
                                print('\nThe input provided was greater than 3 digits. Please try again. ')
                            if len(str(filer)) < 3:
                                print('\nThe input provided was less than 3 digits. Please try again. ')
                    break
                except TypeError:
                    print('The input provided is not valid for this query. Please try again.')
                    
                except:
                    print('The input provided is not valid. Please try again.')
    
            #Get Receive Indicator
            while True:
                try:   
                    RInd = input('\nDo you want to search receive files? (Y/N) ').lower()
                    if not RInd == 'y' and not RInd == 'n':
                        raise ValueError
                    if RInd == 'n':
                        ReceiveInd = (RInd, '')
                        break
                    while True:
                        try:
                            DBname = input('Please enter database name: ').lower()
                            print(DBname)
                            DBlist = os.listdir(str(os.path.join('E:/', 'receive')))  
                            DBlistlower = []
                            for db in DBlist:
                                DBlistlower.append(str(db.lower()))
                            if DBname not in DBlistlower:
                                raise ValueError
                            ReceiveInd = (RInd, DBname)
                            break
                            
                        except ValueError:
                            print(DBname + ' is not a valid database. Please try again.')
                    
                    break
                except TypeError:
                    print('The input provided is not valid for this query. Please try again.')
    
                except:
                    print('The input provided is not valid. Please try again.')
     
            #Get Starting Date Range, Month and Year
            while True:
                try:
                    DateRangeStartMM = input('\nPlease enter starting search month (MM), blank if current month : ')
                    if not DateRangeStartMM == '':
                        if (int(DateRangeStartMM.strip('0')) > 12) or (int(DateRangeStartMM.strip('0'))) <= 0:
                            raise TypeError
                    else:
                        DateRangeStartMM = month
                        print(month)
                    DateRangeStartYY = input('\nPlease enter starting search year (YY), blank if current year : ')
                    
                    if not DateRangeStartYY == '':
                        int(DateRangeStartYY)
                    else:
                        DateRangeStartYY = year
                        print(year + '\n')
                    break
    
                except TypeError:
                    print('The input provided is not valid for this query. Please try again. ')
                    
                except:
                    print('The input provided is not valid. Please try again. ')
            break
    
        return FileNumber, SendInd, ReceiveInd, DateRangeStartMM, DateRangeStartYY
    
    def Create_Range(DateRangeStartMM, DateRangeStartYY):
        #Check DateRangeStartMM / YY, create list of months to search
        #Create list of months and year combinations to search
        MonthIncrement = 0
        RangestoSearch = [('20' + (DateRangeStartYY) + '-' + str(DateRangeStartMM))]
    
        while MonthIncrement <= 1:
            MonthIncrement += 1
            MonthtoSearch = (int(DateRangeStartMM.strip('0')) + int(MonthIncrement))
            if int(MonthtoSearch) < 10:
                MonthtoSearch = '0' + str(MonthtoSearch)
            YeartoSearch = int(DateRangeStartYY[:].strip('0'))
            if int(MonthtoSearch) > 12:
                YeartoSearch = int(DateRangeStartYY[:].strip('0'))
                YeartoSearch+=1
                MonthtoSearch = MonthtoSearch - 12
                MonthtoSearch = str('0' + str(MonthtoSearch))
            RangestoSearch.append('20' + str(YeartoSearch) + '-' + str(MonthtoSearch))
        return RangestoSearch
        
    def dircheck(FileNumber):
        if not os.path.exists(os.path.join('E:/', 'copy', FileNumber)):
            os.makedirs(os.path.join('E:/', 'copy', FileNumber))
        dst = os.path.join('E:/', 'copy', FileNumber)
        return dst
    
    ##  Search either Receive and/or Send directories using list of months to search
    def Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch, dst):
        print('Processing...')
        
        ##SEND SEARCH    
        if SendInd[0] == 'y':
            root = os.path.join('E:/', 'Send', 'hist')
            dstS = os.path.join(dst, 'send')
            os.chdir(root)
            try:
                #Case 1 - Get Files in Current Send Directory
                ind = '1'                
                FilesToday = os.listdir(root)
                for file in FilesToday:
                    if file[-4:] == '.ABI':
                        FileContents = open(os.path.join(root, str(file)), 'r')
                        FileContentsRead = FileContents.read()
                        if str(FileNumber) in FileContentsRead and SendInd[1] in FileContentsRead:
                            if os.path.isdir(dstS) == True:
                                shutil.copy(os.path.join(root, str(file)), dstS)
                                print('S '+ str(file))
                            else:
                                os.mkdir(dstS)
                                shutil.copy(os.path.join(root, str(file)), dstS)
                                print('S '+ str(file))
                        FileContents.close()
                        
                #Case 2 - Get Files from Past Send Directories, subdirectories and handle zip files
                ind = '2'  
                for dirs in RangestoSearch:
                    if os.path.isdir(os.path.join(root, str(dirs))) == True:
                        os.chdir(os.path.join(root, str(dirs)))
                        dirlist = os.listdir()
                        for dirfiles in dirlist:
                            #Directories  - ABI                          
                            if dirfiles[-4:] == '.ABI':
                                target = os.path.join(str(root), str(dirs), str(dirfiles))
                                FileContents = open(target, 'r')
                                FileContentsRead = FileContents.read()
                                if str(FileNumber) in FileContentsRead and SendInd[1] in FileContentsRead:
                                    if os.path.isdir(dstS) == True:
                                        shutil.copy(target, dstS)
                                        print('S '+ str(dirfiles))
                                    else:
                                        os.mkdir(dstS)
                                        shutil.copy(target, dstS)
                                        print('S '+ str(dirfiles))
                                FileContents.close()
                            #Directories - ZIP
                            ind = '3'
                            if dirfiles[-4:] == '.zip':
                                target = os.path.join(str(root), str(dirs), str(dirfiles))
                                zippeddir = zipfile.ZipFile(target, 'r')
                                zippeddirfiles = zippeddir.namelist()
                                for zippedfiles in zippeddirfiles:
                                    if zippedfiles[-4:] == '.ABI':
                                        ZippedFileContents = zippeddir.open(zippedfiles)
                                        ZippedFileContentsRead = str(ZippedFileContents.read(), 'latin-1')
                                        if str(FileNumber) in ZippedFileContentsRead  or str(FileNumber) in zippedfiles and SendInd[1] in ZippedFileContentsRead:
                                            if os.path.isdir(dstS) == True:
                                                zippeddir.extract(zippedfiles, path=dstS)
                                                print('S '+ str(zippedfiles))
                                                ZippedFileContents.close()
                                            else:
                                                os.mkdir(dstS)
                                                zippeddir.extract(zippedfiles, path=dstS)
                                                print('S '+ str(zippedfiles))
                                                ZippedFileContents.close()
                                        else:
                                            ZippedFileContents.close()
                                zippeddir.close()                        
                            #Sub-Directories - ABI
                            ind = '4'
                            if os.path.isdir(os.path.join(str(root), str(dirs), str(dirfiles))):
                                os.chdir(os.path.join(str(root), str(dirs), str(dirfiles)))
                                subdirlist = os.listdir()
                                for subdirfiles in subdirlist:
                                    if subdirfiles[-4:] == '.ABI':
                                        target = os.path.join(str(root), str(dirs), str(dirfiles), str(subdirfiles))
                                        FileContents = open(target, 'r')
                                        FileContentsRead = FileContents.read()
                                        if str(FileNumber) in FileContentsRead and SendInd[1] in FileContentsRead:
                                            if os.path.isdir(dstS) == True:
                                                shutil.copy(target, dstS)
                                                print('S '+ str(subdirfiles))
                                            else:
                                                os.mkdir(dstS)
                                                shutil.copy(target, dstS)
                                                print('S '+ str(subdirfiles))
                                        FileContents.close()
                                        
            
            except Exception as e:
                        print(e)
                        print(ind)
                        pass    
        
        ##RECEIVE SEARCH
        if ReceiveInd[0] == 'y':
            root = os.path.join('E:/', 'receive', str(ReceiveInd[1]))
            dstR = os.path.join(dst,'receive')
            os.chdir(root)
            try:
                #Case 1 - Get Files in Current Receive Directory
                FilesToday = os.listdir(root)
                for file in FilesToday:
                    if file[-4:] == '.OUT':
                        
                        FileContents = open(os.path.join(root, str(file)), 'r')
                        FileContentsRead = FileContents.read()
                        if str(FileNumber) in FileContentsRead:
                            if os.path.isdir(dstR) == True:
                                shutil.copy(os.path.join(root, str(file)), dstR)
                                print('R '+ str (file) )
                            else:
                                os.mkdir(dstR)
                                shutil.copy(os.path.join(root, str(file)), dstR)
                                print('R '+ str (file) )
                        FileContents.close()
                        
                #Case 2 - Get Files from Past Receive Directories, and handle zip files
                HistReceiveDir = os.listdir(str(os.path.join(root, 'history')))
                
                for i in range(len(HistReceiveDir)):
                    HistReceiveDir[i] = HistReceiveDir[i].replace('_', '-')
                os.chdir(os.path.join(root, 'history'))
                for dirs in RangestoSearch:
                    for dirfiles in HistReceiveDir:
                        if dirfiles[:-6] == dirs:
                            #Directory - OUT                            
                            if dirfiles[-4:] == '.OUT':
                                target = os.path.join(root, 'history', str(dirfiles.replace('-','_')))
                                FileContents = open(target, 'r')
                                FileContentsRead = FileContents.read()
                                if str(FileNumber) in FileContentsRead:
                                    if os.path.isdir(dstR) == True:
                                        shutil.copy(target, dstR)
                                        print('R '+ str (target) )
                                    else:
                                        os.mkdir(dstR)
                                        shutil.copy(target, dstR)
                                        print('R '+ str (target) )
                                FileContents.close()
                            #Directory - ZIP
                            if dirfiles[-4:] == '.zip':
                                target = os.path.join(root, 'history', str(dirfiles.replace('-','_')))
                                zippeddir = zipfile.ZipFile(target, 'r')
                                zippeddirfiles = zippeddir.namelist()
                                for zippedfiles in zippeddirfiles:
                                    if zippedfiles[-4:] == '.OUT':
                                        ZippedFileContents = zippeddir.open(zippedfiles)
                                        ZippedFileContentsRead = str(ZippedFileContents.read(), 'latin-1')
                                        if str(FileNumber) in ZippedFileContentsRead or str(FileNumber) in zippedfiles:
                                            if os.path.isdir(dstR) == True:
                                                zippeddir.extract(zippedfiles, path=dstR)
                                                print('R '+ str (zippedfiles) )
                                                ZippedFileContents.close()
                                            else:
                                                os.mkdir(dstR)
                                                zippeddir.extract(zippedfiles, path=dstR)
                                                print('R '+ str (zippedfiles) )
                                                ZippedFileContents.close()
                                        else:
                                            ZippedFileContents.close() 
                                zippeddir.close()                        
                                
            except Exception as e:
                        print(e)
                        pass
                    
    month, year = get_present_date()
    FileNumber, SendInd, ReceiveInd, DateRangeStartMM, DateRangeStartYY = get_user_input(month, year)
    RangestoSearch = Create_Range(DateRangeStartMM, DateRangeStartYY)
    dst = dircheck(FileNumber)
    Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch, dst)
    print('\nSearch complete\nFiles are available at E:\copy\\' + FileNumber + '\n')
    del FileNumber, SendInd, ReceiveInd, DateRangeStartMM, DateRangeStartYY, RangestoSearch, dst

def main():    
    search()
    while True:    
        Search_Again = input('Do you have another search? (Y/ N) ')
        if Search_Again.lower() == 'y':
            main()
        else:
            break
    quit()

if __name__ == '__main__':
    print('Welcome.\n\nUsing a file number this program will search through 3 months \nof send/receive directories based on the starting date provided.\n\nE.g., MM = 01, YY = 18 -> 2018-01, 2018-02, 2018-03')
    print('\nTo search for send files you will need a filer code. \nTo search for receive files you will need a database name.')
    main()
