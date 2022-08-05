from django.utils.translation import gettext as _

marriage_status_label = _("1. What is your marriage status?")
marriage_status_text = _("婚姻状况")
marriage_status = [
    (0, _("Never Married / Single")),
    (1, _("Annulled Marriage")),
    (2, _("Common-Law, Married")),
    (3, _("Married")),
    (4, _("Widowed")),
    (5, _("Divorced / Separate")),
    (6, _("Legally Separated")),
]

age_group_label = _("2. Age")
age_group_text = _("年龄")
age_group = [
    (-1, _("17 years of age or less")),
    (0, _("18 years of age")),
    (1, _("19 years of age")),
    (2, _("20 years of age")),
    (3, _("21 years of age")),
    (4, _("22 years of age")),
    (5, _("23 years of age")),
    (6, _("24 years of age")),
    (7, _("25 years of age")),
    (8, _("26 years of age")),
    (9, _("27 years of age")),
    (10, _("28 years of age")),
    (11, _("29 years of age")),
    (12, _("30 years of age")),
    (13, _("31 years of age")),
    (14, _("32 years of age")),
    (15, _("33 years of age")),
    (16, _("34 years of age")),
    (17, _("35 years of age")),
    (18, _("36 years of age")),
    (19, _("37 years of age")),
    (20, _("38 years of age")),
    (21, _("39 years of age")),
    (22, _("40 years of age")),
    (23, _("41 years of age")),
    (24, _("42 years of age")),
    (25, _("43 years of age")),
    (26, _("44 years of age")),
    (27, _("45 years of age or more")),
]
age_group_score = {
    # Without Partner
    0: {-1: -1, 0: 99, 1: 105, 2: 110, 3: 110, 4: 110, 5: 110, 6: 110, 7: 110, 8: 110, 9: 110, 10: 110, 11: 110,
        12: 105, 13: 99, 14: 94, 15: 88, 16: 83, 17: 77, 18: 72, 19: 66, 20: 61, 21: 55, 22: 50, 23: 39, 24: 28, 25: 17,
        26: 6, 27: 0},
    # With Partner
    1: {-1: -1, 0: 90, 1: 95, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 100, 8: 100, 9: 100, 10: 100, 11: 100, 12: 95,
        13: 90, 14: 85, 15: 80, 16: 75, 17: 70, 18: 65, 19: 60, 20: 55, 21: 50, 22: 45, 23: 35, 24: 25, 25: 15, 26: 5,
        27: 0}
}

education_lv_label = _("3. What is your level of education?")
education_lv_text = _("教育水平")
education_lv = [
    (0, _("Less than secondary school (high school)")),
    (1, _("Secondary diploma (high school graduation)")),
    (2, _("One-year degree, diploma or certificate from a university, college, trade or technical school, "
          "or other institute")),
    (3, _("Two-year program at a university, college, trade or technical school, or other institute")),
    (4, _("Bachelor's degree OR a three or more year program at a university, college, trade or technical school, "
          "or other institute")),
    (5, _("Two or more certificates, diplomas, or degrees. One must be for a program of three or more years")),
    (6, _("Master's degree, OR professional degree needed to practice in a licensed profession "
          "(For “professional degree,” the degree program must have been in: "
          "medicine, veterinary medicine, dentistry, optometry, law, chiropractic medicine, or pharmacy.)")),
    (7, _("Doctoral level university degree (Ph.D.)"))
]
education_lv_score = {
    # Without Partner
    0: {0: 0, 1: 30, 2: 90, 3: 98, 4: 120, 5: 128, 6: 135, 7: 150},
    # With Partner
    1: {0: 0, 1: 28, 2: 84, 3: 91, 4: 112, 5: 119, 6: 126, 7: 140},
}

education_canadian_label = _("3. a) Have you earned a Canadian degree?")
education_canadian_text = _("加拿大学位?")

education_canadian_lv_label = _("3. b) Choose the best answer to describe this level of education.")
education_canadian_lv_text = _("加拿大学位")
education_canadian_lv = [
    (_("Secondary"), (
        (0, _("Secondary (High school) or Less")),
    )),
    (_("Post-Secondary"), (
        (1, _("One or Two year diploma or certificate")),
        (2, _("Degree, Diploma, Certificate of three years or longer,or Master degree, professional or doctoral "
              "degree of at least one academic year"))
    ))
]
education_canadian_lv_score = {
    0: 0, 1: 15, 2: 30
}

valid_first_language_test_label = _("4. Do you have a valid language score")
valid_first_language_test_text = _("第一语言测试？")

