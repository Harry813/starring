from django.utils.translation import gettext as _
from django.utils.translation import pgettext as _p
from django.utils.translation import ngettext as _n


###################################################################################################
# overall  全局设定
###################################################################################################

# Translators: 全局设定{品名}
brand_name = _('星环')


###################################################################################################
# staring.models.User  用户模组
###################################################################################################

# Translators: 用户模组{用户ID}
user_uid_text = _('用户ID')

# Translators: 用户模组{用户名}
user_username_text = _('用户名')

# Translators: 用户模组{用户名}-帮助文本
user_username_help_text = _('8-150字符，仅可包含大小写字母、数字以及@/./+/-/_')

# Translators: 用户模组{用户名}-错误文本@唯一性
user_username_err_unique = _("用户名已存在")

# Translators: 用户模组{用户名}-错误文本@无效
user_username_err_invalid = _("无效的用户名")

# Translators: 用户模组{用户名}-错误文本@过长
user_username_err_max = _("用户名长度不得超过150字符")

# Translators: 用户模组{用户名}-错误文本@过短
user_username_err_min = _("用户名长度不得少于8字符")

# Translators: 用户模组{密码}
user_password_text = _('密码')

# Translators: 用户模组{密码}-帮助文本
user_password_help_text = _('8-128个字符，至少包含1个数字、1个字母')

# Translators: 用户模组{密码}-错误文本@无效
user_password_err_invalid = _("密码格式错误，请包含8-128个字符，至少包含1个数字、1个字母")

# Translators: 用户模组{密码}-错误文本@过长
user_password_err_max_length = _("密码格式错误，至多包含128个字符")

# Translators: 用户模组{密码}-错误文本@过短
user_password_err_min_length = _("密码格式错误，至少包含8个字符")

# Translators: 用户模组{请再次确认密码}
user_confirm_text = _("请再次确认密码")

# Translators: 用户模组{联系电话}
user_tele_text = _("电话号码")

# Translators: 用户模组{联系电话}-错误文本@无效
user_tele_err_invalid = _("电话格式错误")

# Translators: 用户模组{真实姓名}
user_name_text = _('真实姓名')

# Translators: 用户模组{头像}
user_avatar_text = _('头像')

# Translators: 用户模组{头像}-帮助文本
user_avatar_help_text = _('')

# Translators: 用户模组{生日}
user_dob_text = _('生日')

# Translators: 用户模组{邮箱地址}
user_email_text = _('邮箱地址')

# Translators: 用户模组{冠码}
user_countryCode_text = _("冠码")

# Translators: 用户模组{活跃状态}
user_active_text = _('活跃状态')

# Translators: 用户模组{活跃状态}-帮助文本
user_active_help_text = _('指定是否应将此用户视为活动用户，请取消选择此项代替删除帐户。')

# Translators: 用户模组{注册日期}
user_date_join_text = _('注册日期')

# Translators: 用户模组{最后更改}
user_last_change_text = _("最后修改")


###################################################################################################
# admin.forms.CustomerSearch  用户搜索表单
###################################################################################################

# Translator:　用户搜索表单{标签搜索}
user_search_tag_text = _("标签筛选")

# Translator:　用户搜索表单{等级筛选}
user_search_vip_text = _("等级筛选")

# Translator:　用户搜索表单{搜索模式}
user_search_type_text = _("搜索模式")

# Translator:　用户搜索表单{精确搜索}
user_search_detail_text = _("精确搜索")

# Translator:　用户搜索表单{错误信息}-条件不足
user_search_errmsg_InsuffCond = _("搜索条件不足，请选择搜索类型或填写搜索内容")

###################################################################################################
# staring.models.Article  文章模组
###################################################################################################

# Translators: 文章模组{状态}
article_status_text = _("文章状态")

# Translators: 文章模组{标题}
article_title_text = _("标题")

# Translators: 文章模组{用户}
article_author_text = _("作者")

# Translators: 文章模组{用户等级}
article_lv_require_text = _("需求用户等级")

# Translators: 文章模组{文章可复制}
article_copyable_text = _("文章可复制")

# Translators: 文章模组{文章可复制}-帮助文本
article_copyable_help_text = _("勾选后，用户可选择、复制文章内容")

# Translators: 文章模组{Meta描述}
article_meta_description_text = _("META标签-描述")

# Translators: 文章模组{Meta描述}-帮助文本
article_meta_description_help_text = _("本标签将不在页面中显示。上限300字符")

# Translators: 文章模组{Meta关键词}
article_meta_keyword_text = _("META标签-关键词")

# Translators: 文章模组{Meta关键词}-帮助文本
article_meta_keyword_help_text = _("本标签将不在页面中显示，关键字之间请使用逗号分割。上限150字符")

# Translators: 文章模组{文章主体}
article_meta_content_text = _("文章主体")

# Translators: 文章模组{创建时间}
article_create_date_text = _("创建时间")

# Translators: 文章模组{最后修改}
article_last_change_text = _("最后修改")


###################################################################################################
# admin.models.Department  部门模组
###################################################################################################

# Translators: 部门模组{部门名称}
department_dep_name_text = _("部门名称")


