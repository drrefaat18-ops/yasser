# 🚀 دليل بدء سشن تقييم الكتاب مع كلود (Claude Evaluation Guide)

هذا الدليل يوضح لك كيفية تشغيل جلسة تقييم أكاديمية وسريرية شاملة لكتاب:
**"ARTIFICIAL INTELLIGENCE IN MEDICINE"** للمؤلفة: **أ.د. شيرين السيد الخولي**
باستخدام **Claude Code** أو **Claude Desktop / Web**.

---

## 📌 1. كيف تبدأ سشن Claude Code في هذا المجلد؟

افتح موجه الأوامر (PowerShell أو Terminal) في مجلد المشروع `D:\yasser`، ثم اكتب:

```powershell
cd D:\yasser
claude
```

بمجرد تشغيل `claude`، سيقرأ كلود تلقائياً ملف `CLAUDE.md` الذي يحتوي على سياق الكتاب بالكامل ومعايير التقييم وأسماء الفصول ومسارات الصور!

---

## 💬 2. برومبتات جاهزة للبدء (انسخ والصق مباشرة في كلود)

### 🔹 الخيار الأول: التقييم الشامل العام للكتاب (Comprehensive Peer-Review)
انسخ هذا البرومبت في سشن كلود للحصول على تقرير تقييم تنفيذي شامل وفق المحاور الستة:

```text
أنت الآن في دور Senior Medical AI Peer Reviewer. 
قم بقراءة ملف الكتاب بالكامل `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md` مع الرجوع لمعايير `EVALUATION_RUBRIC.md`.
أريد تقريراً أكاديمياً وسريرياً شاملاً يتضمن:
1. تقييم تنفيذي عام لمستوى الكتاب وملاءمته لطلاب الطب والأطباء المقيمين.
2. تقييم تفصيلي وفق المحاور الستة (الدقة الطبية، الدقة الخوارزمية، الجودة التعليمية، بنك الأسئلة، الجوانب القانونية والأخلاقية، وحداثة المراجع).
3. جدول الدرجات الكمي من 100 مع توضيح نقاط القوة وأهم الثغرات (Gaps).
4. قائمة بأهم 5 موضوعات طبية/ذكاء اصطناعي حديثة ينصح بإضافتها في الطبعة القادمة.
```

---

### 🔹 الخيار الثاني: المراجعة المتعمقة فصلاً بفصل (Chapter-by-Chapter Deep Dive)
وهو الخيار الأكثر دقة وأكاديمية لمراجعة الكتاب صفحة بصفحة. ابدأ بكل فصل على حدة:

#### لمراجعة الفصل الأول (الأساسيات):
```text
راجع الفصل الأول (# Chapter 1: Fundamentals of Artificial Intelligence in Healthcare) في ملف `AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md`.
قدم تقريراً نقدياً يوضح:
- مدى دقة تعريفات الذكاء الاصطناعي والتعلم العميق والنماذج التوليدية.
- وضوح الفروق بين الأنظمة التقليدية المبنية على القواعد وأنظمة تعلم الآلة.
- أي أخطاء علمية أو صياغات غير دقيقة مع تقديم النص البديل المقترح.
```

#### لمراجعة الفصل الثاني (الأشعة التشخيصية والـ MRI Fast Imaging):
```text
قم بمراجعة الفصل الثاني (# Chapter 2: AI in Diagnostic Radiology & Medical Imaging).
ركز بشكل خاص على:
- دقة شرح فيزياء الـ MRI و k-space undersampling.
- تصنيف خوارزميات الـ CADe مقابل الـ CADx ومسار الفرز (Triage).
- تقييم بنك الأسئلة الخاص بالأشعة (Self-Assessment Quiz).
- تدقيق المخططات والصور التوضيحية ومطابقتها للمحتوى.
```

#### لمراجعة الفصل الثالث (علم الأمراض والمختبرات):
```text
راجع الفصل الثالث (# Chapter 3: AI in Clinical Pathology & Automated Laboratory Diagnostics).
افحص دقة:
- معايير HIL indices وفحوصات الـ Delta Checks في مسارات التشغيل الآلي للمختبرات.
- معالجة Whole Slide Imaging (WSI) وتصنيف Gleason grading لسرطان البروستاتا.
- فحص أسئلة الاختيار من متعدد الـ 18 وصحة الإجابات النموذجية.
```

