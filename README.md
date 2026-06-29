# 📊 مصاريفي - Masarify

**تطبيق أندرويد احترافي لإدارة الميزانية بقاعدة 50/20/30**

---

## 📱 مميزات التطبيق

| الميزة | الوصف |
|:------|:------|
| 🏠 **الرئيسية** | لوحة تحكم تعرض الدخل الشهري ونسب الصرف لكل فئة |
| ➕ **إضافة معاملة** | تسجيل مصروفات أو دخل مع تصنيفها |
| 📋 **السجل** | عرض جميع المعاملات مع إجمالي المصروف والدخل |
| ⚙️ **الإعدادات** | تحديد الدخل الشهري، إعادة تعيين البيانات |
| 🎨 **واجهة عصرية** | تصميم Material Design باللون الداكن |
| 🌙 **دعم كامل للعربية** | واجهة 100% بالعربية، خط احترافي |

## 🎯 قاعدة 50/20/30

| الفئة | النسبة | اللون | أمثلة |
|:-----|:-----:|:-----:|:------|
| 🏠 **الاحتياجات** | 50% | 🔵 | إيجار، فواتير، طعام، مواصلات |
| 💰 **الادخار** | 20% | 🟢 | استثمار، صندوق طوارئ، تقاعد |
| 🎮 **الرغبات** | 30% | 🟠 | ترفيه، سفر، تسوق، مطاعم |

---

## 🚀 كيفية بناء APK

### 🌐 الطريقة 1: GitHub Actions (موصى به)

1. أنشئ مستودع على GitHub
2. ارفع المجلد `masarify/` للمستودع
3. اذهب إلى **Actions** ⟵ اختر **بناء APK - مصاريفي**
4. اضغط **Run workflow**
5. بعد ~30 دقيقة، حمل الـ APK من **Artifacts**

### 💻 الطريقة 2: Buildozer محلياً (Linux)

```bash
# متطلبات
sudo apt install -y git zip unzip python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev openjdk-17-jdk
pip3 install --user buildozer cython pillow

# بناء
cd masarify
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
python3 -m buildozer android debug

# الـ APK في:
ls -la masarify/bin/*.apk
```

### 🌍 الطريقة 3: Google Colab

افتح [هذا الرابط](https://colab.research.google.com/) وأنشئ نوت بوك جديد، ثم شغّل:

```python
!git clone https://github.com/YOUR_USERNAME/masarify.git
%cd masarify
!pip install buildozer cython pillow
!sudo apt install -y zlib1g-dev libncurses5-dev
!buildozer android debug
```

---

## 📁 هيكل المشروع

```
masarify/
├── .github/workflows/build-apk.yml    # GitHub Actions
├── main.py                            # كود التطبيق الأساسي
├── masarify.kv                        # واجهة المستخدم (KV)
├── buildozer.spec                     # إعدادات Buildozer
├── Masarify_icon.png                  # أيقونة التطبيق
└── fonts/
    └── NotoNaskhArabic-Regular.ttf    # الخط العربي
```

---

## 🛠️ التقنيات المستخدمة

- **Python 3** + **Kivy 2.3.1** — إطار العمل
- **KivyMD 1.2.0** — واجهة Material Design
- **JSON** — تخزين البيانات محلياً
- **Buildozer** — تحويل التطبيق إلى APK

---

## 📜 الترخيص

MIT License - استخدم كما تشاء ✅
