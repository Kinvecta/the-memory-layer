Session 6 - Building Workflows — transcript

[0:00] cover
Welcome to Session 6 in our series on using generative AI well, and safely, at work. In Session 5, we put one model call inside a container, with the endpoint in config and the key in a secrets store. Today, we chain those calls together. Today is about building workflows. Watch the picture: three Mondays, the same task done by hand. On the first Monday, the prompt gets edited. On the second, a step gets skipped. On the third, nobody checks. Then one fixed lane runs the same steps every time, with a check.

[0:34] agenda
By the end of this session, you'll be able to do four things. Tell a workflow from a chatbot and an agent. Pick a good first workflow. Chain saved prompts into fixed steps, with a check and a review. And run it safely, with a container, logs, and limits. We'll spend the most time on the anatomy of a workflow, because that's the pattern you'll copy.

[0:55] why
Why does this matter? Because three complaints keep coming up. "We paste the same prompt every Monday." That's a repeat task, done by hand, a little differently each time. "It broke, and nobody noticed." Workflows fail quietly when inputs change, unless something checks the output. And, "we can't get agents approved." The good news: you don't need them yet. So the question is: how do we turn a repeat task into a safe, fixed pipeline?

[1:22] whodecides
Start with one question: who picks each step? Watch the chatbot lane. The person picks every step: ask, read the reply, ask again, copy it out. The person decides, each turn. Now the workflow lane. The whole path is drawn before it runs. Then every run follows it exactly: pull inputs, summarize, check, route. A designer decided, in advance. Now the agent lane. The AI plans, acts, and checks, in a loop. Then a person reviews. Here, the AI decides, at run time. In a workflow, the path is fixed before it runs.

[2:01] available
So how far can you climb with what you have today? Read the ladder from the bottom. With chat only, you prompt by hand and share templates. With chat plus an API, you can build scripted or low-code workflows that call the model, with MCP servers, the connectors we'll cover in Session 7, as fixed steps. Above that, tool calling lets the model look things up. And a full harness adds skills and agents. Here's where to stop: chat plus an API is enough. That's working, containerized automation.

[2:31] pick
Which task should be your first workflow? Score it. Watch the checklist score a weekly status report. It repeats weekly. It has the same shape every time. There's a known-good output. A lead already reviews it. The data is at an approved level. And you can measure the time it takes. Six out of six: ready to build. Score your own task the same way. Four out of six is enough to start.

[2:56] anatomy
Now, the anatomy of a workflow. Six fixed steps, including one check and one person. Watch the figure. A trigger starts the run, usually a schedule. Then the inputs are pulled, through an MCP server, as a fixed step. Next, the saved prompt, version two, goes to a pinned model through the API. Then the output is validated. A named person reviews it. And then it's delivered. Every step writes to the audit log. Now the log clears, and one full run goes through. Each step lights up and writes its line again. The run waits at review, because a person signs off. Then it's delivered. The script decides each step, not the model.

[3:36] validate
A workflow's main risk is that it breaks quietly. Validation is how you hear it break. Here's the draft. It reads well. Now the checks run. Check one, format: pass. Check two, required fields: pass. Check three, links: fail. There's a link nobody expected. Check four, recipients: pass. One failure is enough. The run is flagged and routed to a person, and nothing is delivered. Bad output is flagged, never passed on.

[4:06] saferun
Next, run it safely. Sealed in, logged, and capped. Watch the figure. This is the same container we built in Session 5. The workflow runs inside it. The key is injected at run time, from the secrets store. The call to the model endpoint is allow-listed. So is the call to the MCP server. But a call to anywhere else is blocked at the wall. Every run is logged. And a cost limit stops the run before a loop can run up the bill.

[4:32] release
That's how it runs. Now, what happens before a change goes live? Test it, then version it. Watch the figure. Prompt version three is a draft. It runs the test set. Five known-good cases, and each one passes. Then the tricky case: a report that says, "ignore your rules." The prompt holds. Only then does release v3 go to the team library, and the log records it. A new version is a new release, never an edit in place.

[5:00] measure
How do you prove it's working? Four numbers. Time saved per run. Errors caught in review. Workflows running in production. And how many other teams reuse your prompts. Time the task by hand first, so you have a baseline.

[5:15] rule
Here's the one idea to hold on to. Fix the path. Check every output. A person approves before it ships. The script decides each step, the check catches bad output, and nothing is delivered without review.

[5:30] exercise
Time to practice. Pause the video for this one. Part A. Design it. Pick one weekly task, and fill in a workflow card: the trigger, the inputs, the steps as saved prompts, the check, and the reviewer and delivery. The status report card on the slide is your example. Part B. Break it. Run six scenarios against your design. The input template changed. One report is missing. The output has an unknown link. The model version was updated. A report says, "ignore your rules." And the run loops and keeps calling. For each one, does your workflow flag it, or pass it on? Anything that would pass silently is a missing check.

[6:12] check
Before we finish, see if you can answer these six questions in your own words. Who decides the steps in a workflow? What can a team build with only chat and an API? Can you name three signs of a good first workflow? What happens when a validation check fails? Where should a workflow's prompts live? And if a report in the inputs says "ignore your rules," which two parts of the workflow stop that from shipping? If any of these feel shaky, go back to that part of the video.

[6:41] bridge
Here's where we go next. Today, the script decided every step. But what happens when the model asks for the step itself? That's Session 7: tools, MCP, and prompt injection. The model asks for a tool. The harness checks the request and runs the approved ones. And whatever comes back is untrusted. Thanks for watching. See you in Session 7.