#### لمراجعة الفصل الرابع (الجراحة والروبوتات الجراحية):
```text
راجع الفصل الرابع (# Chapter 4: AI in Surgery & Surgical Robotics).
افحص دقة:
- درجات الاستقلالية الجراحية (Levels of Autonomy).
- حواجز الأمان الافتراضية (Haptic Virtual Fixtures).
- تقنيات الـ Computer Vision في تحديد الـ Critical View of Safety أثناء استئصال المرارة بالمنظار.
- بنك الأسئلة الخاص بالجراحة.
```

#### لمراجعة الفصل الخامس (القسطرة التداخلية والقلب):
```text
راجع الفصل الخامس (# Chapter 5: AI in Interventional Medicine & Cardiology).
افحص دقة:
- تطبيقات IVUS و OCT وحسابات الـ FFR-CT غير التداخلية.
- تخطيط صمامات TAVR و LAA Occlusion.
- السكتة الدماغية الإقفارية الحادة وتحليلات CT Perfusion.
- بنك الأسئلة التقييمي للفصل الخامس.
```

#### لمراجعة الفصل السادس (التخصصات السريرية: الجلدية، الأورام، الباطنة):
```text
راجع الفصل السادس (# Chapter 6: AI Applications Across Clinical Medical Specialties).
افحص دقة:
- تصنيف الآفات الجلدية وتحديات Fitzpatrick skin types.
- تكامل البيانات متعددة الأوميكس (Multi-Omics) في علاج الأورام الدقيق.
- أنظمة الأنسولين ذات الحلقة المغلقة (Closed-Loop) وتطبيقات الـ Oculomics لشبكية العين.
- بنك الأسئلة التقييمي للفصل السادس.
```

#### لمراجعة الفصل السابع (الأخلاقيات والمسؤولية القانونية ومستقبل الذكاء الاصطناعي):
```text
راجع الفصل السابع (# Chapter 7: Ethics, Medicolegal Challenges & Future Horizons).
افحص دقة:
- الأركان الأربعة للمسؤولية القانونية الطبية (Duty, Breach, Causation, Damages).
- تطبيق عقيدة "Learned Intermediary" ومسارات ترخيص FDA SaMD وخطة PCCP للنماذج التكيفية.
- الفروق بين تشريعات الخصوصية (HIPAA Safe Harbor vs. GDPR).
- جدول مصفوفة المخاطر الطبية القانونية وبنك الأسئلة الشامل (25 سؤالاً).
```

---

### 🔹 الخيار الثالث: تدقيق بنوك الأسئلة وجودتها السيكومترية (MCQ Audit)
```text
قم بمراجعة جميع بنوك الأسئلة في الكتاب (Chapters 2, 3, 4, 5, 6, 7).
أريد تدقيقاً سيكومترياً وعلمياً:
1. هل هناك أي سؤال يحتوي على أكثر من إجابة صحيحة أو إجابة خاطئة علمياً؟
2. هل المشتتات (Distractors) منطقية ومبنية على أخطاء سريرية شائعة؟
3. هل التفسيرات (Explanations) كافية وتعلّم الطالب لماذا هذا الخيار صحيح ولماذا البقية خاطئة؟
```

---

### 🔹 الخيار الرابع: استدعاء الوكلاء التخصصيين (Sub-agents) في سشن كلود
إذا أردت الاستفادة من البروفايلات الأكاديمية الموجودة في مجلد `.claude/agents/`:

- **لاستدعاء خبير المراجعة السريرية للذكاء الاصطناعي:**
  > "Use the `medical-ai-reviewer` persona to evaluate Chapter 2 and Chapter 5."
- **لاستدعاء خبير الإحصاء الحيوي ومقاييس النماذج:**
  > "Use the `academic-statistician` persona to audit all validation metrics (AUROC, Dice, sensitivity/specificity, p-values) reported in the textbook."
- **لاستدعاء خبير فحص المراجع والتحقق من الأدلة:**
  > "Use the `research-synthesist` persona to audit the references list and fact-check landmark clinical trial citations in the book."

---

## 📂 ملفات المشروع المتاحة للرجوع إليها:
- 📖 [AI_in_Medicine- Assistant Prof Dr Shereen Elkholy.md](file:///D:/yasser/AI_in_Medicine-%20Assistant%20Prof%20Dr%20Shereen%20Elkholy.md)
- 📊 [EVALUATION_RUBRIC.md](file:///D:/yasser/EVALUATION_RUBRIC.md)
- ⚙️ [CLAUDE.md](file:///D:/yasser/CLAUDE.md)
- 🧑‍⚕️ [medical-ai-reviewer.md](file:///D:/yasser/.claude/agents/medical-ai-reviewer.md)
