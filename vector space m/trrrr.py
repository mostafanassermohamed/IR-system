from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
import random , os ,math,re

list_of_chars = ['A', 'B', 'C', 'D', 'E', 'F']

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
            pattern=r'^<([A-F]:0.[0-9];)+>$' 
            res=re.match(pattern,qry_str)
            print(res)
            if res:
                  print("correct")
            else:
                  print("uncorrect")
            if res !=None:    
                print(qry_str)
                open('Q.txt','r+').write(str(qry_str))       #store query in doc

                print(str(open('Q.txt','r+').readlines()))
                print(request.form['way'])
                list_of_doc = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
                if request.form['way'] == 'Random':                                               #random or not
                    for k in list_of_doc:
                        random_size = random.randint(3, 11)
                        print(random_size)
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

                    for a2 in list_of_chars:  # to count the number of char in the doc
                        s = tmp_str.count(a2)
                        j.update({a2: s})
                        tmp_dic.update({a2: s/(tmp_str.count(max(tmp_str, key=tmp_str.count)))})
                        
                    print(j)    
                    print(tmp_dic)
                    tf_dic.update({a.replace(".txt", ""): tmp_dic})
                    print(tf_dic)
                # calculate itf___________________________________________________________________________________
                itf_dic= {}
                for a in list_of_chars:
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
                print("tf-idf",t)
                print("tf-idf",q)
                sim_dic={}
                for key1 , value1 in t.items():   # claculate similarity
                    tmp= {}
                    score=0
                    for key2, value2  in value1.items():
                        if key2 in q:
                            score= score+(float(value1[key2]) * float(q[key2]))
                
                    sim_dic.update({key1:score})
                print("sim_dic",sim_dic)
                L=sorted (sim_dic.items(), key=lambda i:(i[1], i[0]), reverse=True)       
                return render_template('vector_s.html',list=L)
            else:
                return render_template('vector_s.html',err="error")   
        return render_template('vector_s.html',list=[])

if __name__ == '__main__':
	app.run(debug = True)