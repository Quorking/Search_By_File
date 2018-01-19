# -*- coding: utf-8 -*-
"""
Created on Sun 11/19 10:26:35 2017

Input -> file # to search for
Output -> Copied files in supplied path\Copied_Files

@author: Alec
"""
import datetime, os, zipfile, shutil

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
                FileNumber = int(input('\nPlease enter file number : '))
                if len(str(FileNumber)) > 8:
                    raise ValueError
                if len(str(FileNumber)) < 8:
                    raise ValueError
                break
            
            except ValueError:
                if len(str(FileNumber)) > 8:
                    print('\nThe input provided was greater than 8 digits. Please try again. ')
                if len(str(FileNumber)) < 8:
                    print('\nThe input provided was less than 8 digits. Please try again. ')
            
        #Get Send Indicator
        while True:
            try:
                SendInd = input('\nDo you want to search send files? (Y/N) ' ).lower()
                if not SendInd == 'y' and not SendInd == 'n':
                    raise TypeError
                break
            
            except TypeError:
                print('The input provided is not valid for this query. Please try again.')

            except:
                print('The input provided is not valid. Please try again.')

        #Get Receive Indicator
        while True:
            try:   
                ReceiveInd = input('\nDo you want to search receive files? (Y/N) ').lower()
                if not ReceiveInd == 'y' and not ReceiveInd == 'n':
                    raise TypeError
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
    
