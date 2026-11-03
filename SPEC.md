# AI Client Discovery - Product Specification

Status: Draft v0.1 - for owner review before development.
Language of this specification: English. All end-user UI and questionnaire text: Hebrew, RTL.

## 1. Product, users, and objective

Build a small, practical **AI Client Discovery** system for an AI implementation consultancy. After an initial fit call, a team member creates a lead, sends a personalized discovery questionnaire, and later reviews the submitted answers, follow-up answers, and an AI-assisted preliminary analysis before the next discovery conversation.

User roles:
- **Consultancy admin/team member**: creates leads and questionnaires, edits the master questionnaire, reviews progress and answers, writes private comments, reviews AI outputs, and manages status.
- **Lead respondent**: fills out only their own questionnaire through a private, non-guessable link; may pause, resume, and submit. No access to internal notes or AI analysis.

Demo scope: a small consultancy (initially 1-5 staff), tens of leads, full-featured on both desktop and mobile, with a mobile-first responsive layout even though long answers may be easier to type on desktop. Hebrew RTL throughout. This is a learning project for the first four phases of Lesson 9: **Design, Place, Manage, Test/Eval**. **Deployment is explicitly out of scope for now.**

## 2. Core workflow

1. Admin creates a lead with company name, contact email, and phone, and optionally a contact person.
2. Admin creates a questionnaire instance from the current master questionnaire; its heading is **"שאלון איפיון להטמעת AI - {שם העסק}"**, where the company name is injected automatically. Do not ask the lead to re-enter the company name.
3. Admin copies/shares the questionnaire's unique link. Track the actual sent timestamp separately from creation; in a local demo allow admin to mark it as sent. **Never claim an email was sent without a real send operation.**
4. Lead fills the original questionnaire; every keystroke updates local state immediately and a durable local draft, while background saves to the backend are debounced. The UI distinguishes "שומר..." from server-confirmed "נשמר". A **"שמירת טיוטה ויציאה"** button forces a save and allows resumption through the same link.
5. When the lead chooses **"המשך לשליחה"**, the answers are saved and the AI reviews gaps. Ask **0-5 concise, useful, nonredundant follow-up questions**, never five just to meet a quota. Questions are optional/skippable; do not needlessly request sensitive details. Display them in the same flow before final submission.
6. Lead clicks **"שליחה סופית"**. Save all original and follow-up answers, with submitted timestamp. If no relevant follow-up questions exist, proceed directly to final submission with clear confirmation.
7. The system prepares an **internal draft AI analysis**: business need, current workflow, hoped-for outcomes/KPIs, relevant stakeholders and systems, data and security considerations, unknowns, suggested questions for the next call, and tentative solution directions clearly labeled as hypotheses. The team reviews it; AI does not autonomously make the final solution decision.
8. Admin reviews the full questionnaire, adds private notes alongside individual answers and general lead notes, tracks progress and advances lead status.

## 3. Statuses and progress tracking

Primary statuses (Hebrew labels, in this order):
1. `חדש` - lead record created; questionnaire not sent.
2. `ממתין למילוי` - questionnaire sent; not finally submitted.
3. `התקבל` - final submission received.
4. `בבדיקה` - internal team is reviewing the answers/analysis.
5. `הושלם` - initial discovery stage is complete.

**Draft is not a primary status.** Draft activity is a separate indicator under `ממתין למילוי` (not started / started / saved and left / resumed), with the last saved timestamp. Store status history with timestamps; allow controlled admin changes.

Dashboard: company name, lead status, questionnaire sent date/time, elapsed calendar days since sent, completion percentage/progress bar, last activity, and submission date when applicable. Lead-detail page has four main tabs: **פרטי לקוח**, **תשובות והערות**, **ניתוח AI**, **מעקב מילוי**.

Progress tracking on the lead-detail page:
- Link created and actually sent timestamps; first opened and first meaningful answer timestamps.
- Current completion percentage and sections completed, based on fields in **this lead's frozen questionnaire version**; count answered applicable questions, not characters typed. Repeatable stakeholder rows count as their question, not one question per row.
- First/last activity, final submission time, elapsed time from first open to submission, approximate **active filling time**, and distinct filling sessions.
- Session timeline: started, paused/idle, resumed, draft explicitly saved, progress changed, final submission. Show timestamps and percentage at useful milestones; avoid a keystroke log.
- Active time is approximate: stop counting when tab is hidden or after an inactivity threshold (initial proposal: 5 minutes). Avoid double counting and use a clearly documented session definition.
- Track follow-up AI questions asked/answered/skipped separately. The original questionnaire progress should not suddenly decrease when follow-up questions are generated; show the follow-up step separately.
- Lead also sees a simple progress indicator and save status. Make tracking transparent; do not record full keystroke histories, mouse movements, or unnecessary personal data.

