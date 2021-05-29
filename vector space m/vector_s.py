from flask import Flask,render_template,request,redirect,url_for
import sys
sys.path.append("c:/program files/python37/lib/site-packages")
import pygal
from math import cos
app = Flask(__name__)
import random , os ,math,re

list_of_chars = ['A', 'B', 'C', 'D', 'E', '1', '2', '3', '4', '5']

#----------------------------------------------------------
#score function
def cal_wieght(itf_dic,tf_dic):
    wieghts_dic= {}
    for key1 , value1 in tf_dic.items():
        tmp= {}
        for key2, value2  in value1.items():
             if key2 in itf_dic:
                tmp.update({key2:(float(value1[key2]) * float(itf_dic[key2]))})
                
        wieghts_dic.update({key1:tmp})
    return wieghts_dic
#________________________________________________________________________________


# this function if the files created randomly
@app.route('/search2', methods =['GET', 'POST'] )
def search():
    if request.method== 'POST' :
        L=[]
        qry_str = request.form['query']
        
        print(qry_str)
        open('Q.txt','r+').write(str(qry_str))       #store query in doc

        print(str(open('Q.txt','r+').readlines()))
        print(request.form['way'])
        list_of_doc = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
        if request.form['way'] == 'Random':                                               #random or not
            for k in list_of_doc:
                random_size = random.randint(3, 10)
                temp = []
                for i in range(random_size):
                    st = random.choice(''.join(list_of_chars))
                    temp.append(st)
                open(k, "r+").write(''.join(temp))
                
    # calculation tf _____________________________________________________________
        list_of_doc = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt','Q.txt']
        tf_dic= {}
        for a in list_of_doc:
            tmp_dic = {}
            j = {}
            tmp_str =str(open(a).readlines())
            print(tmp_str)

            for a2 in list_of_chars: 
              p=['1','2','3','4','5']
              if a2 not in p: # to count the number of char in the doc
                s = tmp_str.count(a2)
                j.update({a2: s})
                for i in p:
                    tmp_str=tmp_str.replace(i,"")
                tmp_dic.update({a2: s/(tmp_str.count(max(tmp_str,key=tmp_str.count)))})
                
            print(j)    
            print(tmp_dic)
            tf_dic.update({a.replace(".txt", ""): tmp_dic})
            print(tf_dic)
        # calculate itf___________________________________________________________________________________
        itf_dic= {}
        for a in list_of_chars:
          if a not in p:
            count= 0
            for a2 in list_of_doc:
                if a in str(open(a2).readlines()):
                   count=count+1
            print(count)
            if count!=0:
               t=math.log2(len(list_of_doc)/count) 
            else:
              t=0
            itf_dic.update({a:t})     
        print("itf_dic",itf_dic) 
        t=cal_wieght(itf_dic,tf_dic)      # tf*idf
        q=t['Q']
        del t['Q']
        print("tf*idf",t)
        print(q)
        sim_dic={}
        for key1 , value1 in t.items():   # claculate similarity
            tmp= {}
            score=0
            for key2, value2  in value1.items():
                if key2 in q:
                    score= score+(float(value1[key2]) * float(q[key2]))
          
            sim_dic.update({key1:score})
        print(sim_dic)
        L=sorted (sim_dic.items(), key=lambda i:(i[1], i[0]), reverse=True) 
        '''--------------------------- link analysis   ---------------------------- '''
        list_of_doc = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
        import numpy as np

        adj_matrix=np.zeros((5,5))
        for a in list_of_doc:
            tmp=open(a,'r').readlines()
            for b in range(5):
                if (str(b+1) in str(tmp)) and ((b) != list_of_doc.index(a)) : # ignore looooops
                    adj_matrix[list_of_doc.index(a)][b]=1
        adj_matrix_T=np.transpose(adj_matrix)
        a=np.array([[1,1,1,1,1]]).T
        h=a
        print('initial a,h =', a,h)
        print("adj matrix",adj_matrix)
        print("adj matrix transpose",adj_matrix_T)

        for i in range(20):
            a=np.dot(adj_matrix_T,h)
            a=a/(np.sqrt(np.sum(np.power(a,2))))
            h=np.dot(adj_matrix,a)
            h=h/(np.sqrt(np.sum(np.power(h,2))))
             

        a=np.array(a).tolist()
        h=np.array(h).tolist()
        print('Authority =',a)
        print('Hubs=',h)
        result={}
        result1={}
        for i in range(5):
            result.update({list_of_doc[i]:a[i]})
        L1=sorted(result.items(), key=lambda i:(i[1], i[0]), reverse=True) 
        for i in range(5):
            result1.update({list_of_doc[i]:h[i]})
        L2=sorted(result1.items(), key=lambda i:(i[1], i[0]), reverse=True)
        print(L1)
        #bar
        line_chart = pygal.Bar()
        # line_chart = pygal.HorizontalBar()
        line_chart.title = 'Authority and Hubs'
        line_chart.x_labels = map(str, range(1,6))
        a=np.array(a)
        h=np.array(h)
        print(result1)
        line_chart.add('Authority',[x[0] for x in result.values()])#[a[[0]],a[[1]],a[[2]],a[[3]],a[[4]]])
        line_chart.add('HUBS',[x[0] for x in result1.values()])#[h[0],h[1],h[2],h[3],h[4] ])
        graph_data = line_chart.render_data_uri()
       
        return render_template('vector_s.html',list=L, list1=L1,list2=L2, graph_data= graph_data)
        
    return render_template('vector_s.html',list=[] ,list1=[],list2=[] )

if __name__ == '__main__':
	app.run(debug = True)