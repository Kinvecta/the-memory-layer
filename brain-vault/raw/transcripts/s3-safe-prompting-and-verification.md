Session 3 - Safe Prompting and Verification — transcript

[0:00] cover
Welcome to Session 3 in our series on using generative AI well, and safely, at work. Sessions 1 and 2 were about what AI is, and what your organization owns. Today is about the everyday habits that keep your own use safe and useful. Here's the whole session in one picture. Your data passes an approval check. You give the AI a proper briefing. The draft gets verified. And a person signs off.

[0:26] agenda
By the end of this session, you'll be able to do four things. State the one rule, and apply it to a real tool. Write a prompt like a briefing. Verify a draft, claim by claim. And save a prompt as a reviewed instruction. We'll spend the most time on verification, because it's the number one gap teams have.

[0:44] why
Why does this matter? Because most AI problems at work start with a habit, not the technology. Fluent is not correct. Confident, well-written output can still be wrong. One bad paste of confidential data or personal information can end a program. And vague in, vague out. One-line asks get generic drafts, and people give up. So the question for this session is: how do we use AI safely, and trust what it gives us?

[1:11] onerule
Start with the one rule. Data only goes into a tool approved for its sensitivity level. Watch the flow. Your data has a sensitivity level. The first check asks: is this tool approved for this data? If not, switch tools first, before you write a single prompt. If yes, you write the prompt, and the AI produces a draft. Then the second check: does the draft pass verification? Here it fails. So you revise, and run it again. This time it passes. And a named person signs off before anything is used. Two checks. One sign-off.

[1:47] datalevels
Here's how to match the data to the tool. This grid is an example. Your organization will have its own levels and its own approved tools. Public information, that's already published, can go almost anywhere. Internal information belongs only in an approved enterprise tool. And sensitive information, like personal data, confidential or controlled information, only goes into a tool approved for that level. If the data and the tool don't match, fix it before the prompt.

[2:14] accident
Accidents happen. What matters is what you do next. Stop. Don't keep chatting, or paste more to fix it. Report it. Tell your security or privacy contact right away. Record what was shared, in which tool, and when. Then follow your incident process. Reporting early is what limits the damage. A quiet delete can make it worse.

[2:37] accountable
The one rule comes with three duties. And the short version is: AI drafts, and a person signs. Human accountability. Anything used in a decision needs a named reviewer. Records and transparency. Some work must be labeled as AI assisted, and prompts and outputs can be records. And responsible use. When output affects people, check it for bias, and know who to escalate to.

[3:02] briefing
Now, prompting. Give the AI what a new teammate would need. Watch the figure. The first try is just, "summarize this." The answer is vague and generic. Now the same request, as a briefing. A role: you are a contracting specialist. A task: list every deliverable and its due date. An audience: for the program manager. A format: a table. And the source: the attached document. Now the answer is a usable draft. Then you refine it with short follow-ups. Make it shorter. Add the clause numbers. Pasting the source matters most. It keeps the model working from your material, not its memory.

[3:42] verify
Next, verification. Fluent is not correct, so check every claim. Watch the draft. It reads well. Now check each claim against the source memo. The date is right. The budget is wrong. The source says four point two million, and the draft says two point four. The approver's name is not in the source at all. The quote is right. And the vendor count is right. Two of five claims fixed before anyone used them. That's what hallucination looks like in practice: confident, fluent, and false.

[4:13] checklist
Here's a checklist you can keep. Check the sources: does each claim come from the material you gave it? Check the numbers. Check names and dates. Check quotes, word for word. Look for what's missing, anything the source said that the draft left out. And check tone and bias, especially when the output is about people.

[4:32] library
Finally, save what works. A prompt that works becomes a saved instruction. Watch the lifecycle. First, write it with a header: a name, a purpose, an owner, the inputs, and the approved data level. Second, a second person reviews it. Third, it's tested, with sample inputs that have known-good outputs, plus one tricky case, like a document with a planted instruction. Fourth, it's published to the team library. And fifth, other teams reuse it. And when the prompt or the model changes, it goes back through review and tests.

[5:07] rule
Here's the one idea to hold on to. Right tool for the data. Brief it like a teammate. Check every claim. And a person signs. That's two checks before anything is used: the data is cleared for the tool, and the draft passes verification.

[5:23] exercise
Time to practice. Pause the video for this one. Part A. Take a short memo and an AI summary of it. Find the three errors in the summary. Then rewrite "summarize this" as a briefing, run it in an approved tool, and check every claim in the new draft. Part B. Turn your briefing into a saved instruction. Give it a name and purpose, an owner and inputs, an approved data level, and two test cases. When you're done, ask yourself: what did your check catch?

[5:53] check
Before we finish, see if you can answer these six questions in your own words. What is the one rule? What do you do right after pasting something you shouldn't have? What are the parts of a briefing prompt? Can you name four things to check before using a draft? Who is accountable for AI assisted work? And what makes a prompt ready for the team library? If any of these feel shaky, go back to that part of the video.

[6:18] bridge
Here's where we go next. Today we pasted the source into the prompt, so the model works from our material. But what can the model actually see when it answers? That's Session 4: tokens, context, and how AI finds your data. What fits in the context window, what gets dropped, and how tools fetch your information. Thanks for watching. See you in Session 4.
