import { afterEach, describe, expect, it, vi } from "vitest";

import { api } from "./api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("ThreatAtlas API client", () => {
  it("retrieves the local review queue from the same-origin API", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify([{ case_id: "case-demo", title: "Demo", source_label: "Local", tags: [], summary: {} }]), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    const cases = await api.listCases();

    expect(fetchMock).toHaveBeenCalledWith("/api/cases", undefined);
    expect(cases[0]?.case_id).toBe("case-demo");
  });

  it("sends an explicitly supplied local record to the bounded analysis endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ case_id: "case-local" }), { status: 200, headers: { "Content-Type": "application/json" } })
    );
    vi.stubGlobal("fetch", fetchMock);

    await api.analyze({ case_id: "case-local", title: "Synthetic", indicators: [], evidence: [] });

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/analyze",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ case: { case_id: "case-local", title: "Synthetic", indicators: [], evidence: [] } })
      })
    );
  });
});
