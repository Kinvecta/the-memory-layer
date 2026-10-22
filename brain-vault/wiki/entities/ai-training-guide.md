---
type: entity
summary: The AI Training Guide for Teams Adopting Generative AI (October 2026 edition) - a tool- and industry-agnostic guide in PDF, HTML and Markdown, organized in five parts plus glossary and appendix, that the train-the-trainer series is built from.
sources: ["[[raw/guide/ai-training-guide-oct-2026]]"]
related: ["[[source-ai-training-guide]]", "[[train-the-trainer-series]]", "[[five-stage-training-progression]]", "[[agnostic-ai-platform]]", "[[measuring-training-results]]", "[[the-memory-layer]]"]
aliases: [AI Training Guide, the guide, AI Training Guide for Teams Adopting Generative AI]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# AI Training Guide (document)

**TL;DR:** *AI Training Guide for Teams Adopting Generative AI*, October 2026 edition, is the master document this brain is founded on. It lays out where the field is heading, where people need to focus, and a five-stage path "from safe chat use to containerized agents with skills, tools and MCP." It is the content source for the eight-session [[train-the-trainer-series]] and its two deep dives.

## Who / what
- **Title:** AI Training Guide for Teams Adopting Generative AI ([[source-ai-training-guide]]).
- **Edition:** October 2026. Appendix links and product details were checked October 2026; platform features "change monthly, so recheck before each cohort."
- **Formats:** PDF and HTML (which carry the drawings) and a Markdown text version, where diagrams are referenced by figure number only (Figures 1-23). The Markdown copy lives at [[raw/guide/ai-training-guide-oct-2026]] (about 12,500 words).
- **Stance:** tool-agnostic and industry-agnostic; vendor names appear only as examples.
- **Audience:** analysts, operators, engineers, managers and supporting contractors in any organization adopting generative AI; no coding background assumed. Delivery mixes written content, worked examples, short videos and in-person sessions (§1.2).

## Role in this brain
The primary reference for nearly every concept page. Its summary page is [[source-ai-training-guide]]; its five-stage structure is captured in [[five-stage-training-progression]], and its Part 3 foundations in [[agnostic-ai-platform]].

## Key facts
**Structure**

| Part | Title | Covers |
|---|---|---|
| 1 | Orientation | At a glance; purpose and audience; six trainee outcomes; where things are heading; seven ranked focus areas |
| 2 | How the pieces work | Chatbot vs workflow vs agent; harness, model, skills, tools, APIs; endpoints; MCP; [[tokens]]; [[how-ai-finds-your-data]] |
| 3 | The platform the organization owns | Seven foundations; [[containerization]]; skills deep dive; skills + tools; [[prompt-and-skill-library]] |
| 4 | Security, policy and governance | The one rule and its controls; [[prompt-injection]]; operational controls; DevSecOps by component |
| 5 | The training program | Five stages; practical tool use by stage; role targets; course map; training environment; [[measuring-training-results]] |
| - | Glossary | Acronyms, diagram color key, key terms |
| - | Appendix | How each platform uses skills; governance frameworks (NIST AI RMF, ISO/IEC 42001, EU AI Act, OWASP LLM Top 10, SOC 2); recommended training resources |

**How to read it (by role)** - Leaders: Part 1, the seven foundations, and the "How far each role goes" table. Analysts and operators: Part 2, then Part 5 through Stage 3. Engineers and security staff: all five parts, with Parts 3 and 4 as the working reference. Facilitators: Part 5 end to end, with the Appendix tables as handouts.

**Headline claims** (§1.1): learn in five stages that give AI more control only as people prove they can contain and check it; everything past basic chat runs in a container; the most common failure is too little evaluation; top risks are data in the wrong system, unverified output, and prompt injection.

**Diagram color key:** orange = person; blue = model; teal = code, rules and harness; navy = tools and MCP; magenta = data and outside systems; purple = prompts and skills; dark green = containers; salmon = the API. Green = allowed, red = blocked or attack path; dashed = blocked or outside your control.

**Course map:** the guide's own facilitator map has six sessions (60, 90, 120, 180, 180, 240 minutes); the produced video series restructures this into eight sessions plus two deep dives ([[train-the-trainer-series]]).

## See also
[[source-ai-training-guide]] · [[train-the-trainer-series]] · [[five-stage-training-progression]] · [[the-memory-layer]]
