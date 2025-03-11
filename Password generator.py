 import random
 
 name = input("Enter a keyword")
 name_keyword = name.split( )
 count = 0
 for name in name_keyword:
   count +=1
 password = ramdom.randint(0,count)
 print(f"Your password is: {password}")