first_language_test_label = _("4. a) Choose your test type for your first language test")
first_language_test_text = _("第一语言测试")
first_listening_text = _("第一-听力")
first_speaking_text = _("第一-口语")
first_reading_text = _("第一-阅读")
first_writing_text = _("第一-写作")

valid_second_language_test_label = _("5. Do you have another valid language score")
valid_second_language_test_text = _("第二语言测试？")

second_language_test_label = _("5. a) Choose your test type for your second language test")
second_language_test_text = _("第二语言测试")
second_listening_text = _("第二-听力")
second_speaking_text = _("第二-口语")
second_reading_text = _("第二-阅读")
second_writing_text = _("第二-写作")

work_experience_label = _("6. In the last ten years, how many years of skilled work experience in Canada do you have?")
work_experience_text = _("工作经历")

NOC_text = _("NOC等级")
NOC_label = _("7. What is your NOC skil level?")

foreign_work_experience_label = _("8. In the last ten years, how many years of skilled work experience in other "
                                  "countries do you have?")
foreign_work_experience_text = _("国外工作经历")

work_experience = [
    (0, _("No experience or less than a year of experience")),
    (1, _("1 year of experience")),
    (2, _("2 year of experience")),
    (3, _("3 year of experience")),
    (4, _("4 year of experience")),
    (5, _("5 year of experience or more")),
]

work_experience_score = {
    # Without Partner
    0: {0: 0, 1: 40, 2: 53, 3: 64, 4: 72, 5: 80},
    # With Partner
    1: {0: 0, 1: 35, 2: 46, 3: 56, 4: 63, 5: 70},
}

foreign_work_experience = [
    (0, _("No experience or less than a year of experience")),
    (1, _("1 year of experience")),
    (2, _("2 year of experience")),
    (3, _("3 year of experience or more")),
]

partner_education_lv_label = _("1. What is the highest level of education for which your spouse or common-law "
                               "partner's has？")
partner_education_lv_text = _("伴侣教育水平")
partner_education_lv_score = {0: 0, 1: 2, 2: 6, 3: 7, 4: 8, 5: 9, 6: 10, 7: 10}

valid_partner_language_test_label = _("2. Did your spouse or common-law partner have a valid language test score?")
valid_partner_language_test_text = _("伴侣语言测试?")

partner_language_test_label = _("2. a) Which test did your spouse or common-law partner take?")
partner_language_test_text = _("伴侣语言测试")
partner_listening_text = _("伴侣-听力")
partner_speaking_text = _("伴侣-口语")
partner_reading_text = _("伴侣-阅读")
partner_writing_text = _("伴侣-写作")

partner_work_experience_label = _("3. In the last ten years, how many years of skilled work experience in Canada does "
                                  "your spouse/common-law partner have?")
partner_work_experience_text = _("伴侣工作经历")

partner_work_experience_score = {0: 0, 1: 5, 2: 7, 3: 8, 4: 9, 5: 10}

valid_certificate_label = _("1. Do you have a certificate of qualification from a Canadian province, "
                            "territory or federal body?")
valid_certificate_text = _("资格证书")

valid_job_offer_label = _("2. Do you have a valid job offer supported by a Labour Market Impact Assessment "
                          "(if needed)?")
valid_job_offer_text = _("工作机会")

valid_nomination_label = _("3. Do you have a nomination certificate from a province or territory?")
valid_nomination_text = _("提名证书")

valid_relatives_citizen_label = _("4. Do you or your spouse or common law partner ( if they will come with you to "
                                  "Canada) have at least one brother or sister living in Canada who is a citizen or "
                                  "permanent resident?")
valid_relatives_citizen_text = _("亲属身份")

# general
boolean_general = [
    (True, _("Yes")),
    (False, _("No")),
]

language_test = [
    (_("English"), (
        (0, _("CELPIP-G")),
        (1, _("IELTS")),
    )),
    (_("French"), (
        (2, _("TEF Canada")),
        (3, _("TCF Canada")),
    )),
]

listening_label = _("听力")
speaking_label = _("口语")
reading_label = _("阅读")
writing_label = _("写作")
eligible_text = _("合格")

noc = [
    ("00", _("00 - Senior management occupations")),
    ("0", _("0 - Management occupations")),
    ("A", _("A - Occupations usually require university education")),
    ("B", _("B - Occupations usually require college education, specialized training or apprenticeship training")),
    ("C", _("C - Occupations usually require secondary school and/or occupation-specific training")),
    ("D", _("D - On-the-job training is usually provided for occupations")),
]
