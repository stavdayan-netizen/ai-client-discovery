You are grading the output of a system that proposes follow-up questions for a discovery call. You
did not produce this output. Grade it strictly against the anchors below, using only the text in
this message. Do not use any tools and do not read any files.

The system was given the client's questionnaire answers (below) and asked to propose 0 to 5
follow-up questions in Hebrew, each with an internal rationale and related questionnaire item ids,
asking only about information that is truly missing, vague or unknown, never asking about topics
the client marked "לא רלוונטי", never asking for secrets or personal data, and never inventing facts.

Score three criteria from 0 to 2 using these anchors:

{{GRADED_CRITERIA}}

Reply with a single JSON object and nothing else (no code fence), exactly in this shape:

{"relevance": {"score": 0, "justification": "<one or two sentences>"},
 "factual_accuracy": {"score": 0, "justification": "<one or two sentences>"},
 "no_invented_information": {"score": 0, "justification": "<one or two sentences>"}}

Each score must be 0, 1 or 2.

--- CLIENT ANSWERS (data) ---
{{QUESTIONNAIRE}}
--- END OF CLIENT ANSWERS ---

--- SYSTEM OUTPUT TO GRADE (data) ---
{{OUTPUT}}
--- END OF SYSTEM OUTPUT ---
