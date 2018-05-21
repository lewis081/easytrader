

import easytrader

cookies1='aliyungf_tc=AQAAAD7JNHKvfA0AH3v1ehk5UqyYDyly; device_id=b9405d98fcd29da83d80a0b6a2619f27; snbim_minify=true; s=f512bccsu7; bid=fd9a8893ad1cd19d3842187802b0fe54_jdkb8czy; __utmc=1; __utmz=1.1525187205.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1525187205; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=4b814328d66f0eee19984308c72cfcd267f24c3a; xq_a_token.sig=Ive5YAB3BRkSCse21lABJ5q0V14; xq_r_token=e3405a6ac01640314a2a9e524fd3220a206830d7; xq_r_token.sig=xqTgU7jBY-w6XGvRn2L9reBMwCE; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=4548762178; u.sig=Pi4n9y2wBSu-pfSuwcjZI1Fi5ak; __utma=1.2110886982.1525187205.1525393014.1525441756.5; __utmt=1; __utmb=1.6.10.1525441756; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1525441909'
p_code='ZH010389'

# create user
xq = easytrader.CreateXueqiuVisitor()
xq.login(cookies=cookies1)
user = easytrader.use('gj_client')
user.setXueqiu(xq)

# create follower
xq_follower = easytrader.follower('xq')
xq_follower.login(cookies=cookies1)


# follow
print('follower user')
xq_follower.follow(user, p_code, total_assets=10000000)


#print('more test')
#print(user.get_position())