## 4. Admin capabilities

### Lead management
- Create and edit company name, primary contact email, phone, and optional primary contact name.
- On submission, extract stakeholder names, roles, and responsibilities from question 5, and project sponsor name/role from question 6, into a reviewable contacts list. Avoid duplicates; preserve original questionnaire responses and clearly identify extracted vs manually added contacts.
- Add, edit, and remove contacts manually; changes in contacts must not rewrite submitted answers.
- Show private general notes and dated history per lead.

### Questionnaire template editor
- Edit the master template through the admin UI, without modifying code: add/remove/reorder sections or questions, edit wording, choose supported types (long text, short text, date, selection, repeatable people rows), set required/optional.
- New questionnaire instances take a **versioned snapshot** of the template. Edits to the master must not alter in-progress or submitted instances.
- Prefer safe deactivation/archive over destructive removal of historical answer fields. Stable question IDs; preserve answer linkage through template versions.
- Preview before publishing a new template version; retain initial original as version 1.

### Internal notes
- Each answer supports a **thread** of multiple internal notes, entered using a `+ הוסף הערה` button.
- Render notes as easy-to-read chat bubbles showing author, date, local time, and text; preserve old notes when a new one is added. Sorting chronological, with clear separation from original client text.
- Additionally support lead-wide notes unrelated to a specific answer.
- Internal notes are **never** visible through the respondent link or included in client-facing output.

### AI analysis
- Clearly separate **verbatim client answers**, **AI interpretations/hypotheses**, and **team-written notes**.
- Flag missing evidence; reference source question IDs for major claims. Do not invent API availability, budgets, KPIs, commitments, facts or technical capabilities.
- AI output is a reviewable internal draft and must not be presented as an approved solution.

## 5. Original questionnaire content - preserve Hebrew wording

Source: attached original document titled "שאלון אפיון להטמעת פתרונות AI.docx". Keep original content and section grouping for initial template v1; user can later edit text through the admin template editor. Attribution/intro can be configured by admin rather than hard-coded as a provider's brand.

**Intro (original)**: "לקוח יקר, על מנת שנוכל לדייק את הפתרון הטכנולוגי לצרכים העסקיים שלך ולהבטיח הטמעה חלקה ומוצלחת, אנא הקדש/י מספר דקות למענה על השאלות הבאות."

### חלק א': ההקשר העסקי והמטרות
1. מהו האתגר המרכזי או נקודת הכאב (Pain Point) שאתם מנסים לפתור באמצעות בינה מלאכותית?
2. מהי ההשפעה העסקית המצופה מהטמעת הפתרון? (לדוגמה: חיסכון בזמן, הגדלת הכנסות, שיפור שירות)
3. כיצד נמדוד הצלחה? אילו מדדי ביצוע (KPIs) מרכזיים ישתפרו בעקבות הפרויקט?

### חלק ב': התהליך הקיים ובעלי העניין (Stakeholders)
4. תאר/י בקצרה את התהליך הידני כפי שהוא מתבצע היום ללא AI:
5. מי הם הגורמים והתפקידים הרלוונטיים המעורבים בתהליך זה כיום? (Repeatable rows: שם, תפקיד, אחריות בתהליך; add/remove person.)
6. מי יהיה מנהל הפרויקט / "הספונסר" מתוך הארגון? (איש הקשר המרכזי לקבלת החלטות) (Fields: שם, תפקיד.)
7. מי יהיו משתמשי הקצה של המערכת?

