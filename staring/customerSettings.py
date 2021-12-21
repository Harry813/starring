from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n

from django.urls import reverse

Languages = [
    {"CODE": "zh-hans", "NAME": "简体中文", "FLAG": "IMG/FLAGS/CHN.gif"},
    {"CODE": "en-us", "NAME": "English", "FLAG": "IMG/FLAGS/USA.gif"}
]

Roles = [
    ("STAFF", _("职员")),
    ("LEADER", _("组长")),
    ("MANAGER", _("经理")),
    ("DIRECTOR", _("总监"))
]

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

Intentions = [
    ("IMMI", _("加拿大移民")),
    ("STUD", _("加拿大留学")),
    ("WORK", _("加拿大工作")),
    ("FAMR", _("家庭团聚")),
    ("HOME", _("安家置业")),
    ("APPL", _("案件上诉")),
    ("OTHR", _("其他，请详细说明")),
]

VipLevel = [
    (0, _("普通访客")),
    (1, _("IS访客")),
    (2, _("IS会员")),
    (3, _("IS-VIP")),
]

ContactTypes = [
    ("WHATSAPP", _("WhatsApp")),
    ("WECHAT", _("微信"))
]

ArticleStatus = [
    ("PUBLISH", _("已发布")),
    ("PENDING", _("待审核")),
    ("REJECT", _("审核失败")),
    ("REVISED", _("需要修订")),
    ("DRAFT", _("正在编辑")),
    ("DELETE", _("已删除"))
]

article_Search_type = [
    ("TITLE", _("标题")),
    ("CONTENT", _("内容")),
    ("TC", _("标题与内容")),
    ("AUTHOR", _("作者")),
    ("KEYWORD", _("META标签-关键词")),
    ("DESCRIPTION", _("META标签-简介"))
]

ADMMegaMenu = (
    {"name": _("Test1"),
     "items": [
         {"name": _("Test1-1"), "linkName": "#"},
         {"name": _("Test1-2"), "linkName": "#"},
     ]},
)

IndexCarousel = [
    ("NEWS", _("时事要文")),
    ("MIGR", _("移民留学")),
    ("WORK", _("工作生活")),
    ("EDUC", _("亲子教育")),
]

customer_tags = [
    ('VISITOR', _('访客')),
    ('POTENTIAL', _('意向访客')),
    ('SIGN', _("签约用户")),
    ('REFERRER', _('推荐人')),
    ('AGENT', _('代理商')),
    ('PARTNER', _('合作伙伴'))
]

user_Search_type = [
    ('UID', "UID"),
    ('UNM', _("用户名")),
    ('RNM', _("姓名"))
]

staff_tags = [
    ('ADMIN', _('管理团队')),
    ('MARKET', _('市场部')),
    ('SALES', _('销售部')),
    ('COPYWRITE', _('文案部')),
    ('TRAVEL', _('旅游部')),
    ('MANITOBA', _('曼省分公司')),
    ('NEWFOUND', _('纽省分公司')),
    ('QUEBEC', _('魁省分公司')),
]

meeting_status = [
    ('APPLY', _("申请已提交")),
    ('ACCEPT', _("预约成功")),
    ('REJECT', _("预约失败")),
    ('FINISH', _("此次会议已结束")),
    ('TIMEOUT', _("逾时未参与"))
]

navigator_item_type = [
    ("URLS", _("链接")),
    ("ARTICLES", _("文章"))
]
