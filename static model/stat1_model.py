from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
import random
list_of_chars = ['A', 'B', 'C', 'D', 'E', 'F']
list_of_doc = ['D1.txt', 'D2.txt', 'D3.txt','D4.txt']
#----------------------------------------------------------
#score function
def cal_score(doc_dic,q_dic):
    score_dic= {}
    for key1 , value1 in doc_dic.items():
        score=0
        for key2, value2  in value1.items():
            for key3 ,value3 in q_dic.items():
                if key2==key3 :
                   score = score +(value2 * value3)
        score_dic.update({key1:score})
    return score_dic
#________________________________________________________________________________

# this function if the files created randomly
@app.route('/search', methods =['GET', 'POST'] )
def search():
    if request.method== 'POST' :
        L=[]
        qry_str = request.form['query']
        print(qry_str)
                     #handel query
        qry_str = list(qry_str.replace('>', '').replace('<', '').split(";"))
        dic_q ={}      # this dic will save query

        for k in qry_str: #store query in dic
            t = k.split(":")
            dic_q.update({t[0]: float(t[1])})
        
        for k in list_of_chars:
            if k not in dic_q:
                dic_q.update({k:0})

        fill_method=request.form['way']
        print(fill_method)
        if fill_method == 'Random':
            
            for k in list_of_doc:
                random_size = random.randint(3, 11)
                temp = []
                for i in range(random_size):
                    st = random.choice(''.join(list_of_chars))
                    temp.append(st)
                Doc = open(k, "r+")
                Doc.write(''.join(temp))
    # calculation
        prob_dic = {}
        for a in list_of_doc:
            tmp_dic = {}
            j = {}
            tmp_str = str(open(a).readlines())
            print(tmp_str)
            for a2 in list_of_chars:  # to count the number of char in the doc
                s = tmp_str.count(a2)
                tmp_dic.update({a2: s/(len(tmp_str)-4)})
                j.update({a2: s})
            print(j)    
            print(tmp_dic)
            prob_dic.update({a.replace(".txt", ""): tmp_dic})
            dic_s=cal_score(prob_dic, dic_q)
            print(dic_s)
            L=sorted (dic_s.items(), key=lambda i:(i[1], i[0]), reverse=True)
            print(L)
        return render_template('stat_model.html',list=L)
    return render_template('stat_model.html',list=[])

if __name__ == '__main__':
	app.run(debug = True)