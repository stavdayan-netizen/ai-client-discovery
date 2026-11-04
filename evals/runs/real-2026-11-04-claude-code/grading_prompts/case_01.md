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
שם העסק: חברת דוגמה אלפא (דמו)

[q_01] מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
תשובה: אנחנו מקבלים כ-120 פניות ביום בוואטסאפ, רובן שאלות חוזרות על זמני הגעה ומחירון, והצוות מבזבז על כך כשלוש שעות ביום.

[q_02] מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
תשובה: חיסכון של כשעתיים עבודה ביום לכל נציג, וקיצור זמן המענה הראשון מ-40 דקות לפחות מ-5 דקות.

[q_03] כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?
תשובה: זמן מענה ראשון חציוני של עד 5 דקות, ירידה של 30% בפניות שמגיעות לנציג, וציון שביעות רצון של 4.5 מתוך 5 בסקר קצר.

[q_04] תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
תשובה: נציג קורא כל הודעה, מחפש במחירון ובלוח הזמנים המשותף וכותב תשובה ידנית. תשובות מורכבות מועברות למנהל התפעול.

[q_05] מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום?
תשובה: שם: נציגת שירות לדוגמה; תפקיד: נציגת שירות; אחריות: מענה ראשוני בוואטסאפ
שם: מנהל תפעול לדוגמה; תפקיד: מנהל תפעול; אחריות: טיפול בפניות מורכבות ואישור הצעות מחיר

[q_06] מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות)
תשובה: שם: מנהל תפעול לדוגמה; תפקיד: מנהל תפעול

[q_07] מי יהיו משתמשי הקצה של המערכת?
תשובה: נציגי השירות בלבד בשלב הראשון. הלקוחות ינהלו שיחה ישירות רק בשלב מאוחר יותר.

[q_08] היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
תשובה: מחירון בקובץ PDF, שאלות נפוצות במסמך Word, ולוח זמנים בגיליון Google Sheets משותף.

[q_09] האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
תשובה: בעיקר לא מובנה (מסמכים). לוח הזמנים מובנה בגיליון.

[q_10] מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
תשובה: המחירון מתעדכן פעם ברבעון והוא מדויק. מסמך השאלות הנפוצות עודכן לפני חודשיים ויש בו כמה סעיפים ישנים.

[q_11] לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?
תשובה: אין צורך בממשקים בשלב הראשון. נקרא את הגיליון המשותף בקריאה בלבד. אין לנו API פתוח מלבד זה של WhatsApp Business.

[q_12] כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
תשובה: צ'אט בוואטסאפ העסקי הקיים, עם העברה לנציג אנושי בלחיצה אחת.

[q_13] באיזו שפה או שפות נדרשת המערכת לתמוך?
תשובה: עברית ואנגלית

[q_14] האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
תשובה: הלקוחות מוסרים שם וכתובת להזמנת טכנאי. לא נאסף מידע פיננסי או רפואי בשיחה.

[q_15] מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
תשובה: סובלנות נמוכה: תשובה שגויה על מחיר או זמן הגעה אינה מקובלת, ולכן נעדיף להעביר לנציג כשיש ספק.

[q_16] האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?
תשובה: כן. כל הזמנה או שינוי מחיר יאושרו על ידי נציג לפני ביצוע.

[q_17] האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית?
תשובה: 2027-03-01

[q_18] האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?
תשובה: תקציב הקמה של עד 20,000 ש"ח ותחזוקה חודשית של עד 1,500 ש"ח, אושרו על ידי הנהלה.
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{"follow_up_questions": [{"text": "אם כבר יש לכם מידע על כך, אילו מקרים נחשבים \"מורכבים\" ומועברים היום למנהל התפעול, ובאיזה אחוז מהפניות בערך? זה יעזור לנו להגדיר מתי הבוט יעביר לנציג.", "rationale": "q_04 מציין שתשובות מורכבות עוברות למנהל התפעול, אך אין הגדרה של מורכבות או היקף. חשוב לתכנון כללי ההעברה לנציג בסביבה עם סובלנות נמוכה לטעויות (q_15) ויעד של ירידה של 30% בפניות.", "source_question_ids": ["q_04", "q_15", "q_03"]}, {"text": "אם אפשר, נשמח להבין מי אחראי על עדכון מסמך השאלות הנפוצות ועל המחירון, ואיך תרצו שישתקף שינוי בהם (למשל, האם מסמך השאלות הנפוצות ייבדק ויעודכן לפני ההשקעה בפתרון).", "rationale": "q_10 מציין שבמסמך השאלות הנפוצות יש סעיפים ישנים, ולא ברור מי אחראי על עדכון המקורות. מידע שגוי יפגע ישירות בדיוק התשובות, שבו הסובלנות נמוכה (q_15).", "source_question_ids": ["q_10", "q_08", "q_15"]}, {"text": "אם כבר חשבתם על זה, מה הם הכללים שלכם לגבי שמירת שיחות וואטסאפ שכוללות שם וכתובת של לקוחות, ולמשך כמה זמן, ואם יש דרישות פרטיות שחלות עליכם?", "rationale": "q_14 מציין שנאספים שם וכתובת (מידע אישי), אך אין מידע על שמירה, גישה או דרישות פרטיות, והפתרון עשוי לעבד את המידע באמצעות שירות AI חיצוני.", "source_question_ids": ["q_14"]}, {"text": "אם יש לכם נתון על כך, כמה פניות בשבוע מגיעות באנגלית, ובאילו נושאים? כך נדע כמה משקל לתת לתמיכה באנגלית.", "rationale": "q_13 מציין עברית ואנגלית ללא פירוט היקף האנגלית, מה שמשפיע על היקף הבדיקות ועל עדכון חומרי הידע (הם בעברית ככל הנראה אך לא צוין).", "source_question_ids": ["q_13", "q_08"]}]}
--- END OF SYSTEM OUTPUT ---
