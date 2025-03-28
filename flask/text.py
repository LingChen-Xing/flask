import base64
import json
import pymysql
from Demos.win32ts_logoff_disconnected import session
from flask import request
from flask import Response
import flask
import bs4
from flask import Flask
from scrapy.utils.response import response_status_message
from datetime import timedelta
from twisted.conch.insults.window import cursor

#可以把这两个都加进来

app = Flask(__name__,
            static_url_path='/static',#静态文件路径，当程序解析到这个static的时候，用读取文件的方法解析
            static_folder='static',#虽然现在比较智能了，但是还是写一下，计算机的优化是为了方便人类。但是我们不能因为这些方便失去解决问题的能力
            template_folder='templates'#模板文件，html文件就丢这里面
            )

def base64_e(a):
    bs = base64.b64encode(a.encode('utf-8'))
    bs1 = bs.decode('utf-8')
    #加密开关
    #bs1 = str(base64.b64decode(bs),"utf-8")#这是解密开关
    return bs1

#装饰器，关联路由
@app.route('/')
def index():
    #也就是说这里是把前端代码给搞出来了
    return "haha"

@app.route('/a/<user_id>/<int:user_pwd>')#这边就是只允许输入int类型的东西
def a_page(user_id,user_pwd):#这边传参的话数字字符串都能传，万一黑客进来干我怎么办
    #也就是说这里是把前端代码给搞出来了
    pwd = base64_e(str(user_pwd))
    return "this is a page ,welcome ,%s ,your password is \n%s"%(user_id,pwd)

@app.route('/b',methods=["GET"])#在函数里面传入参数的情况只能用于/
def b_page():#这边传参的话数字字符串都能传，玩意黑客进来干我怎么办
    uid = request.args.get('uname')#这边的话不允许乱来，不要直接引用requests，很多函数都是长的很像requests的，可能会搞错
    pwd = request.args.get('upd')#args只能在get中使用
    pwd = base64_e(str(pwd))

    if uid == 'dzy':
        return 'go out'
    return "this is b page ,welcome ,%s ,your password is \n%s"%(uid,pwd)

@app.route('/c',methods=["POST"])#这里换成POST方式了，如果不是POST方式进来是找不到这个网页的
def c_page():#这边传参的话数字字符串都能传，玩意黑客进来干我怎么办
    uid = request.form.get('uname')#这边的话不允许乱来，不要直接引用requests，很多函数都是长的很像requests的，可能会搞错
    pwd = request.form.get('upd')
    pwd = base64_e(str(pwd))
    return "this is c page ,welcome ,%s ,your password is \n%s"%(uid,pwd)

#这个d页面的东西是拿来测试使用方法的
@app.route('/d',methods=["GET","POST"])#这里POST和GET都能进来
def d_page():#这边传参的话数字字符串都能传，玩意黑客进来干我怎么办
    if request.method == 'GET':
        uid = request.args.get('uname')#这边的话不允许乱来，不要直接引用requests，很多函数都是长的很像requests的，可能会搞错
        pwd = request.args.get('upd')
    elif request.method == 'POST':
        uid = request.form.get('uname')
        pwd = request.form.get('upd')
    else:
        return 'ERROR'
    pwd = base64_e(str(pwd))

    #检测小开关
    a = "this is d page ,welcome ,%s\nyour password is %s"%(uid,pwd)
    a = Response(a, mimetype='text/plain')
    return a
    #return "%s"%(request.headers.get('User-Agent'))
    #return "%s"%(request.headers)#这是这哥们的请求头
    #return "%s"%(request.method)#这里是获取这哥们的请求方式
    #return "%s"%(request.headers.path)#这是这哥们的访问路径
    #return "%s"%(request.headers.full_path)#这是这哥们的全部访问路径
    #return "%s"%(request.base_url)#这是这哥们的访问的网站路径，是不是域名还没有测试，没有vps用，太穷了
    #return "%s"%(request.url)#这是这哥们的全部访问路径带参数
    #return "%s"%(request.user_agent.platform)#这是这哥们的操作系统
    #return "%s"%(request.user_agent.browser)
    #return "%s"%(request.user_agent)

#json
@app.route('/e')
def e_page():
    #搞个字典
    json_dict = {
        "name":"xiaoming",
        "age":"20",
        "score":"100"
    }

    result = json.dumps(json_dict)#字典转化为json字符串

    dict1 = json.loads(result)
    print(dict1["name"])
    return f'''  
        <pre>  
        JSON字符串:  
        {result}  

        解析后的字典:  
        {dict1}  
        </pre>  
        '''

