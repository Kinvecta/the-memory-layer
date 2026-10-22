Session 8 - Agents, Skills and Running the Program — transcript

[0:00] cover
Welcome to Session 8, the final session in our series on using generative AI well, and safely, at work. Seven sessions built the pieces. Today we put them together, and then we talk about running the program itself. Watch the picture. Inside the harness, a skill holds the method. The model brings judgment. Tools bring facts and actions. And at the exit, a person approves what leaves.

[0:25] agenda
By the end of this session, you'll be able to do four things. Explain how a skill loads, and why it stays cheap. Combine a skill, tools and a model into one repeatable job. Put guardrails on an agent. And plan a rollout by stage, role and measure. Bring the saved prompt you wrote in Session 3. You'll turn it into a skill in the exercise.

[0:46] why
Why does this matter? Because AI programs tend to stall in three ways. Know-how walks out the door. The best prompts live in one person's chat history, and when they leave, so does the method. Unchecked skills get installed. In one audit, roughly a third of skills in a public registry had a security flaw. And courses end at Stage 1. People finish training, but nobody checks whether the work changed. So the question is: how does know-how become shared, safe, measured practice?

[1:16] skills
Start with skills. A skill is like an onboarding guide that the AI loads only when it's needed. Watch the figure. Six skills are installed, but only their names and descriptions load. Now a request comes in. One description matches. Then the full instructions load. Then only the file it needs, the template. Add it up: about two and a half thousand tokens, around one percent of the window. Dozens installed. One loaded. And a vague description is a skill that never fires.

[1:45] skillcode
But a skill is software, so treat every skill like code. Read every file before it's installed. Scan it, and pin the version, which means locking it to one known version. Install only from your internal registry, your approved download shelf. Run any skill with scripts inside a container. If an agent rewrites its own skill, a person approves it first. And decide who may install skills before you turn them on.

[2:11] combo
Now put a skill, tools and a model together. Each part does what it's good at. Watch the worked example. The request: review the vendor contract. The skill brings a checklist, a template, and one rule: dollar figures come only from the system. The model fills the gaps. It calls the contracts MCP server for the value, the PDF reader for the clauses, and the code runner to check the dates. Then it checks its own work: the totals match the record. A person approves before anything is written back. And the result is reviewed, cited and checked. Same request, same steps, for anyone who runs it.

[2:50] agent
At Stage 5, you delegate multi-step work to an agent. With guardrails. Watch the figure. The agent runs inside a container. It plans the task, reads the tracker, and checks the rows. Then it loops back to plan the draft and the send. Every step goes into the log. Now it tries to send an email. That action holds at the gate, inside the flow. A person reviews the steps, and approves. Only then does the email leave the container. Step six: sent. Review the steps, not just the answer.

[3:24] library
All of this runs on one shared library of prompts and skills. Watch a saved prompt become a skill. Its header becomes the name and description, and its body becomes the steps. The template and the tests attach: two cases, plus one tricky one. A second person reviews it. It gets a version. It lands in the library, one home. And chat, scripts and agents all pull from it.

[3:49] stages
Now, running the program. People learn in five stages, and each stage adds one new risk. Watch the staircase build. Stage 1, chat and saved prompts: the risk is the wrong tool for the data. Stage 2, the API in a container: leaked keys. Stage 3, a fixed workflow: bad output passed on. Stage 4, tool calling: unapproved actions. And Stage 5, a harness with skills: untested skills. Now, where each role stops. Everyone stops at Stage 1. Leaders too, with a demo of the rest. Analysts go to Stage 3. Technical staff go to Stage 5. Everyone starts at Stage 1.

[4:32] measure
So how do you know the training worked? When the work changed. Watch the baselines appear first. Then the after numbers tick in. Time per report: six hours, down to two. Corrections in review: nine, down to three. Library reuse: zero teams, up to four. Workflows in production: zero, up to two. These are example numbers. The habit is real: take your baselines before training starts. Track security findings too. And every prompt, skill and workflow passes its tests before release, and again after any change.

[5:08] rule
Here's the one idea to hold on to. Write it once, as a skill. Gate what leaves. Measure what changes. Because know-how becomes shared practice when it's reviewed, tested and measured.

[5:21] exercise
Time to practice. Pause the video for this one. You only need paper. Part A. Package it. Name your Session 3 prompt, and write a description that says when to use it. Write three requests that should trigger it, and two that shouldn't. Then swap. Your partner plays the model: they read only the description and decide which requests trigger it. Fix the description until they get all five right. For homework, add the template and test cases. Part B. Plan the rollout. For one real pilot, write down the workflow, which roles go to which stage, three measures with their baselines, and the date you'll review the numbers. If any of your measures counts courses instead of work, swap it out.

[6:04] check
Before we finish, see if you can answer these six questions in your own words. What loads before a skill is triggered? Which stage does everyone complete, and where do analysts stop? What do a skill, tools and a model each add? Where must a person approve an agent's work? What makes a prompt ready for the library? And can you name two measures that show training worked? If any of these feel shaky, go back to that part of the video.

[6:31] close
And that completes the series. Watch the eight sessions tick by: models and harnesses, resilience, safe prompting, tokens and finders, AP-Is and containers, workflows, tools and MCP, and today, agents and skills. And the rule to carry with you: write it once, gate what leaves, measure what changes. Your next step is one pilot, measured. First, pick one pilot workflow. Second, take your baselines. Third, stand up the shared library. Fourth, run Stage 1 for everyone. And put the review date in the calendar before you leave. Thank you for training with us. Now go build something your team can measure.
