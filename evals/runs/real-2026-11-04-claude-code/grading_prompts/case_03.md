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
שם העסק: סטודיו דוגמה גמא (דמו)

[q_01] מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
תשובה: הלקוחות פונים אלינו בשאלות על קורסים ואנחנו עונים ידנית, עם עיכובים של יום או יומיים.

[q_02] מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
תשובה: מענה מהיר יותר ופחות עבודה ידנית בתחילת כל חודש.

[q_03] כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?
תשובה: זמן מענה של עד שעתיים ביום עבודה, ופחות פניות שנשארות ללא מענה.

[q_04] תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
תשובה: מזכירה עוברת על תיבת הדוא"ל ועל ההודעות בפייסבוק ועונה אחת-אחת.

[q_05] מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום?
תשובה: שם: מזכירה לדוגמה; תפקיד: מזכירה; אחריות: מענה לפניות
שם: מנהלת סטודיו לדוגמה; תפקיד: מנהלת הסטודיו; אחריות: אישור תשובות חריגות

[q_06] מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות)
תשובה: [סומן על ידי הלקוח: לא ידוע / טרם הוחלט]

[q_07] מי יהיו משתמשי הקצה של המערכת?
תשובה: המזכירה, ובהמשך אולי גם הלקוחות.

[q_08] היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
תשובה: לא יודע איפה בדיוק נמצא המידע. צריך לבדוק עם מי שמנהל את זה.

[q_09] האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
תשובה: לא בטוח.

[q_10] מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
תשובה: לא יודע, לא בדקנו.

[q_11] לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?
תשובה: יש לנו מערכת רישום לקורסים. לא יודעים אם אפשר להתחבר אליה.

[q_12] כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
תשובה: אולי צ'אט באתר. טרם הוחלט.

[q_13] באיזו שפה או שפות נדרשת המערכת לתמוך?
תשובה: עברית

[q_14] האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
תשובה: לא יודעים אם יש מידע רגיש.

[q_15] מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
תשובה: סובלנות בינונית, תלוי בנושא.

[q_16] האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?
תשובה: נראה לי שכן אבל לא סגרנו.

[q_17] האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית?
תשובה: [סומן על ידי הלקוח: לא ידוע / טרם הוחלט]

[q_18] האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?
תשובה: טרם הוחלט.
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{"follow_up_questions": [
  {"text": "אם כבר יש לכם מידע על מערכת רישום הקורסים (איזו מערכת זו, ואם יש בה אפשרות חיבור או ייצוא נתונים), נשמח לדעת. אם לא, גם פרט קטן כמו שם המערכת יעזור.", "rationale": "הלקוח לא יודע אם אפשר להתחבר למערכת הרישום; זה קריטי לאפשרות לתת מענה מדויק על קורסים ולאומדן היקף ההטמעה.", "source_question_ids": ["q_11"]},
  {"text": "אם אפשר, נשמח לדעת מי אצלכם מנהל או מתחזק את המידע על הקורסים (באתר, במסמכים או במערכת), ואם אפשר לשתף אותו בשיחה.", "rationale": "הלקוח לא יודע היכן המידע, מה מבנהו ואיכותו; צריך איש קשר שיכול לענות על כך.", "source_question_ids": ["q_08", "q_09", "q_10"]},
  {"text": "אם כבר יש לכם תחושה, האם בפניות מגיעים פרטים אישיים של לקוחות (כמו שם, טלפון או פרטי הרשמה) או פרטי תשלום? ואם יש דרישות או הנחיות לגבי הטיפול בהם, נשמח לשמוע.", "rationale": "לא ידוע אם יש מידע רגיש; הפניות מגיעות במייל ובפייסבוק ועשויות לכלול פרטים אישיים, וזה משפיע על הארכיטקטורה והאבטחה.", "source_question_ids": ["q_14", "q_04"]},
  {"text": "אם כבר יש לכם מחשבה על כך, מי אצלכם יהיה האדם שמלווה את הפרויקט ומקבל החלטות (למשל מנהלת הסטודיו)? ואם אין עדיין, אפשר גם להגיע לשיחה עם הצעה ראשונית.", "rationale": "ספונסר הפרויקט לא ידוע; בלעדיו קשה לקבל החלטות על היקף, אישורים ותקציב.", "source_question_ids": ["q_06", "q_05"]},
  {"text": "אם יש לכם כבר רעיון, האם תרצו שהמזכירה תאשר את תשובות ה-AI לפני שליחה, או שחלק מהן יישלחו ישירות ללקוחות? ואילו סוגי פניות לדעתכם תמיד צריכים אישור אנושי?", "rationale": "אישור אנושי נראה רצוי אך לא הוחלט, וכן ידוע שתשובות חריגות מאושרות על ידי מנהלת הסטודיו; ההחלטה קובעת את מידת האוטומציה והסיכון.", "source_question_ids": ["q_16", "q_15", "q_05"]}
]}
--- END OF SYSTEM OUTPUT ---
