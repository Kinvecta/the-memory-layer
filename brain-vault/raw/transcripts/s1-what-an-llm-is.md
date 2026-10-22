Session 1 - What an LLM Is — transcript

[0:00] cover
Welcome. This is the first session in a series on using generative AI well, and safely, at work. Today we answer two questions. What is a large language model? And what is the harness, the app or platform wrapped around it, that decides what the model can actually see and do? Keep this picture in mind. A model in the middle. Skills and tools beside it. And a harness around all of it.

[0:26] agenda
By the end of this session, you'll be able to do four things. Explain what a large language model is, and what it is not. Name the parts of an AI system. Recognize the six main types of harness. And tell a chatbot, a workflow and an agent apart. We'll start with the model, move out to the harness around it, then sort out the three words people mix up most. The session finishes with a hands-on exercise.

[0:51] why
Why start with vocabulary? Because most confusion in AI briefings is about words, not technology. When someone says, "we use ChatGPT," they usually mean a whole system, not just a model. When someone says, "it's an agent," it's often a chatbot, or a fixed workflow. And when someone says, "the AI did it," they're usually crediting the model for something the harness allowed. Three terms get misused more than any others: AI safety, agent, and workflow. By the end of today, you'll be able to use all three precisely.

[1:25] llm
So what is a large language model, or LLM? It's a trained engine that predicts the next piece of text, one token at a time. Watch the figure. The model has read, "The report is due on." It scores every possible next token. "Friday" scores highest, so it's picked and added to the text. Then the whole thing runs again, with "Friday" now part of the context. One token at a time. A token is about three quarters of a word. "Large" means billions of learned settings, called weights. And "model" means the engine only, not the app around it. Everything an LLM does, writing a memo, answering a question, writing code, comes from repeating that one step. That's why it's so fluent. And it's also why it can be fluently wrong.

[2:12] made
How is a model made? In three stages. First, pretraining. The model learns language and patterns by predicting the next token across an enormous amount of text. Second, post-training. It's tuned to follow instructions, refuse harmful requests, and use tools. Third, it's deployed. At that point its weights are frozen, and a harness is wrapped around it. That has three consequences. The model has a knowledge cutoff. It does not learn from your chats. And anything current reaches it only because the harness went and fetched it.

[2:47] isnot
Let's clear up six common beliefs. "It looks things up." It doesn't. It generates. It only fetches information if the harness gives it a tool to do so. "It learns from my chats." The weights are frozen. What apps call memory is the harness saving notes and feeding them back in. "It knows today's news." Only up to its cutoff, plus whatever gets fetched. "Same question, same answer." No. Output varies from run to run. "Wrong answers are rare." Confident, fluent errors are a normal failure mode. That's why checking output matters so much. And, "customizing means training." Usually, good prompts, skills and retrieval are enough.

[3:29] othermodels
One more thing about models. A single request usually passes through several of them, not just one. Take a request like, "Review these scanned vendor proposals against last quarter's scores." A classifier screens the question. A vision model reads the scans. An embedding model and a reranker find the right passages. Then the language model writes the comparison. Another classifier screens the output. And finally, a person checks every number. Each of these models is a dependency, often from a different vendor. The language model is the star, but it writes near the end.

[4:04] rule
Here's the one idea to hold on to. The model thinks. Skills teach it how. Tools let it act. And the harness decides which of those it gets. One more piece. An API lets your own software reach the model directly. And when that happens, your software becomes the harness.

[4:22] parts
Let's build that picture. The harness is the app or platform your organization approves. Inside it are the instructions it adds to every request, the memory it saves and feeds back in, the permissions and approval gates, and the logging. In the middle sits the model, which only sees what the harness hands it. Skills are packaged instructions that tell the model how to do a job well. Tools let it fetch facts and take actions, often through a standard called MCP. Watch a request come in. It passes the permissions check, reaches the model, calls a tool, and leaves as an answer, and every step is logged. Two common confusions. Skills are not training. And tools are not "internet access." The model reaches only what it's connected to.

