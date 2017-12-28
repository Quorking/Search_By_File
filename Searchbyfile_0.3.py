# -*- coding: utf-8 -*-
"""
Created on Sun 11/19 10:26:35 2017

Input -> file # to search for
Output -> Copied files in supplied path\Copied_Files

@author: Alec
"""
import datetime, os, zipfile, shutil

##def read_zip_file(filepath):
##    zfile = zipfile.ZipFile(filepath)
##    for info in zfile.infolist():
##        file = zfile.open(info)
##        line_list = file.readlines()

def get_present_date():
    timeanddate = str(datetime.datetime.now())
    month = timeanddate[5:7]
    year = timeanddate[2:4]
    return month, year
    
def get_user_input(month, year):
    while True:
        #File Number
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
            
        #Send Indicators
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

        #Receive Indicator
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
 
        #Starting Date Range, Month and Year
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
                    print(year)
                    
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
        YeartoSearch = int(DateRangeStartYY[:].strip('0'))
        
        if MonthtoSearch > 12:
            YeartoSearch = int(DateRangeStartYY[:].strip('0'))
            YeartoSearch+=1
            MonthtoSearch = MonthtoSearch - 12
            MonthtoSearch = str('0' + str(MonthtoSearch))
        RangestoSearch.append('20' + str(YeartoSearch) + '-' + str(MonthtoSearch))
        
    return RangestoSearch
    
##  Search with list of months to search, check send/receive indicators
def Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch):
    root = 'E:\\Send\\hist\\'
    dst = 'E:\\copy'
    
    if SendInd == 'y':
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
                        else:
                            os.mkdir(dst)
                            shutil.copy(root + str(file), dst)
                            
                    FileContents.close()
                    
            #Case 2 - Get Files from Past Send Directories, and handle zip files
            for dirs in RangestoSearch:
                print(RangestoSearch)
                
                if os.path.isdir(root + str(dirs)) == True:
                    os.chdir(root + str(dirs))
                    dirlist = os.listdir()
                    print(dirlist)
                    
                    for dirfiles in dirlist:
                        print('Moving through directory -Pass- ' + dirs)
                        
                        if dirfiles[-4:] == '.ABI':
                            target = str(root) + str(dirs) + '\\' + str(dirfiles)
                            print('Moving through files -Pass- ' + dirfiles + ' ' + target)
                            FileContents = open(target, 'r')
                            FileContentsRead = FileContents.read()
                            
                            if str(FileNumber) in FileContentsRead:
                                print(dirfiles + ' ABI')
                                if os.path.isdir(dst) == True:
                                    shutil.copy(target, dst)
                                else:
                                    os.mkdir(dst)
                                    shutil.copy(target, dst)
                            FileContents.close()
                            print('pass')
                            
                        if dirfiles[-4:] == '.zip':
                            target = str(root) + str(dirs) + '\\' + str(dirfiles)
                            print('zip' + target)
                            zippeddir = zipfile.ZipFile(target, 'r')
                            zippeddirfiles = zippeddir.namelist()
                            print('unzipped' + target)
                            for zippedfiles in zippeddirfiles:
                                print('unzipped' + zippedfiles)
                                if zippedfiles[-4:] == '.ABI':
                                    #targetzip = str(root) + str(zippedfiles)
                                    ZippedFileContents = zippeddir.open(zippedfiles)
                                    ZippedFileContentsRead = ZippedFileContents.read()
                                    print('Reading file from zip archive ' + zippedfiles)
                                    print(ZippedFileContentsRead)
                                    print(FileNumber)
                                    if str(FileNumber) in ZippedFileContentsRead:
                                        print('Yes')
                                        if os.path.isdir(dst) == True:
                                            shutil.copy(targetzip, dst)
                                        else:
                                            os.mkdir(dst)
                                            shutil.copy(targetzip, dst)
                                    else:
                                        print('else')
                                        ZippedFileContents.close()
                            zippeddir.close()                        
                            
        except:
                    print('Problem')
    
#def
month, year = get_present_date()
FileNumber, SendInd, ReceiveInd, DateRangeStartMM, DateRangeStartYY = get_user_input(month, year)
RangestoSearch = Create_Range(DateRangeStartMM, DateRangeStartYY)
Search_Directories(FileNumber, SendInd, ReceiveInd, RangestoSearch)

#def main():

#if __name__ == '__main__':
  #main()
