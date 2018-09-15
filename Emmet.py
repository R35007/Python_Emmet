import re
from lxml import etree, html


def getInputType(x):
    if x=='s':return 'submit'
    elif x=='h':return 'hidden'
    elif x=='b':return 'button'
    elif x=='r':return 'reset'
    elif x=='p':return 'password'
    elif x=='c':return 'cancel'
    elif x=='clr':return 'color'
    elif x=='d':return 'date'
    elif x=='e':return 'email'
    else:return ''

def formatTag(a):

    myClass=myId=myTagName=myType=myText=''
    classname=IdName=TypeName=innerText='false'
    result=[]

    if '*' in a:
        b=a.split('*')
        c=b[0]
    else:c=a

    for i in c:

        if i=='.':
            classname= 'true'
            IdName=TypeName=innerText='false'
        elif i=='#':
            IdName= 'true'
            classname=TypeName=innerText='false'
        elif i==':':
            TypeName='true'
            IdName=classname=innerText='false'
        elif i=='{':
            innerText='true'
            IdName=classname=TypeName='false'

        if classname=='true':myClass+=i
        if IdName=='true':myId+=i
        if TypeName=='true':myType+=i
        if innerText=='true':myText+=i
        if not classname=='true' and not IdName=='true' and not TypeName=='true' and not innerText=='true':myTagName+=i

    myClass=myClass.split('.')
    myId=myId.split('#')
    myType=myType.split(':')
    myText = myText.replace('{',' ').replace('}',' ').split()


    ClassName=' '.join(myClass)
    ClassName=ClassName.strip()
    InnerText=' '.join(myText)
    InnerText=InnerText.strip()

    if len(ClassName)>0:cn=' class="'+ClassName+'"'
    else:cn=''
    if len(myId[-1])>0:mi=' id="'+myId[-1]+'"'
    else:mi=''
    if len(myType[-1])>0:
        inputType = getInputType(myType[-1])
        if len(inputType)>0:mt=' type="'+inputType+'" name=""'
        else:mt=''
    else:mt=''
    if len(InnerText)>0:it='<label>'+InnerText+'</label>'
    else:it=''

    if len(myTagName)==0 and (len(cn)>0 or len(mi)>0 or len(mt)>0):myTagName="div"
    elif len(myTagName)==0:myTagName=''

    if len(myTagName)>0:
        result.append('<'+myTagName+mt+mi+cn+'>'+it)
        result.append('</'+myTagName+'>')
    else:
        result.append(it)
        result.append('')

    if '*' in a:result.append(b[1])
    else:result.append(1)

    return result


def SplitIt(x):

    plusindex=x.find('+')
    gtindex=x.find('>')

    if plusindex==-1 and not gtindex==-1:plusindex=gtindex+1
    if gtindex==-1 and not plusindex==-1:gtindex=plusindex+1

    if plusindex==-1 and gtindex==-1:
        myTags=formatTag(x)
        return myTags
    elif plusindex<gtindex or gtindex==-1:  #Split by Plus +
        output=''
        y=x.split(x[plusindex],1)
        for i in y:
            Tags = SplitIt(i)
            combinetags = Tags[0]+Tags[1]
            mutiplytags = combinetags*int(Tags[2])
            output += mutiplytags

        return [output,'',1]
    elif gtindex<plusindex or plusindex==-1:    #Split by Plus >
        innerTag=''
        z=x.split(x[gtindex],1)
        endTags = []
        j=0
        multiplyby = 1
        while j<len(z):
            Tags=SplitIt(z[j])
            if(j==len(z)-1):
                innerTag += (Tags[0]+Tags[1])*int(Tags[2])
            else:
                multiplyby = Tags[2]
                endTags.append(Tags[1])
                innerTag += Tags[0]
            j+=1

        joinendTags = ''.join(endTags)
        multiTags = (innerTag+joinendTags)*int(multiplyby)

        return [multiTags,'',1]


def generateMyTags(Emmet_Code):
    myOutputList = SplitIt(Emmet_Code)
    multiOutput = (myOutputList[0]+myOutputList[1])*int(myOutputList[2])
    jointresult = ''.join(multiOutput.strip())
    document_root = html.fromstring(jointresult)
    output = etree.tostring(document_root, encoding='unicode', pretty_print=True)
    return output

#a = input()
#a='.test+ul.myclass'
#a='.test>ul.myclass'
#a = ".Test+ul>li"
#a = "ul.Test>li+a"
#a = "span.Test1#myId.Test2#myId1>ul.nav.navbar+div.Test1#myId.Test2#myId1>ul.nav.navbar+div.Test1#myId.Test2#myId1>ul.nav"
a = "span.Test1#myId.Test2#myId1*2>ul.nav.navbar*2+div.Test1#myId.Test2#myId1*2>ul.nav.navbar*2+div.Test1#myId.Test2#myId1*2>ul.nav*3"


print(generateMyTags(a))