#重定向
@app.route('/f')#这个/redirect一般就算重定向目录
def f_page():
    #跳转到其他的重定向，站外重定向
    #return flask.redirect('http://lcxing.com.cn')

    #站内，这是用函数名来找站内页面的
    return flask.redirect(flask.url_for('b_page',uname='dzy',upd=123))

@app.route('/g')#这个/redirect一般就算重定向目录
def g_page():

    return "可以在go页面用/传入参数，只能是数字"

@app.route('/g/<int:go>')#这个/redirect一般就算重定向目录
def go_page(go):

    if go==1:
        #跳转到其他的重定向，站外重定向
        return flask.redirect('http://lcxing.com.cn')

    #站内，这是用函数名来找站内页面的
    return flask.redirect(flask.url_for('b_page',uname='dzy',upd=123))

@app.route('/h')
def h_page():
    return flask.redirect(flask.url_for('i'))

@app.route('/i')
def i_page():
    return '你这么聪明，去控制台看看哪里不对劲吧！',404

#主动抛出异常
@app.route('/j')
def j_page():
    flask.abort(404)
    pass

#实验了那么久，就来返回一些好康的吧！
@app.route('/k')
def k_page():
    html='''
    <!-- index.html -->
<!DOCTYPE html>
<!-- 
  HTML核心方法库：
  1. 结构标签: <div>, <section>, <header>, <footer>
  2. 内容标签: <h1>-<h6>, <p>, <span>, <a>
  3. 媒体标签: <img>, <video>, <audio>
  4. 表单元素: <input>, <button>, <textarea>, <select>
  5. 元信息标签: <meta>, <link>, <title>
  6. 列表标签: <ul>, <ol>, <li>
  7. 语义化标签: <nav>, <article>, <aside>
-->
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="static/css/styles.css">
  <title>银狼前端训练场</title>
</head>
<body>
  <!-- 交互式导航栏 -->
  <nav class="main-nav">
    <ul>
      <li><a href="#home">主页</a></li>
      <li><a href="#about">关于</a></li>
    </ul>
  </nav>

  <!-- 卡片容器 -->
  <div class="card" id="mainCard" align="center">
    <h1 class="title">欢迎来到量子前端世界</h1>
    <button id="colorBtn">点击改变样式</button>
  </div>

  <script src="static/script.js"></script>
</body>
</html>
    '''
    return Response(html,200)

@app.route('/l')
def l_page():
    m_list = ["admiewang","dzy","xing","shen"]
    m_int=1
    m_str = "fuck"
    admin = "xing"
    return flask.render_template("moban.html",admin = admin,mint = m_int,mlist = m_list)

@app.route('/l/<id>')#这里可以调用传入id并调用，所有的参数传进来都是字符串
def l_a_page(id):
    admin = "xing"
    uid = 2
    if id != "dzy":
        str = "Good!"
        return flask.render_template("zi_moban.html",id = id,str = str,admin = admin,mint = uid)
    else:
        str = "Fuck you!"
        return flask.render_template("zi_moban.html", id= id,str = str,admin = admin,mint = uid)

#cookie设置
@app.route('/login')
def login_page():
    response = flask.make_response('success,please go back')
    response.set_cookie('user_id','10',max_age=500)
    response.set_cookie('vip', '0', max_age=500)#max_age是时间
    return response

#登出肯定要删除cookie
@app.route('/logout')
def logout_page():
    response = flask.make_response('out')
    response.delete_cookie('user_id','10')
    response.delete_cookie('vip', '0')
    return response

#其他网站读取cookie，当然，有些网站不会这么傻
@app.route('/m')
def m_page():
    user_id = request.cookies.get('user_id')
    vip = request.cookies.get('vip')
    print(vip)
    if user_id:
        html = f'''
        <!DOCTYPE html>
        <html>
        <body>
            <div align="center">
                <h1>用户面板</h1>
                <p>用户ID：{user_id}</p>
                <p>会员状态：{vip}</p>
            </div>
        </body>
        </html>
        '''
        return Response(html,200)
    else:
        return flask.redirect(flask.url_for('login_page'))

#session,使用session是要配置密钥的
app.config['SECRET_KEY']="haha"
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)#设置7天有效