###################################################################################################
# admin.models.Staff  员工模组
###################################################################################################

# Translators: 员工模组{员工ID}
staff_id_text = _("员工ID")

# Translators: 员工模组{部门}
staff_department_text = _("部门")

# Translators: 员工模组{职位}
staff_role_text = _("职位")

# Translators: 员工模组{标签}
staff_tag_text = _("标签")

###################################################################################################
# customer.models.Customer  用户信息翻译
###################################################################################################

# Translators: 用户信息{联系方式}
customer_contact_type_text = _("联系方式")

# Translators: 用户信息{联系号码}
customer_contact_detail_text = _("联系号码")

# Translators: 用户信息{国籍}
customer_nationality_text = _("国籍")

# Translators: 用户信息{意向项目}
customer_intention_text = _("意向项目")

# Translators: 用户信息{附加内容}
customer_extra_text = _("附加内容")

# Translators: 用户信息{用户等级}
customer_vip_lv_text = _("用户等级")

# Translators: 用户信息{用户标签}
customer_tag_text = _("用户标签")


###################################################################################################
# customer.models.Consult  咨询表单翻译
###################################################################################################

# Translators: 咨询表单{姓名}
consult_name_text = _("姓名 | Name")

# Translators: 咨询表单{姓名}-占位符
consult_name_placeholder = _("您的全名")

# Translators: 咨询表单{姓名}-错误文本@required
consult_name_err_required = _("请填写您的姓名")

# Translators: 咨询表单{姓名}-错误文本@min_length
consult_name_err_min_length = _("至少2字符")

# Translators: 咨询表单{姓名}-错误文本@max_length
consult_name_err_max_length = _("至多150字符")

# Translators: 咨询表单{邮箱}
consult_email_text = _("电子邮箱 | Email")

# Translators: 咨询表单{邮箱}-占位符
consult_email_placeholder = _("您的电子邮箱")

# Translators: 咨询表单{邮箱}-错误文本@required
consult_email_err_required = _("您的电子邮箱")

# Translators: 咨询表单{邮箱}-错误文本@invalid
consult_email_err_invalid = _("邮箱格式有误")

# Translators: 咨询表单{邮箱}-错误文本@required
consult_email_err_max_length = _("至多254字符")

# Translators: 咨询表单{联系方式}
consult_contact_text = _("联系方式 | Contact Details")

# Translators: 咨询表单{联系方式}-占位符
consult_contact_placeholder = _("您的联系方式")

# Translators: 咨询表单{联系方式}-错误文本@required
consult_contact_err_required = _("请填写您的联系方式")

# Translators: 咨询表单{联系方式}-错误文本@max_length
consult_contact_err_max_length = _("请填写您的联系方式")

# Translators: 咨询表单{问题}
consult_query_text = _("简述问题 | Brief your questions")

# Translators: 咨询表单{问题}-占位符
consult_query_placeholder = _("请留下你的问题，我们将尽快联系你")

# Translators: 咨询表单{问题}-错误文本@required
consult_query_err_required = _("请留下你的问题")

# Translators: 咨询表单{咨询状态}
consult_status_text = _("咨询状态")

# Translators: 咨询表单{创建时间}
consult_create_date_text = _("创建时间")


###################################################################################################
# staring.models.Carousels  首页轮播模组翻译
###################################################################################################

# Translators: 首页轮播{名称}
carousels_name_text = _("轮播名称")

# Translators: 首页轮播{长度}
carousels_length_text = _("轮播最大长度")


###################################################################################################
# staring.models.CarouselArticles  轮播文章模组翻译
###################################################################################################

# Translators: 首页轮播{名称}
carouselArticle_carousel_text = _("轮播模块")

# Translators: 首页轮播{文章}
carouselArticle_article_text = _("轮播文章")

# Translators: 首页轮播{标题}
carouselArticle_title_text = _("标题")

# Translators: 首页轮播{简介}
carouselArticle_intro_text = _("简介")


###################################################################################################
# staring.models.MeetingSlot  预约时间表模组
###################################################################################################

# Translators: 预约时间表{日期}
meetingSlot_date_text = _("日期")

# Translators: 预约时间表{时间}
meetingSlot_time_text = _("时间")

# Translators: 预约时间表{可用次数}
meetingSlot_availability_text = _("可用次数")


###################################################################################################
# staring.models.MeetingReservation  预约模组
###################################################################################################

# Translators: 预约{客户}
meetingReservation_customer_text = _("客户")

# Translators: 预约{咨询师}
meetingReservation_staff_text = _("咨询师")

# Translators: 预约{预约时间}
meetingReservation_slot_text = _("预约时间")

# Translators: 预约{预约状态}
meetingReservation_status_text = _("预约状态")

###################################################################################################
# Validation Errors  验证错误
###################################################################################################

# Translators: 验证错误{用户相关}-无后台权限/非员工
UserNoPermit_text = _("用户没有相关权限")

# Translators: 验证错误{用户相关}-用户不存在/用户名错误
UserNotExist_text = _("用户不存在")

paswd_errmsg_NOT_match = _("两次输入的密码不同")
