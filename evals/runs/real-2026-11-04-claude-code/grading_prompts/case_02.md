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
שם העסק: מסעדת דוגמה בטא (דמו)

[q_01] מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
תשובה: העסק עמוס ואנחנו לא מספיקים לענות לכולם.

[q_02] מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
תשובה: שיהיה יותר טוב ושיעבוד יותר מהר.

[q_03] כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?
תשובה: שנצמח ושהלקוחות יהיו מרוצים.

[q_04] תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
תשובה: הכול ידני, מי שפנוי עונה.

[q_05] מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום?
תשובה: שם: בעל המסעדה לדוגמה; תפקיד: בעלים; אחריות: מקבל ההחלטות
שם: מנהלת משמרת לדוגמה; תפקיד: מנהלת משמרת; אחריות: מענה להזמנות

[q_06] מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות)
תשובה: שם: בעל המסעדה לדוגמה; תפקיד: בעלים

[q_07] מי יהיו משתמשי הקצה של המערכת?
תשובה: הצוות שלנו ואולי גם הלקוחות.

[q_08] היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
תשובה: בראש של העובדים ובכמה קבצים.

[q_09] האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
תשובה: מעורב.

[q_10] מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
תשובה: בסדר בערך.

[q_11] לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?
תשובה: יש לנו קופה רושמת. לא יודע אם יש לה API.

[q_12] כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
תשובה: וואטסאפ.

[q_13] באיזו שפה או שפות נדרשת המערכת לתמוך?
תשובה: עברית

[q_14] האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
תשובה: לא ממש. רק שמות וטלפונים של לקוחות להזמנות.

[q_15] מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
תשובה: לא נעים כשיש טעויות אבל לא נורא.

[q_16] האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?
תשובה: כן, אנחנו רוצים לאשר הזמנות.

[q_17] האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית?
תשובה: 2027-01-15

[q_18] האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?
תשובה: עדיין לא דיברנו על תקציב.
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{"follow_up_questions": [{"text": "אם כבר יש לכם מושג, מה היינו רוצים לראות משתפר בפועל? למשל כמה פניות או הזמנות מגיעות ביום, כמה זמן לוקח לענות היום, או מה היה נחשב מבחינתכם שיפור ברור.", "rationale": "ה-KPIs (q_03) וההשפעה העסקית (q_02) כלליים מאוד (\"שנצמח\", \"יותר טוב\") וללא מדד מדיד, וקשה להגדיר הצלחה בלעדיהם.", "source_question_ids": ["q_02", "q_03"]}, {"text": "אם אפשר, ספרו לנו קצת יותר על מה שקורה היום כשפונים אליכם: באילו ערוצים הפניות מגיעות (וואטסאפ, טלפון, אתר), ואילו סוגי שאלות או בקשות חוזרים הכי הרבה.", "rationale": "הכאב (q_01) והתהליך הידני (q_04) מתוארים באופן כללי; לא ברור מה סוגי הפניות, הערוצים והנפח, וזה קריטי להגדרת היקף הפתרון.", "source_question_ids": ["q_01", "q_04", "q_12"]}, {"text": "אם כבר יש לכם מידע על הקופה הרושמת, נשמח לדעת איזו מערכת זו ומי מטפל בה (למשל הספק), ומה הייתם רוצים שהפתרון יעשה מולה, אם בכלל.", "rationale": "לא ידוע אם לקופה יש API (q_11), וזה משפיע על היתכנות האינטגרציה ועל אישור והזנת הזמנות.", "source_question_ids": ["q_11", "q_16"]}, {"text": "אם כבר חשבתם על זה, מי בדיוק יאשר הזמנות לפני ביצוע סופי ובאילו מקרים (כל הזמנה, או רק חריגות), ומי יהיה הפונה ללקוחות: רק הצוות או גם הלקוחות עצמם?", "rationale": "יש דרישת אישור אנושי (q_16) אך לא ברור מי מאשר ובאיזה היקף; משתמשי הקצה (q_07) לא הוכרעו (\"ואולי גם הלקוחות\"), וזה משפיע על תכנון התהליך.", "source_question_ids": ["q_07", "q_16", "q_05"]}, {"text": "אם יש לכם כבר כיוון, האם יש טווח תקציב או מסגרת שחשוב לכם לעמוד בה להקמה ולתחזוקה שוטפת? ואם עוד לא, גם זה בסדר גמור.", "rationale": "התקציב לא נדון עדיין (q_18) ויש תאריך יעד מוגדר (q_17); כיוון תקציבי גס יעזור לכוון את היקף ה-MVP.", "source_question_ids": ["q_18", "q_17"]}]}
--- END OF SYSTEM OUTPUT ---
