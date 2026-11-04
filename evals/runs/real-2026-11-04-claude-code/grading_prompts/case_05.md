You are grading the output of a system that proposes follow-up questions for a discovery call. You
did not produce this output. Grade it strictly against the anchors below, using only the text in
this message. Do not use any tools and do not read any files.

The system was given the client's questionnaire answers (below) and asked to propose 0 to 5
follow-up questions in Hebrew, each with an internal rationale and related questionnaire item ids,
asking only about information that is truly missing, vague or unknown, never asking about topics
the client marked "לא רלוונטי", never asking for secrets or personal data, and never inventing facts.

Score three criteria from 0 to 2 using these anchors:

**Relevance**
- 2: Every question is materially useful for the next discovery call and tied to a real gap, vague answer or important unknown in the client's answers. If there are no questions, nothing important is actually missing.
- 1: A mix of useful and marginal or redundant questions, or one clearly important gap is ignored.
- 0: Mostly irrelevant or redundant questions (for example re-asking something answered adequately), or all important gaps are missed.

**Factual accuracy of the rationale**
- 2: Every statement the rationales make about the client's answers is accurate. No questions counts as 2.
- 1: A minor imprecision or loose paraphrase.
- 0: A rationale misstates or contradicts what the client wrote.

**Avoidance of invented information**
- 2: No question or rationale states or presupposes facts that are not in the answers (budgets, systems, numbers, names, commitments, decisions).
- 1: A mild presupposition that goes beyond the answers.
- 0: Clearly invented facts.

Reply with a single JSON object and nothing else (no code fence), exactly in this shape:

{"relevance": {"score": 0, "justification": "<one or two sentences>"},
 "factual_accuracy": {"score": 0, "justification": "<one or two sentences>"},
 "no_invented_information": {"score": 0, "justification": "<one or two sentences>"}}

Each score must be 0, 1 or 2.

--- CLIENT ANSWERS (data) ---
שם העסק: מרפאת דוגמה אפסילון (דמו)

[q_01] מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
תשובה: קביעת תורים וביטולים בטלפון תופסת את הקבלה רוב היום.

[q_02] מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
תשובה: פחות עומס טלפוני וקיצור זמני ההמתנה בקבלה.

[q_03] כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?
תשובה: ירידה של 40% בשיחות הטלפון לקבלה, ושיעור הגעה של לפחות 90% לתורים שנקבעו.

[q_04] תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
תשובה: הקבלה עונה לטלפון, בודקת ביומן ומתעדת את התור בתיק המטופל במערכת.

[q_05] מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום?
תשובה: שם: מזכירה רפואית לדוגמה; תפקיד: מזכירה; אחריות: קביעת תורים
שם: מנהלת מרפאה לדוגמה; תפקיד: מנהלת; אחריות: פיקוח

[q_06] מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות)
תשובה: שם: מנהלת מרפאה לדוגמה; תפקיד: מנהלת

[q_07] מי יהיו משתמשי הקצה של המערכת?
תשובה: המטופלים והקבלה.

[q_08] היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
תשובה: מערכת ניהול תורים ותיקי מטופלים, ועמוד שאלות נפוצות באתר.

[q_09] האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
תשובה: מעורב: נתוני תורים מובנים והערות רפואיות בטקסט חופשי.

[q_10] מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
תשובה: הנתונים מדויקים ומתעדכנים בזמן אמת.

[q_11] לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?
תשובה: מערכת ניהול התורים הנוכחית. לא יודעים אם יש לה API פתוח.

[q_12] כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
תשובה: הודעות בוואטסאפ ובוט באתר.

[q_13] באיזו שפה או שפות נדרשת המערכת לתמוך?
תשובה: עברית, ערבית ורוסית

[q_14] האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
תשובה: כן. המטופלים מוסרים שם מלא, מספר תעודת זהות, מספר טלפון ופרטים על מצבם הרפואי. עדיין לא בדקנו דרישות פרטיות.

[q_15] מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
תשובה: אפס סובלנות לטעויות בנושאים רפואיים.

[q_16] האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?
תשובה: לא יודעים עדיין אילו פעולות יצריכו אישור אנושי.

[q_17] האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית?
תשובה: 2027-06-01

[q_18] האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?
תשובה: עדיין לא הוגדר תקציב.
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{"follow_up_questions": [{"text": "אם כבר יש לכם מידע על כך, נשמח לדעת אילו דרישות פרטיות ואבטחת מידע חלות עליכם בטיפול בפרטי מטופלים ובמידע רפואי (למשל מול קופות החולים, רגולטור או גורם משפטי), ומי במרפאה אחראי על הנושא.", "rationale": "המערכת תיחשף לפרטים מזהים ולמידע רפואי, והלקוח ציין שעדיין לא בדק דרישות פרטיות. פער מהותי שמשפיע על ארכיטקטורה, בחירת ספקים ותזמון.", "source_question_ids": ["q_14"]}, {"text": "אם כבר יש לכם מחשבה על כך, אילו פעולות לדעתכם אפשר שהבוט יבצע לבד (למשל מענה על שאלות נפוצות, קביעה או ביטול של תור) ואילו פעולות תעדיפו שיעברו לאישור או לטיפול של איש קבלה?", "rationale": "הלקוח לא יודע אילו פעולות דורשות אישור אנושי, ויש אפס סובלנות לטעויות רפואיות. ההגדרה קריטית לתכנון התהליך ולחלוקת העבודה בין הבוט לקבלה.", "source_question_ids": ["q_16", "q_15"]}, {"text": "אם אפשר, נשמח לדעת איזו מערכת ניהול תורים משמשת אתכם היום, ואם יש מישהו (למשל ספק המערכת או גורם טכני אצלכם) שיכול לבדוק אם היא מאפשרת חיבור חיצוני לקריאה וכתיבה של תורים.", "rationale": "הלקוח לא יודע אם למערכת התורים יש API. זו תלות מרכזית לאפשרות קביעת וביטול תורים אוטומטית ולהערכת היקף הפרויקט.", "source_question_ids": ["q_11"]}, {"text": "אם כבר יש לכם נתון על כך, כמה שיחות טלפון בערך מתקבלות בקבלה ביום או בשבוע, ומה שיעור ההגעה לתורים כיום?", "rationale": "יעדי ההצלחה (ירידה של 40% בשיחות, הגעה של 90% לפחות) נקבעו, אך אין נקודת התחלה להשוואה ולכן אי אפשר למדוד שיפור.", "source_question_ids": ["q_03", "q_01"]}, {"text": "אם יש לכם כבר מושג, נשמח לדעת באיזה טווח תקציב או סדר גודל אתם חושבים על הפרויקט, ומה עוד יכול להשפיע על ההחלטה אם לצאת לדרך.", "rationale": "לא הוגדר תקציב להקמה ולתחזוקה, ויש תאריך יעד להשקה. הכוונה היא להבין מגבלות ותהליך קבלת החלטות לפני התכנון.", "source_question_ids": ["q_18", "q_17"]}]}
--- END OF SYSTEM OUTPUT ---
