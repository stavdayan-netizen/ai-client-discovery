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
שם העסק: חנות דוגמה דלתא (דמו)

[q_01] מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
תשובה: אנחנו עסק חדש וצריכים לענות על שאלות על משלוחים והחזרות בלי להעסיק נציג.

[q_02] מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
תשובה: חיסכון בעלות כוח אדם ומענה זמין גם בערבים.

[q_03] כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?
תשובה: שיפור שביעות רצון הלקוחות.

[q_04] תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
תשובה: אין תהליך קיים. הבעלים עונה בעצמו כשיש לו זמן.

[q_05] מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום?
תשובה: שם: בעלת החנות לדוגמה; תפקיד: בעלים; אחריות: כל ההחלטות והמענה

[q_06] מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות)
תשובה: שם: בעלת החנות לדוגמה; תפקיד: בעלים

[q_07] מי יהיו משתמשי הקצה של המערכת?
תשובה: לקוחות החנות.

[q_08] היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
תשובה: יש רק דף שאלות נפוצות קצר באתר.

[q_09] האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
תשובה: לא רלוונטי.

[q_10] מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
תשובה: לא רלוונטי, אין מידע קיים.

[q_11] לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?
תשובה: לא רלוונטי, אין מערכות קיימות להתממשק אליהן.

[q_12] כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
תשובה: בוט באתר החנות.

[q_13] באיזו שפה או שפות נדרשת המערכת לתמוך?
תשובה: עברית

[q_14] האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
תשובה: רק שמות וכתובות למשלוח.

[q_15] מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
תשובה: נראה לי שזה בסדר שיהיו טעויות קטנות.

[q_16] האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?
תשובה: כן, החזרים כספיים יאושרו על ידי בעלת החנות.

[q_17] האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית?
תשובה: 2027-02-01

[q_18] האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?
תשובה: תקציב הקמה של עד 10,000 ש"ח ועלות חודשית של עד 500 ש"ח.
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{"follow_up_questions": [{"text": "אם כבר יש לכם מושג, איך תרצו לבדוק ששביעות רצון הלקוחות באמת השתפרה? למשל לפי ציון בסקר קצר, מספר פניות שנענו או זמן המתנה למענה.", "rationale": "מדד ההצלחה שנמסר (שיפור שביעות רצון) כללי ואינו ניתן למדידה. הוא חשוב להגדרת היקף הפרויקט ולהערכת תוצאותיו.", "source_question_ids": ["q_03", "q_02"]}, {"text": "אם כבר מוגדרת אצלכם מדיניות משלוחים והחזרות (זמנים, תנאים, עלויות), נשמח לדעת איפה היא כתובה ואם היא כוללת יותר ממה שמופיע בדף השאלות הנפוצות.", "rationale": "מקור הידע היחיד הוא דף שאלות נפוצות קצר, ואין מידע על מדיניות מסודרת. הבוט יצטרך בסיס ידע מוגדר כדי לענות נכון.", "source_question_ids": ["q_08", "q_01", "q_10"]}, {"text": "אם חשבתם על זה כבר, מה הייתם רוצים שיקרה כשהבוט לא יודע לענות או כשלקוח מבקש החזר כספי? למשל איך בעלת החנות תקבל את הפנייה ובאיזה זמן.", "rationale": "החזרים כספיים מאושרים על ידי בעלת החנות, אבל לא ברור מנגנון ההעברה. זה משפיע על התכנון, ובעלת החנות היא גם הבעלים היחיד שנכנס לתהליך.", "source_question_ids": ["q_16", "q_05", "q_04"]}, {"text": "אם כבר יש לכם תמונה על זה, האם הבוט אמור גם לתת מידע על הזמנה מסוימת של לקוח (כמו סטטוס משלוח), או רק תשובות כלליות על משלוחים והחזרות? ואם כן, מאיפה יגיע המידע על ההזמנות?", "rationale": "צוין שהמערכת תיחשף לשמות וכתובות למשלוח, אך לא ברור אם יש גישה להזמנות ומאיפה. התשובה משפיעה על דרישות הפרטיות והאינטגרציה, כי נכתב שאין מערכות קיימות.", "source_question_ids": ["q_14", "q_11", "q_01"]}]}
--- END OF SYSTEM OUTPUT ---