##  Search either Receive and/or Send directories using list of months to search
def Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch):
    ##RECEIVE SEARCH
    print('Processing...')
    if ReceiveInd == 'y':
        root = 'E:\\receive\\bdp'
        dst = 'E:\\copy\\receive'
        os.chdir(root)
        try:
            #Case 1 - Get Files in Current Receive Directory
            FilesToday = os.listdir(root)
            for file in FilesToday:
                if file[-4:] == '.ABI':
                    FileContents = open(root + str(file), 'r')
                    FileContentsRead = FileContents.read()
                    if str(FileNumber) in FileContentsRead:
                        if os.path.isdir(dst) == True:
                            shutil.copy(root + str(file), dst)
                        else:
                            os.mkdir(dst)
                            shutil.copy(root + str(file), dst)   
                    FileContents.close()
                    
            #Case 2 - Get Files from Past Receive Directories, and handle zip files
            HistReceiveDir = os.listdir(root + '\\' + 'history')
            for i in range(len(HistReceiveDir)):
                HistReceiveDir[i] = HistReceiveDir[i].replace('_', '-')
            os.chdir(root + '\\' + 'history')
            for dirs in RangestoSearch:
                for dirfiles in HistReceiveDir:
                    if dirfiles[:-6] == dirs:
                        if dirfiles[-4:] == '.ABI':
                            target = root + '\\' + 'history' + '\\'+ str(dirfiles.replace('-','_'))
                            FileContents = open(target, 'r')
                            FileContentsRead = FileContents.read()
                            if str(FileNumber) in FileContentsRead:
                                if os.path.isdir(dst) == True:
                                    shutil.copy(target, dst)
                                    print('R '+ str (target) )
                                else:
                                    os.mkdir(dst)
                                    shutil.copy(target, dst)
                                    print('R '+ str (target) )
                            FileContents.close()
                        if dirfiles[-4:] == '.zip':
                            target = root + '\\' + 'history' + '\\' + str(dirfiles.replace('-','_'))
                            zippeddir = zipfile.ZipFile(target, 'r')
                            zippeddirfiles = zippeddir.namelist()
                            for zippedfiles in zippeddirfiles:
                                if zippedfiles[-4:] == '.OUT':
                                    ZippedFileContents = zippeddir.open(zippedfiles)
                                    ZippedFileContentsRead = str(ZippedFileContents.read(), 'latin-1')
                                    if str(FileNumber) in ZippedFileContentsRead or str(FileNumber) in zippedfiles:
                                        print('R '+ str (zippedfiles) )
                                        if os.path.isdir(dst) == True:
                                            zippeddir.extract(zippedfiles, path=dst)
                                            ZippedFileContents.close()
                                        else:
                                            os.mkdir(dst)
                                            zippeddir.extract(zippedfiles, path=dst)
                                            ZippedFileContents.close()
                                    else:
                                        ZippedFileContents.close() 
                            zippeddir.close()                        
                            
        except Exception as e:
                    print(e)
                    pass
                
    ##SEND SEARCH    
    if SendInd == 'y':
        root = 'E:\\Send\\hist\\'
        dst = 'E:\\copy\\send'
        os.chdir(root)
        try:
            #Case 1 - Get Files in Current Send Directory
            FilesToday = os.listdir(root)
            for file in FilesToday:
                if file[-4:] == '.ABI':
                    FileContents = open(root + str(file), 'r')
                    FileContentsRead = FileContents.read()
                    if str(FileNumber) in FileContentsRead:
                        if os.path.isdir(dst) == True:
                            shutil.copy(root + str(file), dst)
                            print('S '+ str(file) )
                        else:
                            os.mkdir(dst)
                            shutil.copy(root + str(file), dst)
                            print('S '+ str(file) )
                    FileContents.close()
                    
            #Case 2 - Get Files from Past Send Directories, and handle zip files
            for dirs in RangestoSearch:
                if os.path.isdir(root + str(dirs)) == True:
                    os.chdir(root + str(dirs))
                    dirlist = os.listdir()
                    for dirfiles in dirlist:
                        #print('Moving through directory -Pass- ' + dirs)
                        if dirfiles[-4:] == '.ABI':
                            target = str(root) + str(dirs) + '\\' + str(dirfiles)
                            FileContents = open(target, 'r')
                            FileContentsRead = FileContents.read()
                            if str(FileNumber) in FileContentsRead:
                                if os.path.isdir(dst) == True:
                                    shutil.copy(target, dst)
                                    print('S '+ str(dirfiles) )
                                else:
                                    os.mkdir(dst)
                                    shutil.copy(target, dst)
                                    print('S '+ str(dirfiles) )
                            FileContents.close()
                        if dirfiles[-4:] == '.zip':
                            target = str(root) + str(dirs) + '\\' + str(dirfiles)
                            zippeddir = zipfile.ZipFile(target, 'r')
                            zippeddirfiles = zippeddir.namelist()
                            for zippedfiles in zippeddirfiles:
                                if zippedfiles[-4:] == '.ABI':
                                    ZippedFileContents = zippeddir.open(zippedfiles)
                                    ZippedFileContentsRead = str(ZippedFileContents.read(), 'latin-1')
                                    if str(FileNumber) in ZippedFileContentsRead or str(FileNumber) in zippedfiles:
                                        if os.path.isdir(dst) == True:
                                            zippeddir.extract(zippedfiles, path=dst)
                                            print('S '+ str(zippedfiles) )
                                            ZippedFileContents.close()
                                        else:
                                            os.mkdir(dst)
                                            zippeddir.extract(zippedfiles, path=dst)
                                            print('S '+ str(zippedfiles) )
                                            ZippedFileContents.close()
                                    else:
                                        ZippedFileContents.close()
                            zippeddir.close()                        
                            
        except Exception as e:
                    print(e)
                    pass
    
def main():
    month, year = get_present_date()
    FileNumber, SendInd, ReceiveInd, DateRangeStartMM, DateRangeStartYY = get_user_input(month, year)
    RangestoSearch = Create_Range(DateRangeStartMM, DateRangeStartYY)
    Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch)
    print('\nSearch complete\nFiles are available at E:\copy\send & E:\copy\\receive')
    while True:    
        again = input('Do you have another search? (Y/N) ')
        if again.lower() == 'y':
            main()
        else:
            break
    quit()

if __name__ == '__main__':
    print('Welcome.\n\nUsing a file number this program will search through 3 months \nof send/receive directories based on the starting date provided.\n\nE.g., MM = 01, YY = 18 -> 2018-01, 2018-02, 2018-03')
    main()
