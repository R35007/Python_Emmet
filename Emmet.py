import re

def formatTag(a):
   myClass=''
   myId=''
   myTagName=''
   classname='false'
   IdName='false'
   result=[]

   for i in a:
       if i=='.':
           classname= 'true'
           IdName= 'false'
       elif i=='#':
           IdName= 'true'
           classname= 'false'

       if classname=='true':
          myClass+=i
       if IdName=='true':
           myId+=i
       if not classname=='true' and not IdName=='true':
           myTagName+=i

   if len(myTagName)==0:
       myTagName="div"

   myClass=myClass.split('.')
   myId=myId.split('#')
   ClassName=' '.join(myClass)
   ClassName=ClassName.strip()

   if len(myId[-1])==0 and len(ClassName)>0:
       result.append('<'+myTagName+' class="'+ClassName+'">')
   elif len(myId[-1])>0 and len(ClassName)==0:
       result.append('<'+myTagName+' id="'+myId[-1]+'">')
   elif len(myId[-1])>0 and len(ClassName)>0:
       result.append('<'+myTagName+' class="'+ClassName+'" id="'+myId[-1]+'">')
   else:
       result.append('<'+myTagName+'>')
   result.append('</'+myTagName+'>')
   return result


def SplitIt(x):
   plusindex=x.find('+')
   gtindex=x.find('>')

   if plusindex==-1 and not gtindex==-1:
       plusindex=gtindex+1

   if gtindex==-1 and not plusindex==-1:
       gtindex=plusindex+1

   if plusindex==-1 and gtindex==-1:
       myTags=formatTag(x)
       return myTags
   elif plusindex<gtindex or gtindex==-1:
       output=''
       y=x.split(x[plusindex],1)
       for i in y:
           Tags = SplitIt(i)
           output += Tags[0]+Tags[1]
       return [output,'']
   elif gtindex<plusindex or plusindex==-1:
       innerTag=''
       z=x.split(x[gtindex],1)
       endTags = []
       j=0
       while j<len(z):
           Tags=SplitIt(z[j])
           if(j==len(z)-1):
               innerTag += Tags[0]+Tags[1]
           else:
               endTags.append(Tags[1])
               innerTag += Tags[0]
           j+=1
       joinendTags = '\n'.join(endTags)
       return [innerTag,joinendTags]

def generateTags(a):
   myOutputList = SplitIt(a)
   jointresult = ''.join(myOutputList).strip()
   return jointresult

a = "span.Test1#myId.Test2#myId1>ul.nav.navbar+div.Test1#myId.Test2#myId1>ul.nav.navbar+div.Test1#myId.Test2#myId1>ul.nav"
#a = input()
#a='.test+ul.myclass'
#a='.test>ul.myclass'
#a = ".Test+ul>li"
#a = "ul.Test>li+a"

print(generateTags(a))
