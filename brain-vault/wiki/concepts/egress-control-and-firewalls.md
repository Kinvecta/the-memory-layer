---
type: concept
summary: Layered, default-deny network controls in both directions for AI containers, with an egress proxy hostname allow-list so a prompt-injected agent can reach only the LLM API and approved backends.
sources: ["[[raw/transcripts/ddb-devsecops-containers-cicd]]", "[[raw/research/containers-cicd-brief]]", "[[raw/guide/ai-training-guide-oct-2026]]", "[[raw/transcripts/s5-apis-endpoints-and-containers]]"]
related: ["[[containerization]]", "[[prompt-injection]]", "[[devsecops-pipeline]]", "[[container-hardening]]", "[[apis-and-endpoints]]", "[[building-an-mcp-server]]", "[[ai-governance-and-controls]]"]
aliases: [egress allow-list, network policy, firewall, default deny]
confidence: high
created: 2026-10-21
updated: 2026-10-21
last_reviewed: 2026-10-21
agent_written: true
---
# Egress control and firewalls

**TL;DR:** Think of a building with several locked doors, each checking again, from the outside in and in both directions. Inbound comes only from the load balancer; outbound goes only to DNS, the LLM API and approved backends; everything else is blocked and logged ([[source-ddb-devsecops-containers-cicd]] [14:31], [15:27]). Egress matters as much as ingress for AI: a prompt-injected agent with open internet can send your data anywhere.

## What it is
Network layers and tools ([[source-ddb-devsecops-containers-cicd]] [15:27]; [[source-containers-cicd-brief]] §12.2):
1. **Edge WAF:** filters inbound requests; rate-limits costly LLM endpoints (AWS WAF, Front Door, Cloud Armor, Cloudflare).
2. **Cloud firewall / security groups:** allow or deny by address, port, protocol.
3. **Egress proxy:** one exit with a hostname allow-list and logs (AWS Network Firewall, Azure Firewall, Squid, Envoy).
4. **Host firewall:** nftables, or ufw with the `DOCKER-USER` chain.
5. **Kubernetes NetworkPolicy:** default deny between pods, enforced by Calico or Cilium; has **no hostname field**.
6. **Hostname-aware rules:** Cilium `toFQDNs`, GKE FQDN policies, plus a service mesh like Istio for mTLS between services.
The brief lists eight layers, splitting out the service mesh and adding a last one inside the container: non-root, read-only, no shell ([[container-hardening]]).

## Why it matters
Network limited to approved endpoints is one of the four things a container gives AI work: injected instructions have nowhere to send data ([[source-ai-training-guide]] §3.2, §4.1). In Session 5's picture, the call to the model endpoint goes through; any other website and the host's files are blocked at the wall ([[source-s5-apis-endpoints-and-containers]] [2:57]). Allow-listing the endpoint is one of the four config habits ([[source-s5-apis-endpoints-and-containers]] [2:40]). See [[prompt-injection]].

## How it works
**Why a proxy:** LLM API addresses change often and are shared behind CDNs, so an IP allow-list is either wrong or too broad; you need something that sees the name (proxy `CONNECT` host, TLS SNI/Host header, or DNS-watching CNI). SNI/Host filtering trusts the client, so AWS advises adding IP rules where manipulation is a concern ([[source-containers-cicd-brief]] §12.3).

**Kubernetes pattern** ([[source-containers-cicd-brief]] §6.5): default-deny egress, then allow only DNS (kube-dns, port 53) and the egress proxy (port 3128), which allow-lists `api.anthropic.com`, your Bedrock or Azure OpenAI endpoint, etc. Cloud private endpoints (Bedrock via PrivateLink, Azure OpenAI private endpoint) keep traffic off the public internet, often required for CUI.

> [!warning] The Docker and ufw gotcha
> A team enables ufw "deny incoming," then publishes port 8080. It is reachable from the internet anyway, because Docker's NAT rules divert traffic before ufw sees it. Fixes: bind to `127.0.0.1` behind a reverse proxy, or put rules in the `DOCKER-USER` chain (with an established/related accept first); treat the cloud security group as the real perimeter; test from outside with `nmap` after every change ([[source-ddb-devsecops-containers-cicd]] [14:31]; [[source-containers-cicd-brief]] §12.4).

## In practice
- **Log and alert.** A blocked outbound attempt from an AI workload is a high-signal alert; it often means prompt injection or a compromised dependency ([[source-ddb-devsecops-containers-cicd]] [15:27]).
- **Risk -> control** ([[source-containers-cicd-brief]] §12.6): injection exfiltration -> egress allow-list; malicious MCP server phoning home -> default-deny plus per-workload FQDN policy; accidental internet exposure of an HTTP MCP server -> security group + WAF, bind to localhost; DNS rebinding -> bind to 127.0.0.1 and validate the Host header ([[building-an-mcp-server]]); lateral movement -> namespace default-deny and mTLS.
- MCP servers run with egress only to their backing system; workflows only to the model endpoint and approved MCP servers ([[source-ai-training-guide]] Part 4).
- Azure Container Apps needs a workload-profiles environment to route egress through Azure Firewall ([[source-containers-cicd-brief]] §11.2).

## See also
[[containerization]] · [[prompt-injection]] · [[devsecops-pipeline]]
