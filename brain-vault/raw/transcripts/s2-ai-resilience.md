Session 2 - AI Resilience — transcript

[0:00] cover
Welcome back. This is Session 2 in our series on using generative AI well, and safely, at work. In Session 1, we separated the model from the harness around it. Today we ask what that means for your organization. If models, vendors and apps keep changing, what do you own that survives a switch? Keep this picture in mind. The model in the slot at the top keeps being swapped. The seven foundations underneath never change.

[0:26] agenda
By the end of this session, you'll be able to do four things. Explain what makes an organization agnostic. Name the seven foundations it owns. Show how a model switch becomes a configuration change. And run a lock-in audit on a real workflow. We'll start with what you rent and what you own, then walk through the seven foundations, and finish with a hands-on audit.

[0:48] why
Why does this matter? Because the model you use today will not be the model you use next year. Models retire. Versions are replaced, and older ones are switched off on the vendor's schedule, not yours. Terms change. Prices, data handling and limits move, sometimes with little notice. And approvals change. What security authorizes today can change in either direction. So the question for this session is simple. What do we own that survives a switch?

[1:15] agnostic
Let's define the goal. An organization is agnostic when it can swap the model, or the whole vendor, without rebuilding its work. Watch the figure. At the top is what you rent: the model, and the app or harness around it. Expect those to change. At the bottom is what you own: seven foundations. They meet at interfaces you control, like MCP, a vendor-neutral API schema, and the skill format. Now watch the first swap. The model changes. Nothing below it changes. Then the app changes. And still, nothing below it changes. Swap the top. Keep the bottom.

[1:50] switches
A switch can happen at four levels. A model version: same vendor, newer model. This is the most common switch, and the easiest to miss. A vendor: a different model family entirely. An endpoint: the same model through a different door, like moving from the vendor's own API to a cloud provider. And a harness: a different app or agent tool. Each switch is cheap only if something is already true. Prompts and evals are stored. The workflow layer is vendor-neutral. The endpoint lives in configuration. And your tools and skills are portable.

[2:24] isnot
Let's clear up four common beliefs. "Agnostic means using every vendor." It doesn't. It means being able to switch, usually while running just one. "A gateway makes us agnostic." It helps. But if your prompts, tools, skills and tests are tied to one vendor, you're still locked in. "Switching is a migration project." With configuration and evals, it's a tested, one-line change. And, "agnostic means lowest common denominator." No. Use each vendor's best features, just reach them through interfaces you own.

[2:59] loop
Here is the core idea of the session: seven foundations, one loop. A use case enters at the top and meets each foundation in order. First, the MCP tools that connect it to your data. Then the container it runs in. Then scanning, so every change gets checked. Then skills, the know-how you keep. Then approved code packages. Then the API framework, where the model and endpoint are pinned in configuration. And finally, evals. The evals watch for two kinds of drift. Model drift, when a new version answers differently. And use-case drift, when the business, the data or the users change, but the prompt stays the same. When either one shows up, the fix is local. Swap the model in configuration, or update a skill or prompt. Everything else stays where it is.

[3:49] seven
Here are the seven things you own, in one view. Approved MCP tools: your connection to the data, usable by any harness that speaks MCP. Containers: the authorization attaches to the image, not the model. Scanning: every new package, skill or model gets the same checks. Skills: know-how captured once. Code packages: workflows built from known, pinned parts. A multi-vendor API layer: changing models is a config change. And stored evals: how you know a swap worked. None of these belongs to a model vendor. Wherever you don't own one, that's where lock-in hides.

[4:28] config
Let's go deeper on three of them, starting with the API layer. A model switch should be a one-line change. Watch the figure. The configuration file names the endpoint, the model version and the prompt. In the first run, the request goes through model A, the output comes back with the same fields, and the evals pass. Now one line changes. Model A becomes model B. The second run goes through model B. The output has the same shape. And the evals pass again. Change the configuration, not the code. And always pin a named version, never "latest", so the model can't change under you.

[5:06] skills
Next, skills. Write a skill once, and install it wherever you're authorized. A skill is a folder of instructions, in an open format that most major harnesses now read. Watch the path. The skill package goes into your internal registry, where it's reviewed, scanned, and pinned to a version. Then it's installed into harness A, harness B, and harness C. Each one gets tested. Harness C fails at first, because file paths differ. That's normal. Fix it, and test again. Write once. Test in each harness.

[5:39] evals
And the most important one: evals. Evals are how you know a switch worked. An eval is a stored test set for a prompt, skill or workflow, run on a schedule and on every change. Watch the score over time. When a new model version arrives, the score drops below the threshold. That's model drift. The fix: pin the version and fix it in configuration, and the score recovers. Later, the data and the users change, and the score slides slowly. That's use-case drift. The fix: update the skill or prompt. Without evals, being agnostic is a hope, not a fact.

[6:16] rule
Here's the one idea to hold on to. Rent the model. Own the connections. Own the know-how. And own the proof. Connections are your MCP tools and API layer. Know-how is your skills and prompts. And proof is your stored evals.

[6:33] playbook
So what happens when a new model arrives? You test before you switch. Step one, a new model arrives. Step two, pin your current version, so nothing changes by accident. Step three, run your stored evals on the new model. Step four, compare the results. If it fails, stay pinned, and try again later. Nothing is lost. If it passes, step five: switch in configuration. And step six, keep monitoring for drift. The rule is simple. No evals, no switch.

[7:05] exercise
Time to practice. Pause the video for this one. Part A. Pick one workflow your team runs every week. For each of the seven foundations, mark whether your organization owns it, a vendor owns it, or it's missing. Part B. Imagine the model behind that workflow is retired in thirty days. Where is the model named, in configuration or in code? Which evals would prove the new one works? Which prompts or skills might need changes? Who approves the switch? And what would make the next one easier? When you're done, name your single biggest gap. For most teams, it's evals.

[7:42] check
Before we finish, see if you can answer these six questions in your own words. What makes an organization agnostic? Can you name four of the seven foundations? Why do stored evals matter most when you switch? What's the difference between model drift and use-case drift? Where should the model name and endpoint live? And why test a skill in each harness, if the format is shared? If any of these feel shaky, go back to that part of the video.

[8:10] bridge
Here's where we go next. Today's proof was automatic: stored evals that test a workflow every time something changes. But output is fast and fluent. So how do you know it's right when you're the one reading it? That's Session 3: safe prompting and verification. The one rule for safe use, prompting like you're briefing a new teammate, saved instructions, and checking sources, facts and numbers before anything gets used. Thanks for watching. See you in Session 3.