### חלק ג': נתונים (Data) ותשתיות טכנולוגיות
8. היכן נמצא כיום המידע והידע הנדרש לתהליך? (אתר אינטרנט, קובצי PDF, מערכת CRM, וכו')
9. האם המידע מובנה (טבלאות, מסדי נתונים) או לא מובנה (טקסט חופשי, מסמכים)?
10. מהי איכות המידע הנוכחי ועד כמה הוא מעודכן?
11. לאילו מערכות ארגוניות קיימות נצטרך להתממשק? (לדוגמה: Salesforce, Slack, מערכות פנים). האם קיימים API פתוחים?

### חלק ד': חווית המשתמש וממשק (UI/UX)
12. כיצד תרצו שמשתמשי הקצה יתקשרו עם פתרון ה-AI? (למשל: צ'אט ב-WhatsApp, בוט באתר, מערכת פנימית)
13. באיזו שפה או שפות נדרשת המערכת לתמוך?

### חלק ה': אבטחת מידע, פרטיות וניהול סיכונים
14. האם המערכת תיחשף למידע רגיש, פרטי לקוחות (PII) או סודות מסחריים?
15. מהי רמת הסובלנות של הארגון לטעויות מערכת (הזיות/Hallucinations)?
16. האם נדרש גורם אנושי המאשר את הפעולה (Human in the Loop) לפני ביצוע סופי?

### חלק ו': מסגרת זמן ותקציב
17. האם יש תאריך יעד קשיח להשקת גרסה ראשונית (MVP) או אבן דרך ארגונית? (Date field.)
18. האם הוגדר תקציב מיועד לשלב ההקמה (CapEx) ולשלב התחזוקה (OpEx)?

## 6. Data and persistence

Conceptual data entities: `users`, `leads`, `contacts`, `questionnaire_templates`, `template_versions`, `questionnaire_instances`, `answers`, `fill_sessions`, `progress_events`, `follow_up_questions`, `internal_notes`, `ai_analysis_runs`.

Use stable IDs, timestamps, source question IDs, and version references. Never overwrite originals when producing AI summaries. For local demo, use synthetic lead/company records only; do not upload real client-sensitive information to public GitHub.

Autosave design:
- Local state and browser draft are updated on each change, without network or model calls per keystroke.
- Debounced backend save after typing pauses (~1 second as a starting point), and explicit immediate saves on key transitions and "save draft" action. Avoid concurrent writes overwriting more recent edits; document conflict/ordering behavior.
- Draft should survive refresh; when the browser is offline, keep local changes and display an unsynced indicator. Test eventual synchronization and no silent loss. Local browser storage is a recovery aid, not a substitute for server persistence; minimize sensitive retention and explain limitations on shared devices.
- No AI call while the user is typing. Run AI only after explicit continue-to-submit and for authorized internal analysis; cache generated results to avoid repeat charges on page refresh.

## 7. AI behavior and safety limits

Follow-up generation (after original questionnaire, before final submission):
- 0-5 short, clearly worded questions in Hebrew only when materially useful to the next discovery call.
- Do not repeat answered questions or request unnecessary secrets/PII; avoid speculative claims. Questions are skippable.
- Use structured output with stable IDs, rationale for the internal team, and links to relevant original question IDs. Rationale remains internal.
- On AI failure, don't block the user: allow submission without additional questions and flag analysis as pending/unavailable.

Internal analysis: summarize using only submitted answers; distinguish facts, assumptions, unanswered questions, risks, and potential directions. No final implementation recommendation without human review.

Costs: minimize model calls. **No paid API/services, Railway provisioning, domain purchase, or deployment without explicit owner approval and budget disclosure**. Mock AI responses for deterministic tests. Actual live AI and its Eval results must be labeled clearly as real vs simulated.

## 8. Design and visual identity

Selected palette: **Turquoise, Coral & Sunshine**.
- Background: `#F4FBFA`
- Turquoise primary: `#06A6A1`
- Coral secondary: `#FF846C`
- Sunshine accent: `#F4B942`
- Deep ink: `#183E50`
- Optional soft backgrounds: `#DCF5F2`, `#FFE8E1`, `#FFF3D5`

Use color across navigation, tabs, action buttons, selected states, progress bars, summary cards, status chips, section markers, and note/thread accents; maintain legible contrast, don't rely on color alone for meaning. Friendly but polished SaaS style, generous spacing, rounded cards, readable Hebrew font, RTL layouts. Both respondent and admin experiences must be fully usable on desktop and mobile; **design mobile-first**. Long-form entry may be more comfortable on desktop, but mobile must not be a reduced-functionality version. Focus states, labels, accessibility, and keyboard navigation are required.

### Explicit mobile and responsive acceptance requirements
- Design and verify at representative narrow phone widths (including 320px and 375px), tablets (768px), and desktop (1280px); adapt to viewport instead of requiring horizontal page scrolling.
- The **respondent form** uses a comfortable single-column layout on phones, readable Hebrew text, sufficiently large touch targets (aim for at least 44x44 CSS px for key controls), visible field labels, clear validation, and generous tap spacing. Long-answer fields resize or otherwise remain practical on mobile; avoid awkward zooming.
- Repeatable **people/stakeholder rows** become stacked person cards on narrow screens, each with labeled name, role, responsibility fields and an accessible remove control. The add-person action stays obvious. Never rely on a wide table that overflows the screen.
- Questionnaire **progress and autosave state** remain visible and understandable on mobile (without obstructing form controls). Navigating between sections, saving draft, returning to fill, following up, and final submission must all work on touch screens.
- **Admin dashboard** cards and client rows reflow into mobile-friendly stacked cards or appropriately adapted lists; company, status, elapsed days, progress, and last activity remain legible. Do not simply compress a desktop table to unreadable columns.
- **Lead details** keep all four tabs accessible through a mobile-safe navigation pattern; notes appear beneath the relevant answer on phones and alongside it where width permits on desktop. Note bubbles must wrap long Hebrew text, emails, links and timestamps correctly.
- **Questionnaire template editor** supports add, edit, archive, reorder, publish, and preview on mobile as well as desktop; provide accessible move-up/down controls instead of relying solely on drag-and-drop.
- Show proper RTL/LTR handling of email addresses, telephone numbers, dates, URLs, IDs, and numeric metrics in mixed-direction layouts. Maintain contrast with the approved colorful palette, visible keyboard focus, readable form errors, and no meaning conveyed by color alone.
- Include a **mobile acceptance checklist and at least one automated responsive browser smoke test** for respondent and admin flows when a browser test runner is available; also manually inspect touch behavior and long Hebrew content on representative viewport sizes. Clearly report which checks were actually performed versus only planned.

## 9. Non-goals for first version

No full CRM, outbound email automation, calendar integration, invoicing, proposal generation, auto-sending recommendations to clients, AI agents taking irreversible actions, Google Docs export/integration, Google Drive connectors, production multi-tenant platform, or cloud deployment. A **separate Google Docs Q&A document per submission** remains a desired follow-on feature, not forgotten, but deliberately deferred to keep the assignment manageable.

## 10. Acceptance criteria (demonstrable checks)

1. Admin can create a company with email and phone; questionnaire heading automatically uses company name.
2. Admin can mark link actually sent; sent timestamp and elapsed days appear in dashboard.
3. Lead can enter, leave, and resume answers; auto-save survives refresh without per-character AI calls.
4. A clear save indicator distinguishes local/unsynced from backend-confirmed state.
5. Admin can edit and publish a new questionnaire template version; old lead instances retain original wording and field IDs.
6. Repeatable stakeholder rows add/remove without losing data; sponsor name/role is captured.
7. Contacts appear in lead detail from submitted stakeholder/sponsor data, without destructive overwrites or duplicate records.
8. Dashboard and lead detail accurately display completion percent, first/last activity, approximate active time, session count, and relevant timestamps.
9. Lead can save draft; primary status remains `ממתין למילוי` until final submission.
10. AI asks no more than five relevant, optional follow-up questions, or zero if no gap exists; can fail gracefully.
11. Final submitted answers, AI responses, and internal analysis are separate and traceable.
12. Admin can add multiple timestamped, author-attributed notes per answer and per lead; lead cannot see them.
13. Admin can review AI analysis with cited source question IDs and unresolved questions; it is never marked verified automatically.
14. Functional code Tests and AI Eval case definitions exist, with a reproducible free CI workflow that does not use real paid APIs.
15. Respondent and admin workflows are usable at 320px/375px phone widths, 768px tablet, and 1280px desktop without horizontal page scrolling or inaccessible controls; add-person inputs, admin notes, editor and progress tracking remain usable on mobile.
16. Repository includes planned architecture and its rationale, GitHub Issues/Project, `practice.md`, feature branches and Pull Requests as part of the Lesson 9 workflow. Deployment is excluded.

## 11. Lesson 9 expected deliverables

- **Design**: `SPEC.md` (this file) and `architecture.md` with component diagram/flows and documented decisions.
- **Place**: extend `architecture.md` to detail local/demo component placement, possible future hosting, storage, resource and spend assumptions, secrets, and limits; **plan only, no deployment**.
- **Manage**: GitHub repository, Project board (To do / In progress / Done), small Issues with acceptance criteria, a branch + PR per issue, `practice.md`, minimal `CLAUDE.md` pointer.
- **Test/Eval**: `tests/`, `evals/`, `.github/workflows/ci.yml`, fixed deterministic test inputs, meaningful Eval cases for follow-up questions/analysis, clear distinction between mocked tests and real model evaluations. GitHub Actions should gate PRs wherever feasible.

## 12. Scope control and incremental build

Implement in reviewable slices, not one giant request. Suggested early slices: (1) architecture/spec and board, (2) lead creation and questionnaire snapshot, (3) form and autosave, (4) admin progress/timeline and notes, (5) AI follow-up and draft analysis, (6) tests/evals/CI. Split further when an issue is too large. The owner approves plans and merges before proceeding.

Open decisions for owner review: exact auth method for local demo vs future production; exact UI field types for initial 18 questions; specific live AI provider/model and budget; whether to create Google Docs export in a later milestone. Do not silently choose paid services.