#SESSION设置
@app.route('/login_plus')
def login_page_plus():
    response = flask.make_response('success,please go back')
    session['user_id']=20
    session['vip']=0
    return response

#登出肯定要删除session
@app.route('/logout_plus')
def logout_page_plus():
    response = flask.make_response('out')
    session.pop('user_id',None)
    #session['user_id']=False#这种也可以
    #session.clear()#全部干掉session
    session.pop('vip',None)
    return response

#其他网站读取cookie，当然，有些网站不会这么傻
@app.route('/n')
def n_page():
    try:
        user_id = session['user_id']
        vip = session['vip']#这东西就和个字典一样
        print(vip)
        if user_id:
            html = f'''
            <!DOCTYPE html>
            <html>
            <body>
                <div align="center">
                    <h1>用户面板</h1>
                    <p>用户ID：{user_id}</p>
                    <p>会员状态：{vip}</p>
                    <a href="/logout_plus">logout</a>
                </div>
            </body>
            </html>
            '''
            return Response(html,200)
        else:
            return flask.redirect(flask.url_for('login_page_plus'))
    except:
        return flask.redirect(flask.url_for('login_page_plus'))

#进行前端方面的测试时最好用无痕模式，这样的话可以防止缓存对实验结果造成影响，前端是最容易留缓存的一个地方
@app.route('/test1')
def text1():
    return flask.render_template('test1.html')
    pass

#处理
@app.route('/chuli',methods=['POST'])
def chuli():

    #数据库处理
    db = pymysql.connect(host="localhost",user="root",password="root",db="haha")
    #创建游标对象，相当于是一个指着数据库的指针，指向哪个数值，就读哪个数值
    cursor = db.cursor()
    #sql语句
    sql = "SELECT * FROM table1"
    sql1 = '''
        INSERT INTO table1(username,password)VALUES('test3','9999')
        '''
    try:
        cursor.execute(sql1)
        db.commit()  # 确认执行

    except:
        #执行失败，回滚并把数据还原
        db.rollback()
        return 0
    #sql = "SELECT * FROM table1 where id < 5"#那这边的话是不是可以接收参数了
    #执行sql语句
    cursor.execute(sql)
    db.commit()#确认执行
    #db.close()
    list1 = []
    for temp in cursor.fetchall():
        print(temp)#这边的话是一条一条的出来了,
        dict = {'名字':temp[1],'密码':temp[2]}
        list1.append(dict)
    db.close()#防止占用资源
    result = json.dumps(list1, sort_keys=True, ensure_ascii=False)#不编码
    print(result)


    #接收数据
    list1=[]
    for i in range(5):
        data = cursor.fetchone()#这里面取出来的东西是元组，元组是不可修改的，所以要转换
        li = list(data)#强制类型转换
        list1.append(li)
        print(list1[1][0])#取出list1中第二个元素的第一个数值，可以查了就能进行比对了
    print(list1)

    if request.method=="POST":
        usname = request.form.get('uname')
        passwd = request.form.get('passwd')
        if usname=="xing" and passwd=="1":
            return flask.render_template('admin.html')
        result = f'''
        <div align="center">
            <h1>用户提交了</h1><br>
            <h1>账号：{usname}</h1><br>
            <h1>账号：{passwd}</h1><br>
        </div>
        '''
        return Response(result,200)
    else:
        return "ERROR"


#别名
@app.route('/xixixixixi',endpoint='i')
def xixi_page():
    return 'xixi , you are in xixi_page'

#404重定向,这个就是所有的404都输出这个
@app.errorhandler(404)
def page_404(e):
    return '你要jb干嘛，路径都能写错',404

#405重定向
@app.errorhandler(405)
def page_405(e):
    return 'fuck，请求方式不对',405

#过滤器,取了个名字叫dore，do reserver，也就是翻转，在隔壁用管道符，懂得都懂
@app.template_filter('dore')
def do_reserver(li):
    temp = list(li)#不管进来什么东西我都他存在数组里
    temp.reverse()
    return temp

#这个玩意的功能非常简单
def main():

    #flask是轻量级web框架，也就是说他自己本身就是一个中间件，借助操作系统安装的环境去运行它，路由：什么路径可以访问到什么资源
    #app.run()
    app.run(host='0.0.0.0',port=8888,debug=True)#这个是我可以使用当前电脑上所有的ip，也就是不只是127.0.0.1

    pass

if __name__ == '__main__':
    main()