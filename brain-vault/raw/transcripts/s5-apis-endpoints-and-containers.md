Session 5 - APIs, Endpoints and Containers — transcript

[0:00] cover
Welcome to Session 5 in our series on using generative AI well, and safely, at work. Session 4 ended with a question: how does your own software reach the model safely? That's today. When your code calls the model, your team owns the controls. Watch the figure. Your code sits sealed in a container. The request leaves through one door, to an approved endpoint, and the answer comes back. Anything else trying to get out is blocked at the wall.

[0:27] agenda
By the end of this session, you'll be able to do four things. Explain what changes when your code calls the model. Choose an endpoint, and keep it in config. Describe what a container allows, and what it blocks. And name the four run controls. No one needs to write code today. You just need to know what to ask for.

[0:46] why
Why does this matter? Because three problems start the day code calls the model. "The key was in the script." A pasted API key ends up in the code, the repository, and the logs. "We can't switch vendors." The endpoint and model name are hard-coded in fifty places. And, "nobody knows what ran." No record of which prompt, which model version, or who reviewed it. So the question is: who owns the controls when code calls the model?

[1:14] api
Start with the API. Through the API, your software becomes the harness. Watch the figure. Your code loads the saved prompt from the library. It adds the document. Then it builds the request, with a pinned model version. It sends it to the endpoint named in config. The model answers. The response comes back as a draft. And every call is logged. Remember: the API is not the chat app. The terms, data retention and authorization are different.

[1:43] own
The chat app did six jobs for you. Now your code does. Watch them move across. One: the instructions, a saved prompt in the library. Two: data handling, what goes where. Three: logging, who ran what. Four: keys and network. Five: review, a person signs. And six: cost, with limits for every workflow. Keep those numbers in mind. They come back on every figure that follows.

[2:10] endpoints
Next, where the API comes from. There are three front doors to the same model. Watch the config file. First, the endpoint points at the vendor API, the maker's own. Change one line, and it points at a cloud provider, inside your cloud account. One more line, and it's the approved platform, your org's one approved gateway. The model behind every door is the same. Then pin the model version. The contract is what changes, so authorize first, then pick the model.

[2:40] config
Four habits make a switch a one-line change. Keep the endpoint in config, not in the code. Pin the model version, never "latest." Use one request shape, written the same way for every door. And allow-list that endpoint, so it's the container's only permitted address.

[2:57] container
Now, containers. Every harness, and every workflow that calls the model, runs sealed in a container. Watch what's inside: the exact libraries that were reviewed, your code and saved prompt, and a key injected at run time. That's job four. There's one way out. The call to the model endpoint goes through. A request to any other website is blocked at the wall, so an injected instruction has nowhere to send your data. A reach for the computer's own files is blocked too. And the same scanned image is authorized and redeployed. That's what makes approvals faster.

[3:30] controls
Then, the four run controls. Every run leaves a record. Watch the figure. One: the key lands from the secrets store, never from the code. Two: the model version is pinned, so you switch on purpose, after the tests pass. Three: the audit log fills in. Who ran it, which prompt, which model, how many tokens, and who reviewed it. Four: the cost meter rises, run after run, until it stops at the limit.

[3:56] available
What can your team do today? More than you might think. Watch the staircase. Chat only lights step one. Chat plus an API lights steps two and three: one call from code, and a workflow. That's already here, with what most teams have. Tool calling adds step four. And agents and skills add step five.

[4:16] rule
Here's the one idea to hold on to. Who owns the controls? You do. Call it from code. Keep the endpoint in config. Seal it in a container. Because your code becomes the harness, so your team owns the controls.

[4:30] exercise
Time to practice. Pause the video for this one. Hints are on the slide, so cover them if you want the challenge. Part A. Read it. Here's a short piece of pseudocode, where "doc" is the file being summarized. Find five problems. Part B. Box it. For a weekly contract-summary workflow, fill in the blank container: what's inside, the one endpoint it can reach, where the key comes from, what each run logs, and its rate and cost limit. If you found the key in the code first, you're not alone.

[5:02] check
Before we finish, see if you can answer these six questions in your own words. When your code calls the model instead of the chat app, what does your team now have to handle? Can you name the three kinds of endpoint? Which do you choose first, the door or the model, and why? Why keep the endpoint in config? What can a container reach? And can you name the four run controls? If any of these feel shaky, go back to that part of the video.

[5:29] bridge
Here's where we go next. Today we sent one request from code, safely. But how do you turn a repeat task into a fixed pipeline? That's Session 6: building workflows. Fixed steps the script decides, one check, and a person who signs.

[5:46] sandbox
One last slide, for facilitators: build the Stage 2 sandbox once, and reset it for each group. A pre-scanned base image. Training keys with low limits. Made-up sample documents. And a starter prompt library with test cases. Class time goes to learning, not setup. Thanks for watching. See you in Session 6.
