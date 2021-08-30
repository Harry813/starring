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

# Translators: 用户模组{联系电话}
user_tele_text = _("电话号码")

# Translators: 用户模组{联系电话}-错误文本@无效
user_tele_err_invalid = _("电话格式错误")

# Translators: 用户模组{真实姓名}
user_name_text = _('真实姓名')

# Translators: 用户模组{头像}
user_avatar_text = _('头像')

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

# Translators: 文章模组{Meta描述}
article_meta_description_text = _("META标签-描述")

# Translators: 文章模组{Meta描述}@帮助文本
article_meta_description_help_text = _("本标签将不在页面中显示。上限300字符")

# Translators: 文章模组{Meta关键词}
article_meta_keyword_text = _("META标签-关键词")

# Translators: 文章模组{Meta关键词}@帮助文本
article_meta_keyword_help_text = _("本标签将不在页面中显示，关键字之间请使用逗号分割。上限150字符")

# Translators: 文章模组{文章主体}
article_meta_content_text = _("文章主体")

# Translators: 文章模组{创建时间}
article_create_date_text = _("创建时间")

# Translators: 文章模组{最后修改}
article_last_change_text = _("最后修改")


###################################################################################################
# admin.forms.AdminLoginForm  后台登录表单
###################################################################################################

# Translators: 后台登录表单{用户名}
# _("用户名")


###################################################################################################
# Validation Errors  验证错误
###################################################################################################

# Translators: 验证错误{用户相关}-无后台权限/非员工
UserNoPermit_text = _("用户没有相关权限")

# Translators: 验证错误{用户相关}-用户不存在/用户名错误
UserNotExist_text = _("用户不存在")

