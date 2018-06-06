

import easytrader

cookies1='aliyungf_tc=AQAAAKjOWGCVsA0AZTG+J+yCglPq/Ct3; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1528209508; __utmc=1; captcha_id=mHbDIYeiuPfnEHRDI4sZ8lp5pyR7yN; xq_a_token=3cac49f26dc327bc1027736262115f6723937c12; xq_a_token.sig=dSer2kNG7jwRPcHJ_4bSD4s7GTw; xq_r_token=fcd354b99bb4892bfa1ffefa94f9d6dcf4c05f6e; xq_r_token.sig=OSh88CBB8d4sqAC7ZlJkAuSxl4A; __utmz=1.1528122245.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); device_id=5818210b6297e66ff605a5014cab1a27; __utma=1.1589166500.1528122245.1528122245.1528122245.1; s=g013vd65fo; u=4548762178; Hm_lvt_1db88642e346389874251b5a1eded6e3=1528122185; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=Pi4n9y2wBSu-pfSuwcjZI1Fi5ak'
p_code='ZH010389'
# p_code='ZH1335122'

# create visitor
xq = easytrader.CreateXueqiuVisitor()
xq.login(cookies=cookies1)

user = easytrader.use('gj_client')
user.setXueqiu(xq)
user.login('40095305', '764241', "C:\\全能行证券交易终端\\xiadan.exe")

# create follower
xq_follower = easytrader.follower('xq')
xq_follower.login(cookies=cookies1)
xq_follower.follow([], p_code, track_interval=4, total_assets=10000000)


#create user and bridge
# user   = easytrader.use('xq')
bridge = easytrader.TraderBridge(xq_follower.getQueue(), user)
bridge.trade()

#print('more test')
#print(user.get_position())
