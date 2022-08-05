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
    ('UNPAID', _("未付款")),
    ('PAID', _("已付款")),
    ('ACCEPT', _("预约成功")),
    ('REJECT', _("预约失败")),
    ('CASH', _("现金付款，待收取")),
    ('SUCCESS', _("此次会议已结束")),
    ('TIMEOUT', _("逾时未参与"))
]

payment_method = [
    ('VISADEB', _("Visa 借记卡")),
    ('VISACRE', _("Visa 信用卡")),
    ('MASTER', _("Master 卡")),
    ('ALIPAY', _("支付宝")),
    ('WECHAT', _("微信")),
    ('PAYPAL', _("Paypal")),
    ('CASH', _("现金"))
]

navi_item_per_col = 10

link_type = [
    ("URL", _("链接")),
    ("ARTICLE", _("文章"))
]

navigator_item_level = [
    (0, _("标题")),
    (1, _("条目"))
]

Slot_interval = +15  # Minute
Slot_start = 9  # 24h Clock
Slot_end = 18  # 24h Clock
Slot_duration = +45  # Minute

title_prefix = [
    ("MR", _("Mr.")),
    ("MRS", _("Mrs.")),
    ("MISS", _("Miss.")),
    ("MS", _("Ms.")),
    ("DR", _("Dr.")),
    ("PROF", _("Prof."))
]

slot_status = [
    ("AVAILABLE", _("可用")),
    ("LOCKED", _("锁定")),
    ("OCCUPIED", _("占用"))
]
