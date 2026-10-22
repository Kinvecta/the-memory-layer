Session 4 - Tokens, Context and How AI Finds Your Data — transcript

[0:00] cover
Welcome to Session 4 in our series on using generative AI well, and safely, at work. Session 3 ended with a question: what can the model actually see when it answers? Today has two answers. First, tokens: the unit the model reads, writes, and bills. And second, finders: the ways your tools fetch your data. Watch the picture. The context window fills with everything you send. A finder pulls in your documents. And the answer comes out the top.

[0:29] agenda
By the end of this session, you'll be able to do four things. Explain what a token is, and why it matters. Read what fills a context window. Estimate the token cost of a workflow. And pick the right finder for your data. We'll spend the most time on finders, because that's where most "the AI couldn't find it" complaints come from.

[0:49] why
Why does this matter? Because three common complaints share one root cause. "The bill surprised us." Cost comes from context re-sent in loops and long chats, not from the answer. "It forgot what I said." Long chats fill the window, and early turns get dropped. And, "it couldn't find the table." The wrong finder was used, and the table was flattened into prose. So the question is: what does the model see, and what does it cost?

[1:16] tokens
Start with tokens. A token is the piece of text the model reads and writes. Watch the figure. Here's a sentence: "The quarterly report is due Friday." Six words. Now watch it split. It becomes eight tokens. Now a line of codes and numbers: a purchase order and a dollar amount. It splits into fourteen small tokens. Numbers and codes cost more. And here's the catch. Another vendor's tokenizer counts the same sentence differently. Every vendor counts differently, so treat any count as an estimate.

[1:47] tokentypes
Not all tokens are the same, or cost the same. Input tokens are everything you send: instructions, tools, documents, history, and the question. Output tokens are the answer. They're priced higher, and they drive how long you wait. Thinking tokens are billed as output. Cached tokens are a discount for a stable prefix. Images and audio become tokens too. Every connected tool adds its description. And embedding tokens are charged when documents are indexed. The rule: what you send costs more than what you get back.

[2:18] budget
Now the context window. It's one fixed budget, shared by input and output. Watch it fill. First the system prompt. Then the tool definitions. Then the chat history. Then the retrieved documents, usually the biggest block. Then the new question. And room is reserved at the top for the answer. The system prompt and tool definitions are the same every time, so they can be cached and re-read cheaply. Now look at the receipt. Input tokens are the bulk of the bill. Cached reads are cheap. And the output is small.

[2:51] chat
Here's why long chats get expensive. Every turn re-sends the whole conversation. Watch the first turn: the system prompt and your question go in, and an answer comes back. In the second turn, everything is sent again, plus the new question. And in the third turn, the input is bigger still. The output stays small. Caching turns the repeated history into cheap reads. The habit to teach is simple: when the topic changes, start a new chat.

[3:19] matters
So why should your team care about tokens? Six reasons. Cost: tokens per run, times runs per month. Capacity: one window, shared by everything. Speed: output is written one token at a time. Rate limits: a job that works in testing can be throttled in production. Quality: a lean context beats a stuffed one. And swapping models: counts, costs and limits change with the tokenizer.

[3:45] finders
Now, how AI finds your data. The model only sees what the finders hand it. Watch the figure. One question: which vendors scored lowest on site safety last quarter? The harness sends it to four finders at once. Semantic search finds a memo passage by meaning. Keyword search finds an exact vendor ID. A structured query pulls rows from the scores table. And multimodal retrieval finds a chart on a scanned page. The harness merges the results, and hands them to the model with citations. The answer cites the memo and the table. The model never searches on its own. It reads what the finders return.

[4:22] sixways
There are six ways AI fetches data, and no single one covers everything. Everything in context, for small, stable sets. Semantic search, to find meaning across large prose. Keyword search, for exact names, I-Ds and codes. Agentic search, where the AI plans its own searches over live files. Structured queries, for exact records from tables and databases. And multimodal retrieval, for scans, slides and charts. One security point. An index is a copy of your data. It needs the same access rules and approvals as the source.

[4:58] datatypes
So match the finder to the data. Text documents and memos: semantic and keyword search together. Tables and spreadsheets: structured queries, because totals should come from a query, not from the model reading rows. Images and scans: multimodal retrieval, or a vision model. Code: agentic search over the live files. And live records: structured queries only, through an approved connection.

[5:24] rule
Here's the one idea to hold on to. Send less. Cache what's stable. Fetch with the finder that fits. Because the model only sees what you send it, and what the finders return.

[5:36] exercise
Time to practice. Pause the video for this one. Part A. Count it. Paste one of your own non-sensitive prompts into an approved token counter. Note the input and output tokens. Multiply by how many times a month it runs. Then ask: what would a shorter prompt, or caching, save? Part B. Find it. For six real questions, pick the right finder. A remote-work policy. A ticket number. Total spend by vendor. An org chart slide. Retry logic in your code. And a three-page brief. If you picked semantic search for total spend, think again.

[6:13] check
Before we finish, see if you can answer these six questions in your own words. Roughly how much text is one token? Why do long chats cost more each turn? What shares the context window? What does caching make cheaper? Can you name three ways AI fetches data? And why is a search index a security question? If any of these feel shaky, go back to that part of the video.

[6:37] bridge
Here's where we go next. Today we saw what fills a request, and how data gets fetched. But how does your own software reach the model safely? That's Session 5: AP-Is, endpoints, and containers. Calling the model from code, keeping the endpoint in configuration, and running everything sealed in, with one way out. Thanks for watching. See you in Session 5.