[5:08] samemodel
Here's why the harness matters so much. Take the very same model and put it in three different harnesses. In a chat app, it sees what you paste, plus search or connectors if they're switched on. You drive every turn. Low reach, and it acts alone very little. In a coding agent, it can read and edit files, run commands, and loop until the job is done. High reach, and it acts alone a lot, which is why approval gates matter. In your own script, it sees only what your code sends through the API. You decide its reach, and you own every control. Same engine. Different reach. Different risk. That's why security approves the harness, not just the model.

[5:50] types
There are six kinds of harness you'll meet. One, chat assistants: Claude dot AI, ChatGPT, the Gemini app. Two, AI built into the tools you already use: email, documents, ticketing and case systems. Three, your organization's own approved platform or gateway, with several models behind one front door. Four, coding and agent tools, such as Claude Code, Codex CLI, or Gemini CLI. These read files, run commands, and loop toward a goal. Five, open-source agents you host yourself. Flexible, but with real supply-chain risk. And six, your own software, calling the model by API. In that case, you are the harness. Products change every month. Learn the categories, not the brand names.

[6:39] compare
To size up any harness, ask two questions. What can it reach? And how much does it act alone? A chat assistant sits low on both. Tools with AI built in, a little higher. An organization platform, in the middle. Coding and agent tools, and open-source agents, sit high on both. Your own software can land anywhere, because you build it. The rule is simple. The further up and to the right, the more controls it needs. And if your team can't answer "what can it reach," that's your first finding.

[7:09] endpoints
When your software calls a model, the API comes through one of three front doors. The vendor's own API gets the newest models first, under the vendor's terms. A cloud provider runs the model inside a boundary your organization may already approve, though versions can lag. And an approved platform or gateway puts many models behind one door, with review, access control and logging. The model behind each door is the same. The authorization, data handling and contract are not. So choose by authorization and data level first, and by model second. And keep the endpoint in configuration, so that switching is a one-line change.

[7:47] cwa
Now the three words people mix up most: chatbot, workflow, and agent. The test is one question. Who picks each step? In a chatbot, the person does, one message at a time. You ask, it answers, and you decide what happens next. The main risk is taking a wrong answer as fact. In a workflow, a designer picks the steps in advance. It follows the same fixed path on every run, and AI can be one step in that path. The risk is that it breaks quietly when the inputs change. In an agent, the AI picks its own steps at run time. It plans, acts, checks, and loops until the goal is met, and then a person reviews. The risk is that mistakes compound across steps. One piece of advice. If you already know the steps, build a workflow. It's more predictable, easier to approve, and easier to test.

[8:40] available
How far you can go depends on what your organization has approved. With chat only, you're at stage one: prompting, saved instructions, and copy-and-paste steps. Add an API, and you can build scripted or low-code workflows, through stage three. Add tool calling, and workflows can look things up or take approved actions, which is stage four. And with a full agent harness, you reach stage five: agents with skills and approval gates. Here's the important part. If your team only has chat and an API, you can stop at stage three and still get real, working automation.

[9:15] exercise
Time to practice. Pause the video for this one. Part A. Look at the ten tasks on screen and sort each one: chatbot, workflow, or agent. Remember the test: who picks each step? Part B. Pick one AI tool your team uses today and answer five questions. Which of the six types is it? Which models sit behind it? What can it reach? How much does it act alone? And who approved it, and for what data? If you can't answer that last question, that's worth following up on. When you're ready, here's the answer key for Part A. Chatbot: one, four, seven and ten. Workflow: two, five and eight. Agent: three, six and nine. And if you said "it depends on who picks the steps," you've got the idea.

[10:03] check
Before we finish, see if you can answer these six questions in your own words. What is a large language model, in one sentence? Why can the same model be safe in one app and risky in another? Does the model learn from your chats, and if not, what is memory? Can you name three types of harness? Who picks each step in a chatbot, a workflow, and an agent? And when would you choose a workflow over an agent? If any of these feel shaky, go back to that part of the video.

[10:31] bridge
Here's where we go next. Today you saw that the model and the harness are separate parts, and that the same model can sit behind many harnesses and many front doors. Models, vendors and apps will keep changing. So in Session 2, we ask the strategic question. If models and harnesses are replaceable, what does your organization need to own, so that switching is a configuration change, not a rebuild? The answer is seven foundations: approved tools, containers, scanning, skills, approved packages, a multi-vendor API framework, and stored evaluations, which are how you know a switch actually worked. Thanks for watching. See you in Session 2.
