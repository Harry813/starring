from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

NavItems = [
    {"name": _("移民"), "link": "#"},
    {"name": _("留学"), "link": "#"},
    {"name": _("旅游"), "link": "#"},
    {"name": _("工作"), "link": "#"},
    {"name": _("加拿大咨询"), "link": "#"},
    {"name": _("关于我们"), "link": "#"}
]

# 首页项目清单
IndexListItems = [
    {"name": _("我要移民"),
     "items": [
         {"name": _("投资与企业家移民"), "linkName": "#"},
         {"name": _("技术/雇主担保移民"), "linkName": "#"},
         {"name": _("留学生移民途径"), "linkName": "#"},
         {"name": _("特需人才移民"), "linkName": "#"},
         {"name": _("家庭团聚移民"), "linkName": "#"},
         {"name": _("移民实用工具"), "linkName": "#"},
         {"name": _("移民相关Q&A"), "linkName": "#"},
         {"name": _("免费评估"), "linkName": "#"},
         {"name": _("其他移民相关服务"), "linkName": "#"},
     ]},
    {"name": _("我要留学"),
     "items": [
         {"name": _("留学申请"), "linkName": "#"},
         {"name": _("微留学/游学"), "linkName": "#"},
         {"name": _("DLI认真的教育机构"), "linkName": "#"},
         {"name": _("冬令营/夏令营"), "linkName": "#"},
         {"name": _("学签申请"), "linkName": "#"},
         {"name": _("VIP就业与生活服务"), "linkName": "#"},
     ]},
    {"name": _("我要工作"),
     "items": [
         {"name": _("留学生工作签证"), "linkName": "#"},
         {"name": _("短期签证"), "linkName": "#"},
         {"name": _("各类签证及申请"), "linkName": "#"},
     ]},
    {"name": _("我要旅游"),
     "items": [
         {"name": _("其他工作签证"), "linkName": "#"},
         {"name": _("签证相关其他服务"), "linkName": "#"},
         {"name": _("免费评估"), "linkName": "#"},
         {"name": _("疫情期间临时移"), "linkName": "#"},
         {"name": _("联邦EE快速通道"), "linkName": "#"},
         {"name": _("VIP量身定制"), "linkName": "#"},
     ]},
    {"name": _("加拿大咨询"),
     "items": [
         {"name": _("加拿大护工移民"), "linkName": "#"},
         {"name": _("特色包车游"), "linkName": "#"},
         {"name": _("特色旅游路线"), "linkName": "#"},
         {"name": _("加拿大小众之旅"), "linkName": "#"},
         {"name": _("加拿大安家落地服务"), "linkName": "#"},
         {"name": _("加拿大各省介绍"), "linkName": "#"},
         {"name": _("BC省学校排名"), "linkName": "#"},
         {"name": _("加拿大教育"), "linkName": "#"},
         {"name": _("移民新政和社会新闻"), "linkName": "#"},
         {"name": _("加拿大衣食住行"), "linkName": "#"},
     ]},
]

Intentions = (
    ("IMMI", _("加拿大移民")),
    ("STUD", _("加拿大留学")),
    ("WORK", _("加拿大工作")),
    ("FAMR", _("家庭团聚")),
    ("HOME", _("安家置业")),
    ("APPL", _("案件上诉")),
    ("OTHR", _("其他，请详细说明")),
)

VipLevel = (
    (1, _("IS访客")),
    (2, _("IS会员")),
    (3, _("IS-VIP")),
)

ContactTypes = (
    ("WHATSAPP", _("WhatsApp")),
    ("WECHAT", _("微信"))
)
