import pytest
from mcp import Client

from brain.mcp_server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def vault(tmp_path, monkeypatch):
    (tmp_path / "memory").mkdir()
    (tmp_path / "memory" / "core.md").write_text("# Core\nMark runs AI training.\n")
    (tmp_path / "wiki").mkdir()
    (tmp_path / "wiki" / "mcp.md").write_text("---\ntype: concept\n---\n# MCP\n\nModel Context Protocol plugs tools into a harness. See [[skills]].\n")
    (tmp_path / "wiki" / "skills.md").write_text("---\ntype: concept\n---\n# Skills\n\nFolders of instructions. Related: [[mcp]].\n")
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "src.md").write_text("original")
    (tmp_path / "index.md").write_text("# Index\n- [[mcp]]\n- [[skills]]\n")
    (tmp_path / "log.md").write_text("# Log\n")
    monkeypatch.setenv("BRAIN_VAULT", str(tmp_path))
    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:9")  # force keyword fallback
    return tmp_path


@pytest.fixture
async def client(vault):
    async with Client(mcp, raise_exceptions=True) as c:
        yield c


@pytest.mark.anyio
async def test_tools_listed(client):
    names = {t.name for t in (await client.list_tools()).tools}
    assert {"brain_wake_up", "brain_search", "brain_read", "brain_remember", "brain_save_page",
            "brain_log", "brain_lint", "brain_reindex"} <= names


@pytest.mark.anyio
async def test_wake_search_read(client):
    r = await client.call_tool("brain_wake_up", {})
    assert "Mark runs AI training" in r.content[0].text
    r = await client.call_tool("brain_search", {"query": "protocol tools harness"})
    assert r.structured_content["hits"][0]["path"] == "wiki/mcp.md"
    r = await client.call_tool("brain_read", {"path": "wiki/mcp.md"})
    t = r.content[0].text
    assert "backlinks (2)" in t and "wiki/skills.md" in t and "index.md" in t


@pytest.mark.anyio
async def test_guards(client, vault):
    r = await client.call_tool("brain_read", {"path": "../../etc/passwd"})
    assert r.is_error
    r = await client.call_tool("brain_save_page", {"path": "raw/src.md", "content": "overwrite attempt!!"})
    assert r.is_error
    assert (vault / "raw" / "src.md").read_text() == "original"
    r = await client.call_tool("brain_save_page", {"path": "wiki/questions/q1", "content": "# Q1\n\nAnswer text."})
    assert not r.is_error and (vault / "wiki" / "questions" / "q1.md").exists()
    r = await client.call_tool("brain_remember", {"note": "Prefers hybrid search", "kind": "preference"})
    assert "working.md" in r.content[0].text
